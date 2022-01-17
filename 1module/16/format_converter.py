import json
import yaml
import argparse

def openfile(filepath):
    imported_file = None
    filepath_export = None
    with open(filepath, 'r') as f:
        if '.json' or '.yaml' in f:
            file = f.read()
            if file.startswith('{' or '[{'):
                try:
                    imported_file = json.loads(file)
                except Exception as e:
                    print(f'Found errors in JSON:\n{e}')
                filepath_export = filepath[:-4]+'YAML'
            else:
                try:
                    imported_file = yaml.safe_load(file)
                except Exception as e:
                    print(f'Found errors in YAML:\n{e}')
                filepath_export = filepath[:-4]+'JSON'
        else:
            print('File is not a YAML or JSON')
        return imported_file, filepath_export

def savefile(imported_file,filepath_export):
    with open(filepath_export,'w') as f:
        if 'JSON' in filepath_export:
            json.dump(imported_file,f)
        elif 'YAML' in filepath_export:
            yaml.safe_dump(imported_file, f)
        else:
            print('Error on saving')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON YAML converter')
    parser.add_argument('-f', '--file', help='Path to file', required=True)
    args = vars(parser.parse_args())
    filepath = args['file']
    imported_file,filepath_export = openfile(filepath)
    savefile(imported_file,filepath_export)
    print(f'Successfully saved at {filepath_export}')