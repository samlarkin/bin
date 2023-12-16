#!/usr/bin/env python3

import os
import sys
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError

# The on-launch event is triggered once, after initialization, before
# any processing occurs. This hooks script has no effect on processing.

# Input:
# - None

# Output:
# - Optional feedback/error.

HOME = os.environ.get('HOME', '/home/sam')
task_src = os.path.join(HOME, '.task')
task_dst = os.path.join(HOME, 'bak/task')
time_src = os.path.join(HOME, '.timewarrior')
time_dst = os.path.join(HOME, 'bak/timewarrior')
status = 0


def backup_dir(src, dst):
    """Backup src directory to dst directory.

    Write feedback to sys.stderr. Exit with status 1 in case of error.
    """
    feedback = f'backing up data from {src} ... to ... {dst}'
    try:
        copy_tree(src, dst)
        status = 0
    except DistutilsFileError:
        feedback = 'A DistutilsFileError occurred whilst backing up \
                   data from ... {src} ... to ... {dst}. Check the \
                   script at ~/.task/hooks/on-launch.backup.py'
        status = 1
    sys.stderr.write(''.join([feedback, '\n']))
    if status == 1:
        sys.exit(status)
    return


backup_dir(task_src, task_dst)
backup_dir(time_src, time_dst)

# Status:
# - 0:     JSON ignored, non-JSON is feedback.
# - non-0: JSON ignored, non-JSON is error.

sys.exit(status)
