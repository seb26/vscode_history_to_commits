from datetime import datetime
from pathlib import Path
import argparse
import os
import re
import subprocess
import shutil
import sys

def git(*git_args, **subprocess_options):
    proc = subprocess.run(
        [ 'git', *git_args ],
        **subprocess_options,
    )
    return proc

def main(args):
    dir_history = Path(args.dir_history)
    dir_working = Path(args.dir_working)
    if not dir_history.exists():
        print(f"Aborting, directory does not exist: {dir_history}")
        sys.exit(1)
    if not dir_history.name.endswith(".history"):
        # Ideally this can be overridden with a CLI arg like force
        print(f"Aborting, directory is not named `.history`: {dir_history}")
        sys.exit(1)
    if not dir_working.exists():
        print(f"Aborting, working directory does not exist: {dir_working}")
        print("Check the directory path is correct, or create the directory and initialise a Git repo inside it first.")
        sys.exit(1)
    for filepath in sorted(dir_history.rglob("*")):
        if filepath.is_file():
            pattern = r'^(?P<basename>.*)_(?P<date>\d{14})\.(?P<ext>.*)$'
            match = re.match(pattern, filepath.name)
            if match:
                basename, date, ext = ( match.group(attr) for attr in [ 'basename', 'date', 'ext' ] )
                date_git = datetime.strptime(date, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                print(f"Working on: {filepath.parent}/{basename}.{ext}", date_git)
                # Establish the filepaths
                filename = Path(basename + "." + ext)
                working_filepath = Path( filepath.parent / filename ).relative_to(dir_history)
                working_filepath_phy = Path( dir_working / working_filepath )
                # Write the file to working directory
                os.makedirs(working_filepath_phy.parent, exist_ok=True)
                print(f"Copying {filename} ({date_git}) to: {working_filepath_phy}")
                shutil.copy(filepath, working_filepath_phy)
                # git add
                git(
                    'add',
                    working_filepath,
                    cwd=dir_working,
                )
                # commit interactively
                git (
                    'commit',
                    '-v',
                    "--date",
                    date_git,
                    cwd=dir_working,
                )
            else:
                print(f"Skipping, no match found: {filepath}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir_history', type=str, help='Specify the .history folder')
    parser.add_argument('dir_working', type=str, help='Specify the target working directory (which contains a git repo)')
    args = parser.parse_args()

    main(args)
