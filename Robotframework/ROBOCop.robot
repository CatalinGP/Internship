*** Settings ***
Library    OperatingSystem
Library    Collections
Library    String

*** Variables ***
${INPUT_FILE}    ${CURDIR}/ccs2/RELIABILITY/TC_SWQUAL_CCS2_RELIABILITY_B2B_PA.robot

*** Test Cases ***
HLKs Definition Check
    Log Keyword Search Results As Pass Or Fail

*** Keywords ***
Search Resource Paths
    [Arguments]    ${file_path}
    @{resources_list}=    Create List
    ${content}=    Get File    ${file_path}    encoding=UTF-8
    ${lines}=    Split To Lines    ${content}
    FOR    ${line}    IN    @{lines}
        Run Keyword If    '${line}'.startswith('Resource')    Process Resource Line    ${line}    ${resources_list}
    END
    RETURN    ${resources_list}

Process Resource Line
    [Arguments]    ${line}    ${resources_list}
    ${line_segments}=    Split String    ${line}    ${SPACE}
    FOR    ${segment}    IN     @{line_segments}
        ${segment}=    Strip String    ${segment}
        Run Keyword If    '${segment}'.startswith('../')    Add Modified Segment To List    ${segment}    ${resources_list}
    END

Add Modified Segment To List
    [Arguments]    ${segment}    ${resources_list}
    ${modified_segment}=    Replace String    ${segment}    ../    ccs2/
    Append To List    ${resources_list}    ${modified_segment}

Extract HLKs
    ${test_setup_filename}=    Retrieve Test Setup Filename
    ${hlks_dict}=    Get Uppercase Words From Test Setup    ${test_setup_filename}
    RETURN    ${hlks_dict}

Retrieve Test Setup Filename
    ${content}=    Get File    ${INPUT_FILE}    encoding=UTF-8
    ${line}=    Get Lines Containing String    ${content}    Test Setup
    ${filename}=    Get Substring    ${line}    18
    RETURN    ${filename}

Get Uppercase Words From Test Setup
    [Arguments]    ${marker}
    ${content}=    Get File    ${INPUT_FILE}    encoding=UTF-8
    ${lines}=    Split To Lines    ${content}
    ${index}=    Get Index From List    ${lines}    ${marker}
    Run Keyword If    ${index} == -1    Fail    Keyword not found in file
    ${result_lines}=    Create Dictionary
    FOR    ${i}    IN RANGE    ${index + 1}    len(${lines})
        Exit For Loop If    '${lines[${i}]}' == ''
        ${filtered_line}=    Evaluate    ' '.join([word for word in '''${lines[${i}]}'''.split() if word.isupper()])    re
        Run Keyword If    '''${filtered_line}''' != ''    Set To Dictionary    ${result_lines}    ${filtered_line}    FALSE
    END
    RETURN    ${result_lines}

Search Keywords In Files
    [Arguments]    ${file_paths}    ${keywords_dict}
    ${keys}=    Get Dictionary Keys    ${keywords_dict}
    ${updated_dict}=    Create Dictionary
    FOR    ${key}    IN    @{keys}
        Set To Dictionary    ${updated_dict}    ${key}=False
        FOR    ${file_path}    IN    @{file_paths}
            Continue For Loop If    ${updated_dict}[${key}]
            File Should Exist    ${file_path}
            ${content}=    Get File    ${file_path}    encoding=UTF-8
            ${lines}=    Split To Lines    ${content}
            FOR    ${line}    IN    @{lines}
                ${string_line}=    Convert To String    ${line}
                ${found}=    Run Keyword And Return Status    Should Match    ${string_line}    ${key}
                IF    ${found}
                    Set To Dictionary    ${updated_dict}    ${key}=True
                    Exit For Loop
                END
            END
            Exit For Loop If    ${updated_dict}[${key}]
        END
    END
    RETURN    ${updated_dict}

Generate Imposters File
    [Arguments]    ${dictionary}
    ${file_path}=    Set Variable    Imposters.robot
    FOR    ${key}    IN    @{dictionary.keys()}
        ${value}=    Get From Dictionary    ${dictionary}    ${key}
        Run Keyword If    ${value} == ${False}    Write Imposter Entry    ${file_path}    ${key}
    END

Write Imposter Entry
    [Arguments]    ${file_path}    ${key}
    ${content}=    Catenate    SEPARATOR=\n    ${key}    [Arguments] \${foo}\    Keyword not defined, waiting for implementation.\n\n
    Append To File    ${file_path}    ${content}

Log Keyword Search Results As Pass Or Fail
    ${RESOURCE_PATHS_DICT}=    Search Resource Paths    ${INPUT_FILE}
    ${HLKS_DICT}=    Extract HLKs
    ${HLKS_UNDEFINED}=    Search Keywords In Files    ${RESOURCE_PATHS_DICT}    ${HLKS_DICT}
    Generate Imposters File    ${HLKS_UNDEFINED}
    FOR    ${test}    ${result}    IN    &{HLKS_UNDEFINED}
        ${status}=    Set Variable If    '${result}' == 'True'    Passed    Failed
        Log    ${test}: ${status}
    END