import os
import json

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
output_dir = 'database'
media_dir = 'media'
notice_dir = 'notice'

os.makedirs(output_dir, exist_ok=True)

media_json_path = os.path.join(output_dir, 'media.json')
image_files_by_folder = {}

for subfolder in os.listdir(media_dir):
    subfolder_path = os.path.join(media_dir, subfolder)
    if os.path.isdir(subfolder_path):
        images = []
        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)
            if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                relative_path = os.path.join(media_dir, subfolder, file).replace('\\', '/')
                images.append(relative_path)
        image_files_by_folder[subfolder] = images  # even if empty list

with open(media_json_path, 'w') as f:
    json.dump({"images": image_files_by_folder}, f, indent=4)

notice_json_path = os.path.join(output_dir, 'notice.json')
notices = []

for folder_name in os.listdir(notice_dir):
    folder_path = os.path.join(notice_dir, folder_name)
    if os.path.isdir(folder_path) and '-' in folder_name:
        date_part, title_part = folder_name.split('-', 1)
        title = title_part.replace('_', ' ').strip().capitalize()
        unique_id = title.replace(' ', '-').lower()
        files = []
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                files.append(file_path.replace('\\', '/'))
        notice = {
            "id": unique_id,
            "date": date_part,
            "title": title,
            "files": files
        }
        notices.append(notice)

with open(notice_json_path, 'w', encoding='utf-8') as f:
    json.dump({"notices": notices}, f, indent=4)

version_file = os.path.join(output_dir, 'version.json')

if os.path.exists(version_file):
    with open(version_file, 'r') as vf:
        version_data = json.load(vf)
    version = version_data.get("version", 0) + 1
else:
    version = 0

with open(version_file, 'w') as vf:
    json.dump({"version": version}, vf, indent=4)

os.system("git add .")
os.system(f'git commit -m "{version}"')
os.system("git push")

