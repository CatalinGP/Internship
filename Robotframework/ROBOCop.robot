*** Settings ***
Library    OperatingSystem
Library    Collections
Library    String

*** Variables ***
${INPUT_FILE}     RobotFramework/ccs2/RELIABILITY/TC_SWQUAL_CCS2_RELIABILITY_B2B_PA.robot
${REPORT_FILE}    RobotFramework/ccs2/Imposters.robot
@{KEYWORDS_TO_CHECK}    SAVE CANDUMP LOGS    START LOGCAT MONITOR    START DLT MONITOR    CHECK VIN AND PART ASSOCIATION    CHECK VIN CONFIG ON    SET VNEXT TIME AND DATE ON IVC    SET PROP APLOG    ENABLE IVI DEBUG LOGS   REMOVE IVI APLOG    REMOVE IVI DROPBOX CRASHES


*** Test Cases ***
Verify Resource Keywords In Main Test Case File
    ${resource_paths}=    Extract Resource File Paths    ${INPUT_FILE}
    Check Keywords In Resource Files    ${resource_paths}    @{KEYWORDS_TO_CHECK}


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
        # Remove ".." from the path
        ${adjusted_path}=    Replace String    ${resource_path}    ../   RobotFramework/ccs2/
        Append To List    ${resource_paths}    ${adjusted_path}
    END

    RETURN    ${resource_paths}

Check Keywords In Resource Files
    [Arguments]    ${resource_paths}    @{keywords_to_check}
    FOR    ${path}    IN    @{resource_paths}
        ${content}=    Get File    ${path}
        FOR    ${keyword}    IN    @{keywords_to_check}
            ${matched}=    Run Keyword And Return Status    Should Match Regexp    ${content}    ${keyword}
            IF    ${matched}
                Log    Keyword ${keyword} found in ${path}
            ELSE
                Log    Keyword ${keyword} not found in ${path}
            END
        END
    END