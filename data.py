import os
import json

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
all_media_extensions = image_extensions + video_extensions

output_dir = 'database'
media_dir = 'media'
others_dir = 'others'

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
        image_files_by_folder[subfolder] = images

with open(media_json_path, 'w') as f:
    json.dump({"images": image_files_by_folder}, f, indent=4)

others_json_path = os.path.join(output_dir, 'others.json')
others_dict = {}

if os.path.isdir(others_dir):
    for file in os.listdir(others_dir):
        file_path = os.path.join(others_dir, file)
        name, ext = os.path.splitext(file)
        if os.path.isfile(file_path) and ext.lower() in all_media_extensions:
            key = name
            value = os.path.join('others', file).replace('\\', '/')
            others_dict[key] = value

    with open(others_json_path, 'w') as f:
        json.dump(others_dict, f, indent=4)

notice_json_path = os.path.join(output_dir, 'notice.json')
notices = []
notice_dir = 'notice'

for folder_name in os.listdir(notice_dir):
    folder_path = os.path.join(notice_dir, folder_name)
    if os.path.isdir(folder_path) and '-' in folder_name:
        date_part, title_part = folder_name.split('-', 1)
        formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"
        raw_title = title_part.replace('_', ' ').strip()
        title_lower = raw_title.lower()
        title_title_case = raw_title.title()

        file_entries = []
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lstrip('.').lower()
                relative_path = os.path.join('notice', folder_name, file).replace('\\', '/')
                file_entries.append({
                    "file_name": title_title_case,
                    "file_type": ext,
                    "file_path": relative_path
                })

        if file_entries:
            notice = {
                "date": formatted_date,
                "title": title_lower,
                "files": file_entries
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
