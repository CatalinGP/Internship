import os

def create_structure(base_path):
    structure = {
        'main': {
            'HEAD': {
                'dev': {
                    'system.d': None,
                    'Opt': {}
                },
                'readme.md': None
            },
            'commit': {
                'commit_fiX': {
                    'commit_fix_FIX': None,
                    'src': {
                        'unit_test.py': None,
                        'app_main': None
                    }
                },
                'variables.txt': None
            }
        }
    }

    def create_dir_file(current_path, structure_dict):
        for name, value in structure_dict.items():
            path = os.path.join(current_path, name)
            if value is None:   # E un fisier
                open(path, 'w').close()
            else:   # E un folder
                os.makedirs(path, exist_ok=True)
                create_dir_file(path, value)

    create_dir_file(base_path, structure)


def rename_files_and_dirs(path):
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            new_name = dir_name[0].upper() + dir_name[1:-1] + dir_name[-1].upper()
            os.rename(os.path.join(root, dir_name), os.path.join(root, new_name))

        for file_name in files:
            if '.' not in file_name:
                new_name = file_name[0].upper() + file_name[1:-1] + file_name[-1].upper()
                os.rename(os.path.join(root, file_name), os.path.join(root, new_name))


base_directory = os.path.dirname(os.path.abspath(__file__))
create_structure(base_directory)
rename_files_and_dirs(base_directory)
