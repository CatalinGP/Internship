*** Settings ***
Library    OperatingSystem
Library    Collections
Library    String

*** Variables ***
${INPUT_FILE}     ${CURDIR}/ccs2/RELIABILITY/TC_SWQUAL_CCS2_RELIABILITY_B2B_PA.robot
@{KEYWORDS_TO_CHECK}    START TEST CASE
...     SAVE CANDUMP LOGS
...     START LOGCAT MONITOR
...     START DLT MONITOR
...     CHECK VIN AND PART ASSOCIATION
...     CHECK VIN CONFIG ON
...     SET VNEXT TIME AND DATE ON IVC
...     SET PROP APLOG
...     ENABLE IVI DEBUG LOGS
...     REMOVE IVI APLOG
...     REMOVE IVI DROPBOX CRASHES


*** Test Cases ***
Trace undefined HLK's
    Execute Check

*** Keywords ***
Extract Resource File Paths
    [Arguments]    ${input_file}
    ${resource_paths}=    Create List
    ${file_contents}=    Get File    ${input_file}
    ${lines}=    Split To Lines    ${file_contents}
    ${resource_lines}=    Create List

    FOR    ${line}    IN    @{lines}
        ${line}=    Strip String    ${line}
        ${contains_resource}=    Run Keyword And Return Status    Should Contain    ${line}    Resource    ignore_case=True
        IF    ${contains_resource}
            Append To List    ${resource_lines}    ${line}
        END
    END

    FOR    ${line}    IN    @{resource_lines}
        ${resource_path}=    Get Substring    ${line}    9
        ${resource_path}=    Strip String    ${resource_path}
        ${adjusted_path}=    Replace String    ${resource_path}    ../   ccs2/
        Append To List    ${resource_paths}    ${adjusted_path}
    END
    RETURN    ${resource_paths}

Check Keywords In Resource Files
    [Arguments]    ${resource_paths}    @{keywords_to_check}
    ${missing_keywords}=    Create List    @{keywords_to_check}
    FOR    ${path}    IN    @{resource_paths}
        ${content}=    Get File    ${path}
        ${lines}=    Split To Lines    ${content}
        ${index}=    Set Variable    0
        FOR    ${keyword}    IN    @{missing_keywords}
            ${keyword_found}=    Set Variable    ${FALSE}
            FOR    ${line}    IN    @{lines}
                ${contains_keyword}=    Run Keyword And Return Status    Should Contain    ${line}    ${keyword}
                Run Keyword If    ${contains_keyword}    Set Variable    ${TRUE}    AND    Exit For Loop
            END
            Run Keyword If    ${keyword_found}    Remove From List    ${missing_keywords}    ${index}
            Run Keyword Unless    ${keyword_found}    Set Variable    ${index}+1    ${index}
        END
    END
    Log    ${missing_keywords}
    RETURN    ${missing_keywords}

Add Missing Keywords To Imposters
    [Arguments]    @{missing_keywords}
    ${imposters_file}=    Set Variable    ${CURDIR}/Imposters.robot
    FOR    ${keyword}    IN    @{missing_keywords}
        ${to_append}=    Catenate    SEPARATOR=\n    ${keyword}\n    \    [Arguments]    \${foo}\n    \    Keyword not defined, waiting for implementation.
        Append To File    ${imposters_file}    ${to_append}
    END

Execute Check
    ${resource_paths}=    Extract Resource File Paths    ${INPUT_FILE}
    Check Keywords In Resource Files    ${resource_paths}    ${KEYWORDS_TO_CHECK}