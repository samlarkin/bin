import os

for fn in os.listdir():
    if '.wiki' in fn:
        new_fn = fn[:]
        new_fn = new_fn.replace('.wiki', '')
        new_fn = new_fn.replace('.', '')
        new_fn = new_fn + '.wiki'
        os.replace(fn, new_fn)
