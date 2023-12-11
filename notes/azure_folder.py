from azure.storage.filedatalake import DataLakeServiceClient

def get_folder_size_and_write(account_name, account_key, container_name, directory_path, output_file, max_depth=5, current_depth=1):
    service_client = DataLakeServiceClient(account_url=f"https://{account_name}.dfs.core.windows.net", credential=account_key)
    file_system_client = service_client.get_file_system_client(container_name)
    directory_client = file_system_client.get_directory_client(directory_path)

    # Open the output file in append mode
    with open(output_file, 'a') as file:
        # Initialize continuation token
        continuation_token = None

        while True:
            # Get a page of paths in the current directory
            paths = directory_client.get_paths(continuation_token=continuation_token)

            for item in paths:
                if not item.is_directory:
                    file.write(f"{item.name}: {item.size} bytes\n")

            # Recursively iterate over subdirectories
            if current_depth < max_depth:
                for subdirectory in directory_client.get_subdirectories():
                    get_folder_size_and_write(account_name, account_key, container_name, subdirectory.name, output_file, max_depth, current_depth + 1)

            # Check if there are more paths to retrieve
            continuation_token = paths.continuation_token
            if not continuation_token:
                break

# Replace these values with your ADLS Gen2 account information
account_name = "your_account_name"
account_key = "your_account_key"
container_name = "your_container_name"  # Replace with the actual container name
directory_path = "your_directory_path"  # Replace with the actual directory path within the container
output_file = "output.txt"  # Replace with the desired output file path

# Call the function
get_folder_size_and_write(account_name, account_key, container_name, directory_path, output_file)

print(f"Results written to {output_file}")
