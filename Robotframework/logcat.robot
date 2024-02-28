*** Settings ***
Library    OperatingSystem
Library    Collections
Library    String
Library    BuiltIn
Library    DateTime

*** Variables ***
${LOGCAT_FILE}    logcat_applications.txt
${OUTPUT_FILE}    output.yml

*** Test Cases ***
Analyze Lifespan of Android Applications
    ${data}=    Parse Logcat File    ${LOGCAT_FILE}
    ${lifespans}=    Calculate Lifespan    ${data}
    Output App Data To File    ${lifespans}    ${OUTPUT_FILE}
    Generate Test Verdict      ${lifespans}

*** Keywords ***
Parse Logcat File
    [Arguments]    ${file_path}
    ${parsed_data}=    Create List
    ${file_contents}=    Get File    ${file_path}
    ${relevant_lines}=    Get Lines Matching Regexp    ${file_contents}    .*ActivityTaskManager: START u0.*|.*Layer: Destroyed ActivityRecord.*
    ${lines}=    Split To Lines    ${relevant_lines}

    ${app_states}=    Create Dictionary

    FOR    ${line}    IN    @{lines}
        ${start_marker}=    Run Keyword And Return Status    Should Contain    ${line}    ActivityTaskManager: START u0
        ${end_marker}=    Run Keyword And Return Status    Should Contain    ${line}    Layer: Destroyed ActivityRecord

        IF    ${start_marker}
            Run Keyword    Extract Start Marker Data    ${app_states}    ${line}    ${parsed_data}
        ELSE IF    ${end_marker}
            Run Keyword    Extract End Marker Data    ${app_states}    ${line}    ${parsed_data}
        END

    END
    RETURN    ${parsed_data}

Extract Start Marker Data
    [Arguments]    ${app_states}    ${line}    ${parsed_data}
    ${package_name}=    Get Package Name    ${line}
    ${start_time}=    Fetch Time    ${line}
    ${app_info}=    Create Dictionary    start_time=${start_time}    end_time=${EMPTY}
    Set To Dictionary    ${app_states}    ${package_name}    ${app_info}

Extract End Marker Data
    [Arguments]    ${app_states}    ${line}    ${parsed_data}
    ${package_name}=    Get Package Name    ${line}
    ${end_time}=    Fetch Time    ${line}
    ${app_exists}=    Run Keyword And Return Status    Dictionary Should Contain Key    ${app_states}    ${package_name}
    IF    ${app_exists}
        ${app_info}=    Get From Dictionary    ${app_states}    ${package_name}
        Set To Dictionary    ${app_info}    end_time    ${end_time}
        ${app_data}=    Create Dictionary    package=${package_name}    start_time=${app_info}[start_time]    end_time=${end_time}
        Append To List    ${parsed_data}    ${app_data}
        Remove From Dictionary    ${app_states}    ${package_name}
    ELSE
        Log    Warning: End marker found for ${package_name} without a corresponding start marker.
    END

Get Package Name
    [Arguments]    ${line}
    ${com_start}=    Set Variable    ${line.find('com.')+4}
    ${package_and_activity}=    Get Substring    ${line}    ${com_start}    ${None}
    ${slash_index}=    Set Variable    ${package_and_activity.find('/')}
    ${package_name}=    Get Substring    ${package_and_activity}    0    ${slash_index}
    RETURN    ${package_name}

Fetch Time
    [Arguments]    ${line}
    ${time}=    Get Substring    ${line}    6    18
    RETURN    ${time}

Calculate Lifespan
    [Arguments]    ${data}
    ${lifespans}=    Create List
    FOR    ${app}    IN    @{data}
        Continue For Loop If    '${app['package']}' == '' or '${app['start_time']}' == '' or '${app['end_time']}' == ''
        ${start_sec}=    Convert Time To Seconds    ${app['start_time']}
        ${end_sec}=    Convert Time To Seconds    ${app['end_time']}
        ${lifespan}=    Evaluate    ${end_sec} - ${start_sec}
        ${app_lifespan}=    Create Dictionary    package=${app['package']}    lifespan=${lifespan}
        Append To List    ${lifespans}    ${app_lifespan}
    END
    RETURN    ${lifespans}

Output App Data To File
    [Arguments]    ${data}    ${filename}
    ${output}=    Set Variable    applications:\n
    ${index}=    Set Variable    1
    FOR    ${app}    IN    @{data}
        ${package}=    Set Variable    ${app.get('package', 'N/A')}
        ${start_time}=    Set Variable    ${app.get('start_time')}
        ${end_time}=    Set Variable    ${app.get('end_time')}
        ${lifespan}=    Set Variable    ${app.get('lifespan', 'N/A')}s

        ${app_output}=    Set Variable
        ...    - application_${index}\n
        ...    - app_path:  ${package}\n
        ...    - ts_app_started: ${start_time}\n
        ...    - ts_app_closed:  ${end_time}\n
        ...    - lifespan:  ${lifespan}\n
        ${output}=    Set Variable    ${output}${app_output}\n
        ${index}=    Evaluate    ${index} + 1
    END
    Create File    ${filename}    ${output}

Convert Time To Seconds
    [Arguments]    ${time_str}
    ${minutes}=    Get Substring    ${time_str}    3    5
    ${seconds}=    Get Substring    ${time_str}    6    8
    ${milliseconds}=    Get Substring    ${time_str}    9    12

    ${minutes}=    Set Variable If    '${minutes}' == ''    0    ${minutes.lstrip("0")}
    ${seconds}=    Set Variable If    '${seconds}' == ''    0    ${seconds.lstrip("0")}
    ${milliseconds}=    Set Variable If    '${milliseconds}' == ''    0    ${milliseconds.lstrip("0")}

    ${total_seconds}=    Evaluate    int(${minutes}) * 60 + int(${seconds}) + int(${milliseconds}) / 1000.0
    RETURN    ${total_seconds}

Generate Test Verdict
    [Arguments]    ${data}
    ${total_apps}=    Get Length    ${data}
    IF    ${total_apps} == 0
        Log    No applications analyzed. Test INCONCLUSIVE.
    ELSE
        ${apps_below_threshold}=    Evaluate    len([app for app in ${data} if app['lifespan'] < 30])
        ${percentage_below_threshold}=    Evaluate    100.0 * ${apps_below_threshold} / ${total_apps}
        ${apps_above_threshold}=    Evaluate    [app for app in ${data} if app['lifespan'] > 30]

        FOR    ${app}    IN    @{apps_above_threshold}
            Log    Warning: ${app['package']} was opened for more than 30 seconds. Lifespan: ${app['lifespan']} seconds.
        END

        Run Keyword If    ${percentage_below_threshold} < 75
        ...    Fail    Test FAILED: Percentage of apps below threshold is less than 75%
        ...    ELSE    Log    Test PASSED

    END