import json
import yaml
import os

def normalize_key(key):
    return key.strip().lower().replace(" ", "_")

def normalize_structure(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            new_key = normalize_key(k)
            new_dict[new_key] = normalize_structure(v)
        return new_dict
    elif isinstance(data, list):
        return [normalize_structure(item) for item in data]
    else:
        return data

def load_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    with open(filename, "r") as f: 
        if ext in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        elif ext == ".json":
            return json.load(f)
        else:
            raise ValueError("Unsupported file type")

def save_json(data, out_filename="mani.json"):
   
    with open(out_filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    filename = "pratice.yaml"  
    raw_data = load_file(filename)
    normal_data = normalize_structure(raw_data)
    print(json.dumps(normal_data, indent=4))
    save_json(normal_data, "mani.json")