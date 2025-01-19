import os
def walkDIR(folder_path):
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
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
