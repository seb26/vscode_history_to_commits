from datetime import datetime
from pathlib import Path
import argparse
import re
import sys

def main(args):
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Aborting, directory does not exist: {directory}")
        sys.exit(1)
    if not directory.name.endswith(".history"):
        # Ideally this can be overridden with a CLI arg like force
        print(f"Aborting, directory is not named `.history`: {directory}")
        sys.exit(1)
    for filepath in directory.rglob("*"):
        if filepath.is_file():
            pattern = r'^(?P<basename>.*)_(?P<date>\d{14})\.(?P<ext>.*)$'
            match = re.match(pattern, filepath.name)
            if match:
                basename, date, ext = ( match.group(attr) for attr in [ 'basename', 'date', 'ext' ] )
                date_git = datetime.strptime(date, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                print(f"{filepath.parent}/{basename}.{ext}", date_git)
            else:
                print(f"Skipping, no match found: {filepath}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='Specify the .history folder')
    args = parser.parse_args()

    main(args)
