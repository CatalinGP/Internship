def extract_last_words_in_timestamp_range(file_name, start_timestamp, end_timestamp):
    with open(file_name, 'r') as file:
        return [
            parts[-1]
            for line in file
            if (parts := line.split()) and len(parts) > 1 and start_timestamp <= parts[1] <= end_timestamp
        ]

filename = "logcat_applications.txt"
start = "17:56:07.996"
end = "17:56:08.357"
result = extract_last_words_in_timestamp_range(filename, start, end)

print(*result, sep='\n')
