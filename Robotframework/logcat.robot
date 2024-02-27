*** Settings ***
Library           OperatingSystem
Library           Collections
Library           DateTime
Library            BuiltIn
Library            String

*** Variables ***
${LOG_FILE}       ${CURDIR}/logcat_applications.txt
${PASS_THRESHOLD} =    75
${LIFESPAN_LIMIT} =    30

*** Test Cases ***
Check Application Lifespan Verdict
    ${applications_lifespan}=    Parse Log File And Calculate Lifespan    ${LOG_FILE}
    ${passed}=    Verify Lifespan Criteria    ${applications_lifespan}    ${PASS_THRESHOLD}    ${LIFESPAN_LIMIT}
    Log    Test case result: ${passed}
    Run Keyword If    '${passed}' == 'FAILED'    Log Warning For Long Lifespan Applications    ${applications_lifespan}

*** Keywords ***
Parse Log File And Calculate Lifespan
    [Arguments]    ${log_file}
    ${log_content}=    Get File    ${log_file}
    ${lines}=    Split String    ${log_content}    \n
    ${app_starts}=    Create Dictionary
    ${applications_lifespan}=    Create Dictionary
    FOR    ${line}    IN    @{lines}
        ${is_start}=    Run Keyword And Return Status    Should Contain    ${line}    "ActivityTaskManager: START u0"
        ${is_end}=    Run Keyword And Return Status    Should Contain    ${line}    "Layer: Destroyed ActivityRecord"
        Run Keyword If    ${is_start}    Process Start Line    ${line}    ${app_starts}
        Run Keyword If    ${is_end}    Process End Line    ${line}    ${app_starts}    ${applications_lifespan}
    END
    RETURN    ${applications_lifespan}

Process Start Line
    [Arguments]    ${line}    ${app_starts}
    ${timestamp}=    Get Substring    ${line}    0    18
    ${app_name}=    Fetch App Name    ${line}
    Set To Dictionary    ${app_starts}    ${app_name}    ${timestamp}

Process End Line
    [Arguments]    ${line}    ${app_starts}    ${applications_lifespan}
    ${timestamp}=    Get Substring    ${line}    0    18
    ${app_name}=    Fetch App Name From End Line    ${line}
    ${start_timestamp}=    Get From Dictionary    ${app_starts}    ${app_name}    None
    Run Keyword If    '${start_timestamp}' != 'None'    Calculate And Set Lifespan    ${app_name}    ${start_timestamp}    ${timestamp}    ${applications_lifespan}

Fetch App Name
    [Arguments]    ${line}
    ${start_index}=    Find String    ${line}    "cmp="
    ${end_index}=    Find String    ${line}    "/"    ${start_index}
    ${app_name}=    Get Substring    ${line}    ${start_index+4}    ${end_index}
    RETURN    ${app_name}

Fetch App Name From End Line
    [Arguments]    ${line}
    ${start_index}=    Find String    ${line}    "com."
    ${end_index}=    Find String    ${line}    "}"    ${start_index}
    ${app_name}=    Get Substring    ${line}    ${start_index}    ${end_index}
    RETURN    ${app_name}

Calculate And Set Lifespan
    [Arguments]    ${app_name}    ${start_time}    ${end_time}    ${applications_lifespan}
    ${lifespan}=    Calculate Time Difference    ${start_time}    ${end_time}
    Set To Dictionary    ${applications_lifespan}    ${app_name}    ${lifespan}

Calculate Time Difference
    [Arguments]    ${start_time}    ${end_time}
    ${start_datetime}=    Convert To DateTime    ${start_time}    exact=True
    ${end_datetime}=    Convert To DateTime    ${end_time}    exact=True
    ${lifespan_seconds}=    Get Time Difference    ${end_datetime}    ${start_datetime}    result_format=seconds
    ${lifespan_minutes}=    Convert To Number    ${lifespan_seconds} / 60
    RETURN    ${lifespan_minutes}

Verify Lifespan Criteria
    [Arguments]    ${lifespan_results}    ${pass_threshold}    ${lifespan_limit}
    ${total_apps}=    Get Length    ${lifespan_results}
    ${apps_under_limit}=    Evaluate    sum(1 for app, lifespan in ${lifespan_results}.items() if lifespan < ${lifespan_limit})
    ${percentage}=    Evaluate    100.0 * ${apps_under_limit} / ${total_apps} if ${total_apps} != 0 else 0
    Run Keyword If    ${percentage} >= ${pass_threshold}    Return    PASSED
    RETURN    FAILED


Log Warning For Long Lifespan Applications
    [Arguments]    ${lifespan_results}
    ${long_lifespan_apps}=    Evaluate    [app for app, lifespan in ${lifespan_results}.items() if lifespan > ${LIFESPAN_LIMIT}]
    Log    Warning: The following applications have a lifespan longer than ${LIFESPAN_LIMIT} seconds: ${long_lifespan_apps}
