import re
import os
import gzip

log_dir = r"<YOUR-LOG-FILE-ADDRESS #EXAMPLE: C:\Users\admin\Desktop\Minecraft server\logs>"
output_file = r"<OUTPUT-FILE-LOCATION-ADDRESS #EXAMPLE: C:\Users\admin\Desktop\whitelist_violations.txt>"

def check_log_file(log_dir):
    pattern = r"\[\d{2}[A-Za-z]{3}\d{4} \d{2}:\d{2}:\d{2}\.\d{3}\] \[Server thread/INFO\] (?:\[.*\])?: Disconnecting .*: You are not white-listed on this server!"
    results = []
    
    # Iterate over all files in the log directory
    for file_name in os.listdir(log_dir):
        file_path = os.path.join(log_dir, file_name)
        
        # Ensure we're only reading files, not directories
        if os.path.isfile(file_path):
            if file_name.endswith('.gz'):
                with gzip.open(file_path, 'rt', errors='ignore') as file:
                    try:
                        content = file.read()
                        matches = re.findall(pattern, content)
                        results.extend(matches)
                    except UnicodeDecodeError:
                        print(f"Could not read {file_path} due to encoding error.")
            else:
                with open(file_path, 'r', errors='ignore') as file:
                    try:
                        content = file.read()
                        matches = re.findall(pattern, content)
                        results.extend(matches)
                    except UnicodeDecodeError:
                        print(f"Could not read {file_path} due to encoding error.")
    
    return results

def save_results_to_file(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for result in results:
            file.write(result + '\n')

# Get the matched patterns
result = check_log_file(log_dir)

# Save the results to a file
save_results_to_file(result, output_file)

# Print the results to the console
for line in result:
    print(line)
