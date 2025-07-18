import os
import shutil
import subprocess

def create_test_structure(base_dir):
    """Create a nested folder structure with test files."""
    nested_paths = [
        "a/foo.txt",
        "b/c/bar.txt",
        "b/d/baz.txt",
        "e/f/g/qux.txt"
    ]
    
    for path in nested_paths:
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(f"Contents of {path}")

def clean_up(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

def list_files_flat(dest_dir):
    return sorted(os.listdir(dest_dir))

def main():
    source_dir = "test_source"
    dest_dir = "test_dest"

    # Clean up before and after
    clean_up(source_dir)
    clean_up(dest_dir)

    # Step 1: Create source directory
    os.makedirs(source_dir, exist_ok=True)
    create_test_structure(source_dir)

    # Step 2: Run flatten.py
    cmd = ["python3", "flatten.py", "-s", source_dir, "-d", dest_dir, "-v"]
    subprocess.run(cmd, check=True)

    # Step 3: Verify output
    print("\nFlattened files in dest_dir:")
    flat_files = list_files_flat(dest_dir)
    for file in flat_files:
        print(file)

    expected = sorted([
        "a_foo.txt",
        "b_c_bar.txt",
        "b_d_baz.txt",
        "e_f_g_qux.txt"
    ])

    assert flat_files == expected, "Test failed: Output files don't match expected"

    print("\n✅ Test passed!")

    # Optional: clean up
    # clean_up(source_dir)
    # clean_up(dest_dir)

if __name__ == "__main__":
    main()
