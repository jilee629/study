import tomllib
import json
from pathlib import Path

# load()는 파일을 인수로 받는다.
toml_file = Path(__file__).parent / 't_toml.toml'
with open(toml_file, 'rb') as f:
    toml_data = tomllib.load(f)
    id2 = toml_data['site2']['username']
    print(id2)

# json
json_file = Path(__file__).parent / 't_json.json'
with open(json_file) as f:
    json_data = json.loads(f.read())
    id3 = json_data['site2']['username']
    print(id3)
    id4 = json_data.get('site2').get('username')
    print(id4)
