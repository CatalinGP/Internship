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
    ${updated_data}=    Calculate Lifespan    ${data}
    Output App Data To File    ${updated_data}    ${OUTPUT_FILE}
    Generate Test Verdict      ${updated_data}

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
    FOR    ${index}    IN RANGE   len(${data})
        ${start}=    Convert Time    ${data}[${index}][start_time]    result_format=number    exclude_millis=yes
        ${end}=    Convert Time    ${data}[${index}][end_time]    result_format=number    exclude_millis=yes
        ${lifespan}=    Evaluate    ${end} - ${start}
        Set To Dictionary    ${data}[${index}]    duration    ${lifespan}
    END
    Log    ${data}
    RETURN    ${data}

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

Generate Test Verdict
    [Arguments]    ${data}
    ${total_apps}=    Get Length    ${data}
    IF    ${total_apps} == 0
        Log    No applications analyzed. Test INCONCLUSIVE.
        RETURN
    END

    ${apps_below_threshold}=    Create List
    ${apps_above_threshold}=    Create List

    FOR    ${app}    IN    @{data}
        Run Keyword If    ${app['duration']} < 30
        ...    Append To List    ${apps_below_threshold}    ${app}
        ...    ELSE    Append To List    ${apps_above_threshold}    ${app}
        ...    AND IF    ${app['duration']} > 30
        ...    Log    Warning: ${app['package']} was opened for more than 30 seconds. Lifespan: ${app['duration']} seconds.
    END

    ${apps_below_threshold_count}=    Get Length    ${apps_below_threshold}
    ${percentage_below_threshold}=    Evaluate    100.0 * ${apps_below_threshold_count} / ${total_apps}

    Run Keyword If    ${percentage_below_threshold} < 75
    ...    Fail    Test FAILED: Percentage of apps below threshold is less than 75%
    ...    ELSE    Log    Test PASSED