*** Settings ***
Library           OperatingSystem
Library           String

*** Variables ***
${LOGCAT_FILE}    ${CURDIR}/logcat_applications.txt
${START_MARKER}   ActivityTaskManager: START u0
${END_MARKER}     Layer: Destroyed ActivityRecord

*** Test Cases ***
Analyze Application Lifespan in Logcat
    ${content}=    OperatingSystem.Get File    ${LOGCAT_FILE}
    ${start_time}=    Get Marker Time    ${content}    ${START_MARKER}
    ${end_time}=    Get Marker Time    ${content}    ${END_MARKER}
    Log    Start Time: ${start_time}
    Log    End Time: ${end_time}

*** Keywords ***
Get Marker Time
    [Arguments]    ${content}    ${marker}
    @{lines}=    Split String    ${content}    \n
    ${time}=    Set Variable    ${EMPTY}
    FOR    ${line}    IN    @{lines}
        ${line_matched}=    Run Keyword And Return Status    Should Contain    ${line}    ${marker}
        Run Keyword If    ${line_matched}    Set Variable    ${line}
        ...    AND    Exit For Loop
    END
    RETURN    ${time}

