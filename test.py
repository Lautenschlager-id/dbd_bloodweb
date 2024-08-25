import os
import shutil

def delete_folders_with_few_subfolders(root_path, min_subfolders):
    for folder_name in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder_name)
        if os.path.isdir(folder_path):
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            if len(subfolders) < min_subfolders:
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}: {subfolders}")

# Example usage
root_path = './result/'
min_subfolders = 5
delete_folders_with_few_subfolders(root_path, min_subfolders)