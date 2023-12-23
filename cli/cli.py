import argparse
import os
import click_spinner
import time
import shutil

TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "template")


def copy_template_files(destination_folder):
    """
    Copy template files to the destination folder.
    """
    for root, dirs, files in os.walk(TEMPLATE_FOLDER):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(
                destination_folder, os.path.relpath(src_file, TEMPLATE_FOLDER)
            )
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy(src_file, dest_file)


def init_project(project_name: str):
    """
    Initialize a new FastAPI project
    """
    # Create project folder
    project_folder = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_folder, exist_ok=True)

    copy_template_files(project_folder)


def init(args):
    """
    Initialize FastAPI Utilities CLI
    """
    print("Welcome to FastAPI Utilities CLI Tool")

    project_name = input("Enter the project name: ")

    with click_spinner.spinner(f"Creating project '{project_name}'..."):
        init_project(project_name)
        time.sleep(1)

    print("Project created successfully")


def main():
    """
    Main function for FastAPI Utilities CLI Tool
    """
    parser = argparse.ArgumentParser(description="FastAPI Utilities CLI Tool")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Create 'init' subcommand
    parser_init = subparsers.add_parser("init", help="Initialize FastAPI Utilities CLI")
    parser_init.set_defaults(func=init)

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == "__main__":
    main()
