import json
import os

with open(os.path.join(os.getcwd(), 'config.json')) as config_file:
    config = json.load(config_file)
