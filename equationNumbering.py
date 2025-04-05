# Script to read a file and replace a specific string with another

def replace_in_file(file_path, old_string, new_string):
    try:
        # Read the file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Replace the old string with the new string
        updated_content = content.replace(old_string, new_string)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)
        
        print(f"Replaced '{old_string}' with '{new_string}' in {file_path}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # file_path = input("Enter the file path: ")
    # old_string = input("Enter the string to replace: ")
    # new_string = input("Enter the new string: ")
    replace_in_file('./outputJson.tex', r"\[", r"\begin{equation}")
    replace_in_file('./outputJson.tex', r"\]", r"\end{equation}")

    