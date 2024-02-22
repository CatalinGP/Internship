import yaml

class YamlReader:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def read_yaml_file(self, file_path):
        with open(file_path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as error:
                print(error)
                return None
