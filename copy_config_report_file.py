import os
import shutil

from util.FileManager import join_path, list_dir

'''
This script is used to copy config.report.csv.done to config.report.csv.
It can't be processed on Linux systems.
'''

def copy_file(folder_path):
    list_bug_dir = list_dir(folder_path)
    for bdir in list_bug_dir:

        parent_path = join_path(folder_path, bdir)

        need_filename = join_path(parent_path, "config.report.csv")
        if os.path.isfile(need_filename):
            pass
        else:
            filename = "config.report.csv.done"
            oldname = join_path(parent_path, filename)
            shutil.copyfile(oldname, need_filename)


folder_path = "D:\\SCU\\code\\SPLC2021_Full_Dataset\\SPLC2021_Full_Dataset\\BuggyVersions\\ExamDB\\dddwise-ExamDB-1BUG-Full"

copy_file(folder_path)