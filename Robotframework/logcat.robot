*** Settings ***
Library    Collections
Library    yaml_reader.py

*** Variables ***
${YAML_FILE}    output.yml

*** Test Cases ***
Application Lifespan Test From YAML
    ${applications}=    Read Yaml File    ${CURDIR}/${YAML_FILE}
    ${total_apps}=    Get Length    ${applications['applications']}
    ${count}=    Set Variable    0
    @{warning_apps}=    Create List
    FOR    ${app}    IN    @{applications['applications']}
        ${lifespan}=    Convert To Number    ${app['application']['lifespan'][:-1]}
        Run Keyword If    ${lifespan} < 30
        ...    Set Variable    ${count + 1}
        ...    ELSE    Append To List    ${warning_apps}    ${app['application']['app_path']}
    END
    ${passed_threshold}=    Evaluate    ${total_apps} * 0.75
    Run Keyword If    ${count} >= ${passed_threshold}
    ...    Log    Test PASSED. More than 75% of apps have a lifespan less than 30s.
    ...    ELSE    Fail    Test FAILED. Applications with lifespan over 30s: @{warning_apps}
