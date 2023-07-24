import shutil
import json
import errno
import os
import argparse


def copy_item(source, destination, permissions, mode):
    if os.path.isfile(source):
        # If the source is a file, use copy_file
        copy_file(source, destination, permissions, mode)
        return "File"
    elif os.path.isdir(source):
        # If the source is a directory, use copy_tree
        #copy_tree(source, destination,  permissions, mode)
        return "Folders are not supported"
    
    return "Invalid source path"
    

def copy_file(source, destination, permissions, mode):

    if os.path.exists(destination) and os.path.isfile(destination) and mode=="install":
        dest_permissions = os.stat(destination).st_mode
        with open(source, 'rb') as source_file:
            content = source_file.read()
        with open(destination, 'wb') as dest_file:
            dest_file.write(content)
        os.chmod(destination, dest_permissions)

    else:
        try:
            shutil.copy2(source, destination)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
            # try creating parent directories
            os.makedirs(os.path.dirname(destination))
            shutil.copy2(source, destination)
    
    if permissions is not None and mode=="install":
        os.chmod(destination, int(permissions, base=8))
    


# def copy_tree(source, destination,  permissions, mode):
#     try:
#         shutil.rmtree(destination)  # Remove the destination folder if it exists
#     except OSError:
#         pass  # Ignore errors if the destination folder doesn't exist

#     shutil.copytree(source, destination)

def print_pretty_table(data):
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

    print('-' * 30)
    for row in data:
        for i, item in enumerate(row):
            print(str(item).ljust(col_widths[i] + 2), end="")
        print()
    print('-' * 30)



def main():
    parser = argparse.ArgumentParser(description='Script used to support installation procedure')

    parser.add_argument('--instructions', help='json file with files instructions', required=True)
    parser.add_argument('--backup', action='store_true', help='Make a backup from instructions')
    parser.add_argument('--install', action='store_true', help='Make instructions installation')
    parser.add_argument('--rollback', action='store_true', help='Make rollback from previous created backup')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed options and values
    with open(args.instructions) as f:
        instructions = json.load(f)


    if args.backup:
        backup_folder = instructions['backup_folder']
        data = []
        mode = "backup"
        print("# Backup")

        for manipulation in instructions['release']:
            source = manipulation['destination']
            permissions = manipulation.get('permissions', None)
            status=""
            type=""

            try:
                type = copy_item(source,backup_folder +"/"+source, permissions, mode)
                status = "Success" if type != "Invalid source path" else "Skipped"
            except Exception as e:
                status = repr(e)
            
            new_row = ["Backup", source, backup_folder +"/"+source, type, status]
            data.append(new_row)
        print_pretty_table(data)

    if args.install:
        data = []
        mode = "install"
        print("# Installation")

        for manipulation in instructions['release']:
            source = manipulation['source']
            destination =  manipulation['destination']
            permissions = manipulation.get('permissions', None)
            status=""
            type=""

            try:
                type = copy_item(source,destination, permissions, mode)
                status = "Success"
            except Exception as e:
                status = repr(e)

            new_row = ["Installation", source, destination, type, status]
            data.append(new_row)
        print_pretty_table(data)
    if args.rollback:
        print('Flag is set.')


if __name__ == '__main__':
    main()
