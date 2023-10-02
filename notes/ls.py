import sqlite3
import os

def list_files(db_path, folder=None, prefix=None):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Build the SQL query based on folder and prefix criteria
    query = "SELECT path FROM files"
    conditions = []
    parameters = []

    if folder:
        conditions.append("path LIKE ?")
        parameters.append(f"{folder}%")

    if prefix:
        conditions.append("path LIKE ?")
        parameters.append(f"{prefix}%")

    if conditions:
        query += " WHERE " + " OR ".join(conditions)

    # Execute the query and fetch the matching paths
    cursor.execute(query, parameters)
    file_paths = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    # List the matching files and folders
    for path in file_paths:
        print(path)

if __name__ == "__main__":
    database_path = "your_database.db"  # Replace with your SQLite database file path
    folder_filter = "/folder/"  # Replace with the folder you want to filter (e.g., "/folder/")
    prefix_filter = "file"  # Replace with the prefix you want to filter (e.g., "file")

    list_files(database_path, folder=folder_filter, prefix=prefix_filter)


# Set display options
pd.set_option('display.line_number', False)
pd.set_option('display.colheader_justify', 'left')

# Reorder columns
desired_column_order = ['C', 'B', 'A']
df = df[desired_column_order]

# Print the modified DataFrame
print(df)
