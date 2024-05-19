import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV and add data to a dictionary
    data = []
    with open(csv_file_path, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    
    # Write data to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Example usage
csv_file_path = 'resource/news/nesw.csv'
json_file_path = 'resource/news/nesw.json'
csv_to_json(csv_file_path, json_file_path)
