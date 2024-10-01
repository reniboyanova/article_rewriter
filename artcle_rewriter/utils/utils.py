import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        prompts_data = json.load(f)
    return prompts_data['prompts']
