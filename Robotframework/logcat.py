import re
from datetime import datetime
import yaml


def parse_log_file(file_path):
    applications_data = []
    start_pattern = re.compile(r"(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*ActivityTaskManager: START.*cmp=([^\s]+)\/")
    end_pattern = re.compile(r"(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*Layer: Destroyed ActivityRecord.* ([a-zA-Z0-9.]+)")

    with open(file_path, 'r') as file:
        log_lines = file.read()

    for line in log_lines.strip().split("\n"):
        start_match = start_pattern.search(line)
        if start_match:
            start_time_str, app_path = start_match.groups()
            applications_data.append({
                "app_path": app_path,
                "ts_app_started": start_time_str,
                "ts_app_closed": None,
                "lifespan": None
            })
        else:
            end_match = end_pattern.search(line)
            if end_match:
                end_time_str, app_path_partial = end_match.groups()
                for app in reversed(applications_data):
                    if app["app_path"].startswith(app_path_partial) and app["ts_app_closed"] is None:
                        app["ts_app_closed"] = end_time_str
                        fmt = "%m-%d %H:%M:%S.%f"
                        start_time = datetime.strptime(app["ts_app_started"], fmt)
                        end_time = datetime.strptime(end_time_str, fmt)
                        lifespan_seconds = (end_time - start_time).total_seconds()
                        app["lifespan"] = f"{lifespan_seconds:.3f}s"
                        break
    return applications_data


def generate_yaml_output(applications_data):
    output_data = {"applications": []}
    for app in applications_data:
        output_data["applications"].append({
            "application": {
                "app_path": app["app_path"],
                "ts_app_started": app["ts_app_started"],
                "ts_app_closed": app["ts_app_closed"],
                "lifespan": app["lifespan"]
            }
        })
    yaml_output = yaml.dump(output_data, sort_keys=False)
    with open("output.yml", "w") as yaml_file:
        yaml.dump(output_data, yaml_file, sort_keys=False)
    return yaml_output


def create_robot_test_file(applications_data):
    robot_test_content = """*** Settings ***
Library    Collections
Library    yaml_reader.py

*** Variables ***
${YAML_FILE}    output.yml

*** Test Cases ***
Application Lifespan Test From YAML
    ${applications}=    Read Yaml File    ${YAML_FILE}
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
"""

    with open("logcat.robot", "w") as robot_file:
        robot_file.write(robot_test_content)

    print("Robot Framework test file has been generated.")


if __name__ == "__main__":
    log_file_path = "logcat_applications.txt"
    applications_data = parse_log_file(log_file_path)
    yaml_output = generate_yaml_output(applications_data)
    create_robot_test_file(applications_data)
    print("YAML output and Robot Framework test file have been generated.")
