import re

with open("resource/law/law_clean_list.txt", "r", encoding="utf-8") as file:
    content = file.readlines()

for i, line in enumerate(content):
    content[i] = re.sub(r'مصوب.*', '', line)
    content[i] = re.sub(r'سال \d{4}', '', content[i])

lines_seen = set()
for  line in content:
    if line not in lines_seen: 
        lines_seen.add(line)

with open("resource/law/law_clean_list.txt", "w" , encoding="utf-8") as file:
    file.writelines(lines_seen)

