import os

file_path = 'users.json'

# Read the file with the correct encoding to ignore the BOM
with open(file_path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Overwrite the file with standard UTF-8 encoding (no BOM)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"BOM removed from {file_path}")