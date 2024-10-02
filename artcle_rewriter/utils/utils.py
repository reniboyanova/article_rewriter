import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        prompts_data = json.load(f)
    return prompts_data


def get_api_key(filename):
    try:
        with open(filename, 'r') as file:
            token = file.read().strip()
            if not token:
                raise ValueError("The file is empty!")
            return token
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading token from file: {e}")
