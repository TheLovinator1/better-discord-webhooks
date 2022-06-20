import os
import subprocess
import tempfile
from typing import List


def write_file(string: str):
    # Create a temporary file for the first string
    file = tempfile.NamedTemporaryFile(
        mode="wt",
        encoding="utf-8",
        suffix=".txt",
        delete=False,
    )

    # Write the first string to the file
    file.write(string)

    # Save what we wrote to the file
    file.flush()

    return file


def get_diff(string1: str, string2: str):
    file1 = write_file(string1)
    file2 = write_file(string2)

    cmd: List[str] = [
        "git",
        "diff",
        "--unified=0",
        "--word-diff=color",
        "--no-index",
        f"{file1.name}",
        f"{file2.name}",
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        check=False,  # Diff exits with 1 if there is difference
    )

    # Close and remove the temporary files
    file1.close()
    file2.close()
    os.remove(file1.name)
    os.remove(file2.name)

    # stdout is bytes, so we need decode it to a normal string
    result_str = result.stdout.decode("utf-8")

    # Split the string into lines
    lines = result_str.split("\n")
    # Remove first 5 lines
    lines = lines[5:]
    # Convert list to string with newlines
    final_result = "\n".join(lines)

    return f"```ansi\n{final_result}\n```"


if __name__ == "__main__":
    ONE = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has"  # noqa, pylint: disable=line-too-long
    TWO = "Lorem Ipsum is simply dummy printing of the printing and typesetting industry. Lorem Ipsum has been the industry's dummy dummy text ever since the 1500s, when an unknown and took a galley of type and  it has to make a type specimen book. It scrambled"  # noqa, pylint: disable=line-too-long

    print(repr(get_diff(ONE, TWO)))
    print(get_diff(ONE, TWO))
