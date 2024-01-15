def extract_last_words_in_timestamp_range(file_name, start_timestamp, end_timestamp):
    last_words = []

    with open(file_name, 'r') as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue

            timestamp = parts[1]
            if start_timestamp <= timestamp <= end_timestamp:
                last_words.append(parts[-1])

    return last_words

# Example usage
filename = "logcat_applications.txt"
start = "17:56:07.996"
end = "17:56:08.357"
result = extract_last_words_in_timestamp_range(filename, start, end)
print(*result, sep='\n')
