import re
import yaml
from datetime import datetime


def parse_log_file(log_file):
    timestamp_pattern = r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'
    app_name_pattern = r'com\.(.*?)(?:/|\})'

    app_data = []
    current_app = None
    app_started_time = None

    with open(log_file, 'r') as file:
        for line in file:
            timestamp_match = re.search(timestamp_pattern, line)
            if timestamp_match:
                timestamp = timestamp_match.group(0)

                app_name_match = re.search(app_name_pattern, line)
                if app_name_match:
                    app_name = app_name_match.group(0)

                    if "START" in line:
                        current_app = app_name
                        app_started_time = timestamp
                    elif "Destroyed" in line and current_app:
                        end_time = timestamp
                        lifespan = calculate_lifespan(app_started_time, end_time)

                        app_data.append({
                            "app_name": current_app,
                            "ts_app_started": app_started_time,
                            "ts_app_closed": end_time,
                            "lifespan": lifespan
                        })
                        current_app = None

    return app_data


def calculate_lifespan(start_time, end_time):
    start_timestamp = parse_timestamp(start_time)
    end_timestamp = parse_timestamp(end_time)
    lifespan = (end_timestamp - start_timestamp).total_seconds()
    return f"{lifespan:.3f}s"


def parse_timestamp(timestamp_str):
    timestamp_format = "%m-%d %H:%M:%S.%f"
    return datetime.strptime(timestamp_str, timestamp_format)


def generate_output_yaml(app_data, output_file):
    with open(output_file, 'w') as file:
        yaml.dump({"applications": app_data}, file, default_flow_style=False)


if __name__ == "__main__":
    log_file = "logcat_applications.txt"
    output_file = "output.yml"
    app_data = parse_log_file(log_file)
    generate_output_yaml(app_data, output_file)
