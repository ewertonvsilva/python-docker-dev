from azure.storage.filedatalake import DataLakeServiceClient

def get_folder_size(account_name, account_key, file_system_name, directory_path, max_depth=5, current_depth=1):
    service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=account_key)
    file_system_client = service_client.get_file_system_client(file_system_name)
    directory_client = file_system_client.get_directory_client(directory_path)

    # Initialize total size
    total_size = 0

    # Iterate over files and directories in the current directory
    for item in directory_client.get_paths():
        if item.is_directory:  # If it's a directory, recursively calculate size
            if current_depth < max_depth:
                total_size += get_folder_size(account_name, account_key, file_system_name, item.name, max_depth, current_depth + 1)
        else:
            total_size += item.size  # If it's a file, add its size to the total

    return total_size

# Replace these values with your ADLS account information
account_name = "your_account_name"
account_key = "your_account_key"
file_system_name = "your_file_system_name"
directory_path = "your_directory_path"

# Call the function
total_size = get_folder_size(account_name, account_key, file_system_name, directory_path)

print(f"Total size of folders in '{directory_path}' up to 5 levels deep: {total_size} bytes")
