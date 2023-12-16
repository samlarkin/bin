#!/usr/bin/env python
import os


def main(input_dir):
    """Resize a batch of image using system call to ImageMagick"""
    original_names = os.listdir(input_dir)
    names = gen_dict(original_names)
    resize(input_dir, names, xlim=250, ylim=250)


def gen_dict(original_names):
    """Generates a dict mapping from original image names to small
    (modified) image names

    """
    names = {}
    for name in original_names:
        _, ext = os.path.splitext(name)
        small_name = "".join([name, ".small", ext])
        names.update({name: small_name})
    return names


def resize(input_dir, names, xlim, ylim):
    """Call ImageMagick to resize images"""
    for original_name, small_name in names.items():
        cmd = f"convert {input_dir}/{original_name} \
                -resize {xlim}x{ylim}\> \
                {input_dir}/{small_name}"
        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    main("./")
