import os
filename = "/opt/app/config.py\n"
json_file_path = os.path.join("/cenas", f"{filename}.json")

print(json_file_path)