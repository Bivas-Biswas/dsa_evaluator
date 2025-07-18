import os
import shutil
import argparse

def flatten_with_path_info(source_dir, dest_dir, dry_run=False, verbose=False):
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory {source_dir} does not exist.")
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, source_dir)
            
            # Replace path separators with underscores
            flat_filename = relative_path.replace(os.sep, "_")
            dest_path = os.path.join(dest_dir, flat_filename)

            if verbose:
                print(f"{'[DRY RUN] ' if dry_run else ''}Copying: {full_path} → {dest_path}")

            if not dry_run:
                shutil.copy2(full_path, dest_path)

def main():
    parser = argparse.ArgumentParser(description="Flatten a nested directory structure into a flat one, preserving folder info in filenames.")
    parser.add_argument('--source', '-s', required=True, help="Source directory to flatten")
    parser.add_argument('--dest', '-d', required=True, help="Destination directory to place flat files")
    parser.add_argument('--dry-run', action='store_true', help="Simulate the operation without copying files")
    parser.add_argument('--verbose', '-v', action='store_true', help="Print detailed file operations")

    args = parser.parse_args()

    flatten_with_path_info(
        source_dir=args.source,
        dest_dir=args.dest,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()
