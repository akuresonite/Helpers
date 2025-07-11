import os
def walkDIR(folder_path, include=None):
    r"""
    Lists all files in the given folder, including those in subfolders. 
    Optionally filters files by extensions.
    Parameters:
        folder_path (str): The path to the folder to search.
        include (list of str, optional): A list of file extensions to include (e.g., ['.txt', '.jpg']).
                                         If None, all files are included.
    Returns:
        list: A list of full file paths that match the criteria.
    Example:
        datadir = "path_to_your_folder"
        files = walkDIR(datadir, include=['.png', '.jpeg', '.jpg'])
    """
    
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if include is None or any(file.endswith(ext) for ext in include):
                file_list.append(os.path.join(root, file))
    print("Files found:", len(file_list))
    return file_list



import os, shutil
def copy_files_from_folders(name, source_folders, destination_folder):
    r'''
    Copies files from multiple source folders to a destination folder, 
    renaming them based on the source folder type.
    Parameters:
        name (str): The name to be appended to the destination folder.
        source_folders (list): A list of paths to the source folders.
        destination_folder (str): The path to the destination folder.
    Returns:
        None
    The function creates a new folder inside the destination folder with 
    the given name. It then iterates through each file in the source 
    folders, renaming them based on the folder type ('story', 'highligits', or 'post') 
    and copying them to the destination folder. If a file with the same name 
    already exists in the destination folder, it is added to a list of duplicate 
    files, which is printed at the end along with the total number of files copied.
    Example:
        name = 'Folder1'
        source_folders = srcdir
        destination_folder = dstdir
        copy_files_from_folders(name, source_folders, destination_folder)
    '''
  
    destination_folder = os.path.join(destination_folder, name)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
    total_files = 0
    duplicate_files = []
    
    for source_folder in source_folders:
        print(source_folder)            
        for file_name in tqdm(os.listdir(source_folder)):
            
            if 'story' in source_folder:
                if 'highligits' in source_folder:
                    destination_file_name = ''.join(file_name.split('.')[:-1] + ['highligits']) + '.' + file_name.split('.')[-1]            
                else:
                    destination_file_name = ''.join(file_name.split('.')[:-1] + ['story']) + '.' + file_name.split('.')[-1]
            else:
                destination_file_name = ''.join(file_name.split('.')[:-1] + ['post']) + '.' + file_name.split('.')[-1]
              
                
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, destination_file_name)
            if os.path.isfile(source_file_path):
                if os.path.isfile(destination_file_path):
                    duplicate_files.append(destination_file_path)
                else:
                    shutil.copy(source_file_path, destination_file_path)
                    total_files += 1

    print(f'Total {total_files} files copies')
    for i in duplicate_files:
        print(i)


def rename_folder(old_name, new_name):
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"Renamed: '{old_name}' → '{new_name}'")
    else:
        print(f"Folder '{old_name}' does not exist.")
        
for old_name, new_name in zip(old_names, new_names):        
    rename_folder(old_name, new_name)



def replace_line_in_file(filepath, target_line, new_line):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    with open(filepath, 'w') as f:
        for line in lines:
            if line.strip() == target_line.strip():
                indent = len(line) - len(line.lstrip())
                f.write(' ' * indent + new_line + '\n')
            else:
                f.write(line)


replace_line_in_file(
    "/scratch/23m1521/miniconda/lib/python3.12/site-packages/ignite/handlers/tqdm_logger.py", 
    "from tqdm.autonotebook import tqdm", 
    "from tqdm import tqdm, trange"
)


import os
import importlib.util
def import_objects_from_path(file_path, object_names):
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Cannot find spec for {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Support both single string and list of names
    if isinstance(object_names, str):
        object_names = [object_names]
    
    objects = {name: getattr(module, name) for name in object_names}
    return objects
