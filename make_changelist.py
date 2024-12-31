# !! hoffor did NOT write this (mostly)
# this is ChatGPT generated but i included it here since it's what i use as a 1-click generator for the data for each commit
# place this in your BepInEx folder and execute it there. the output folder will be created for you in the same directory

import os
import json
import shutil
import zlib
from datetime import datetime

def get_version_or_hash(folder_path):
    # Check if manifest.json.old exists
    manifest_old_path = os.path.join(folder_path, 'manifest.json.old')
    if os.path.exists(manifest_old_path):
        with open(manifest_old_path, 'rb') as manifest_file:
            content = manifest_file.read()

            # Detect and remove UTF-8 BOM if present
            if content.startswith(b'\xef\xbb\xbf'):
                content = content[3:]

            manifest_data = json.loads(content.decode('utf-8'))
            version_number = manifest_data.get('version_number', '').strip()
            if version_number:
                return f'{version_number}_DISABLED'

    # Check if manifest.json exists
    manifest_path = os.path.join(folder_path, 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'rb') as manifest_file:
            content = manifest_file.read()

            # Detect and remove UTF-8 BOM if present
            if content.startswith(b'\xef\xbb\xbf'):
                content = content[3:]

            manifest_data = json.loads(content.decode('utf-8'))
            version_number = manifest_data.get('version_number', '').strip()
            if version_number:  # If version_number is not empty
                return version_number

    # If neither manifest.json.old nor valid manifest.json is present, generate CRC32 hash
    crc_value = 0
    for root, dirs, files in os.walk(folder_path):
        for filename in sorted(files):  # Sort to ensure consistent hash
            filepath = os.path.join(root, filename)
            with open(filepath, 'rb') as f:
                while True:
                    buffer = f.read(4096)
                    if not buffer:
                        break
                    crc_value = zlib.crc32(buffer, crc_value)
    hex = format(crc_value & 0xFFFFFFFF, '08x')  # Convert to 8-digit hexadecimal
    return f'CRC32-{hex}'

# Get current datetime in the specified format
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S%f')[:-3]

# Define paths
destination_dir = f'changelist_{timestamp}'
source_plugins_dir = 'plugins'
source_config_dir = 'config'
destination_config_dir = os.path.join(destination_dir, source_config_dir)

# Copy the entire config directory
shutil.copytree(source_config_dir, destination_config_dir)

# Path for the output .txt file
output_file_path = os.path.join(destination_dir, 'plugins_version_list.txt')

# Open the .txt file to write the folder names and their versions
with open(output_file_path, 'w') as output_file:
    # Process each folder within 'plugins' (non-recursive)
    for folder_name in os.listdir(source_plugins_dir):
        folder_path = os.path.join(source_plugins_dir, folder_name)
        if os.path.isdir(folder_path):
            version_or_hash = get_version_or_hash(folder_path)
            # Write the folder name and version to the file
            output_file.write(f'{folder_name}_{version_or_hash}\n')

print(f'Created {output_file_path} with versioned folder names.')
