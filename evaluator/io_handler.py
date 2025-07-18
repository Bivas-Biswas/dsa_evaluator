import shutil
import os

def prepare_file_io(input_path, expected_input_name):
    shutil.copy(input_path, expected_input_name)

def read_output_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()
