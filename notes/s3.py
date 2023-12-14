import boto3

def list_s3_paths(bucket_name, prefix=''):
    """
    List paths in an S3 bucket.

    Parameters:
        - bucket_name (str): The name of the S3 bucket.
        - prefix (str, optional): The prefix to filter paths. Defaults to an empty string.

    Returns:
        - List of paths (str) in the specified S3 bucket and prefix.
    """
    s3 = boto3.client('s3')

    # Use the list_objects_v2 method to get a list of objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Extract paths from the response
    paths = [obj['Key'] for obj in response.get('Contents', [])]

    return paths

# Replace 'your_bucket_name' with the actual name of your S3 bucket
bucket_name = 'your_bucket_name'

# Replace 'your_prefix' with the prefix you want to list (optional, defaults to an empty string)
prefix = 'your_prefix'

# Get the list of paths in the S3 bucket
s3_paths = list_s3_paths(bucket_name, prefix)

# Print the list of paths
for path in s3_paths:
    print(path)
