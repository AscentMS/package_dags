"""\
Package airflow dags into a zipfile suitable for deployment.


Worflows are added to the root of the zip, while additional directories
have their path preserved
"""
import zipfile
import pathlib
import shutil


def cli():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "-o", "--output-file", help="Path to zipfile to create", default="dist/dags.zip"
    )
    parser.add_argument(
        "-w",
        "--workflow-directory",
        help="Path to the workflows to package",
        default="workflows",
    )
    parser.add_argument(
        "-a",
        "--additional-directory",
        help="Additional folders to add",
        action="append",
        default=[],
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose and list out files added?",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    if args.verbose:

        def print_message(*args, **kwargs):
            print(*args, **kwargs)

    else:

        def print_message(*args, **kwargs):
            pass

    create_zip(
        output_file=args.output_file,
        workflow_directory=args.workflow_directory,
        additional_directories=args.additional_directory,
        print=print_message,
    )


def create_zip(
    output_file: str,
    workflow_directory: str = "workflows",
    additional_directories: list[str] = [],
    print=print,
):
    base = pathlib.Path(".")
    workflows = pathlib.Path(workflow_directory)

    if not workflows.is_absolute():
        workflows = base / workflows

    add_dirs = []
    for directory in additional_directories:
        directory = pathlib.Path(directory)

        if not directory.is_absolute():
            directory = base / directory
        else:
            raise RuntimeError("Additional directories must be relative paths")
        add_dirs.append(directory)

    with zipfile.ZipFile(
        output_file,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zip:
        for path_object in sorted(workflows.rglob("*")):
            if path_object.match("*/__pycache__/*"):
                continue

            new_path = path_object.relative_to(workflows)

            if path_object.is_file():
                print(f"Adding {path_object} -> {new_path}")
                with open(path_object, "rb") as f, zip.open(str(new_path), "w") as z:
                    shutil.copyfileobj(f, z)

        for path in add_dirs:
            for path_object in sorted(path.rglob("*")):
                if path_object.match("*/__pycache__/*"):
                    continue

                new_path = path_object.relative_to(base)

                if path_object.is_file():
                    print(f"Adding {path_object} -> {new_path}")
                    with open(path_object, "rb") as f, zip.open(
                        str(new_path), "w"
                    ) as z:
                        shutil.copyfileobj(f, z)


if __name__ == "__main__":
    cli()
