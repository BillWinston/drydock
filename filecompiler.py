"""
Script Name: File Compiler and Copier
Description: Recursively searches through nested folders for files with a user-defined 
             extension. Displays the found files and offers the option to copy them 
             into a single destination folder while automatically preventing filename collisions.
Author:      Bill Winston using Gemini
Date:        May 27, 2026
"""

import os
import shutil

def compile_files():
    # 1. Get user inputs
    top_folder = input("Enter the path to the top-level folder: ").strip()
    extension = input("Enter the file extension to look for (e.g., txt, pdf, jpg): ").strip()
    
    # Clean up extension input (remove leading dot if the user included it)
    if extension.startswith('.'):
        extension = extension[1:]
    
    # Validate the source directory
    if not os.path.isdir(top_folder):
        print(f"\nError: The directory '{top_folder}' does not exist.")
        return

    # 2. Search through nested folders
    found_files = []
    print(f"\nSearching for .{extension} files in: {top_folder}...")
    
    for root, dirs, files in os.walk(top_folder):
        for file in files:
            # Case-insensitive check for the extension
            if file.lower().endswith(f".{extension.lower()}"):
                full_path = os.path.join(root, file)
                found_files.append(full_path)

    # 3. Print the identified files
    if not found_files:
        print(f"No .{extension} files found.")
        return
    
    print(f"\nFound {len(found_files)} file(s):")
    for file_path in found_files:
        print(f" - {file_path}")

    # 4. Ask user if they want to copy the files
    print("\n" + "-"*40)
    copy_choice = input("Do you want to copy these files to a new location? (yes/no): ").strip().lower()
    
    if copy_choice in ['yes', 'y']:
        destination_folder = input("Enter the path to the destination folder: ").strip()
        
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            try:
                os.makedirs(destination_folder)
                print(f"Created destination directory: {destination_folder}")
            except Exception as e:
                print(f"Error creating destination folder: {e}")
                return
        
        # Copy files
        print("\nCopying files...")
        copied_count = 0
        for file_path in found_files:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(destination_folder, file_name)
            
            # Handle potential filename collisions in the flat destination folder
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(destination_folder, f"{name}_{counter}{ext}")
                    counter += 1
            
            try:
                shutil.copy2(file_path, dest_path) # shutil.copy2 preserves file metadata
                print(f"Copied: {file_name} -> {dest_path}")
                copied_count += 1
            except Exception as e:
                print(f"Failed to copy {file_name}: {e}")
                
        print(f"\nSuccessfully copied {copied_count} file(s) to '{destination_folder}'.")
    else:
        print("Operation completed. No files were copied.")

if __name__ == "__main__":
    compile_files()
