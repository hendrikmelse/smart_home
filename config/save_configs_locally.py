# Run this to copy network information to /etc/smart_home/config/

import os
import shutil

config_path = "/etc/smart_home/config/"
if not os.path.exists(config_path):
    os.makedirs(config_path)

for filename in ("devices.yaml", "managers.yaml"):
    shutil.copyfile(os.path.join(os.path.dirname(__file__), filename), os.path.join(config_path, filename))