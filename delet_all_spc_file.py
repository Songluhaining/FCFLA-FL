import os

'''
This script is used to delete the slicing_10.log file from each bug_ID
'''
def delete_spc_file(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for dirs_s in dirs:
            parent_path = os.path.join(root, dirs_s)
            for root_ss, dirs_ss, files_ss in os.walk(parent_path):
                for file in files_ss:
                    if file == "slicing_10.log": #spc_10.log
                        file_path = os.path.join(root_ss, file)
                        os.remove(file_path)

folder_path = "/home/whn/Desktop/BankAccountTP/4wise-BankAccountTP-1BUG-Full"

delete_spc_file(folder_path)