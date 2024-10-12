#!/usr/bin/env python3

from pathlib import Path
import os
import shutil

trash = [
    "~/viminfo",
    "~/.viminfo",
    "~/dotfiles/vim/dot-vim/viminfo",
    "~/dotfiles/vim/dot-vim/.viminfo",
    "~/netrwhist",
    "~/.netrwhist",
    "~/dotfiles/vim/dot-vim/netrwhist",
    "~/dotfiles/vim/dot-vim/.netrwhist",
    "~/.lesshst",
    "~/.python_history"
]


def user_confirm(msg, default="n"):
    """Prompt user for confirmation of file deletion"""
    prompt = "\n".join([msg, "... y/n: "])
    response = input(prompt).strip().lower()
    
    if response not in ("y", "n"):
        response = default

    if response == "y":
        return True

    return False


def cleanup(trash):
    """Clean up unwanted files"""
    rm = []
    for path in trash:
        path = Path(path).expanduser()
        if path.exists():
            rm.append(path)

    if rm == []:
        print("No files to clean up")
        return

    msg = "\n".join(
        ["Are you sure you want to remove the following files:"] +
        [f"... {path}" for path in rm]
    )

    if user_confirm(msg):
        for path in rm:
            print(f"Removing trash: {path}")
            if path.is_file():
                os.remove(path)

            else:
                shutil.rmtree(path)
        print("Cleanup complete")

    else:
        print("Aborting cleanup")


if __name__ == "__main__":
    cleanup(trash)
