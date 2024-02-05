import re


def is_numeric(word):
    return bool(re.match(r'^\d+$', word))


def replace_timestamp(log_line):
    words = log_line.split()

    if len(words) >= 2 and (is_numeric(words[-1]) or is_numeric(words[-2])):
        words[0], words[-1] = words[-1], words[0]
        return True, ' '.join(words)
    else:
        return False, log_line


def process_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    changes_made = False

    for line in lines:
        changed, modified_line = replace_timestamp(line)
        if changed:
            print(f"Original: {line.strip()}")
            print(f"Modified: {modified_line.strip()}\n")
            modified_lines.append(modified_line)
            changes_made = True
        else:
            modified_lines.append(line)

    if changes_made:
        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
    else:
        print("No changes were made.")


log_file_path = r"log.txt"
process_log_file(log_file_path)
