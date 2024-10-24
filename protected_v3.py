import PySimpleGUI as sg
import pyzipper
import os
import threading
import time

# Function to hide or unhide a folder
def set_folder_hidden(folder, hidden):
    if hidden:
        os.system(f'attrib +h "{folder}"')  # Hide the folder
    else:
        os.system(f'attrib -h "{folder}"')  # Unhide the folder

# Function to compress files
def compress_files(filepaths, folder, password, zip_name, compression_level, output_elem):
    zip_filename = os.path.join(folder, f"{zip_name}.zip")
    try:
        with pyzipper.AESZipFile(zip_filename, 'w', compression=compression_level, encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password)
            total_files = len(filepaths)
            for i, filepath in enumerate(filepaths):
                zipf.write(filepath, os.path.basename(filepath))
                progress = (i + 1) / total_files * 100
                output_elem.update(value=f"Compressing... {int(progress)}%")
                time.sleep(0.1)  # Simulate time for compression
            output_elem.update(value="Compression completed with password protection!")
    except Exception as e:
        output_elem.update(value=f"Error: {e}")

# Layout for main menu
menu_layout = [
    [sg.Text("Choose an action:")],
    [sg.Button("Unhide Folder"), sg.Button("Compress Files"), sg.Button("Hide Folder"), sg.Button("Help")],
]

# Create main menu window
menu_window = sg.Window("File Manager", layout=menu_layout)

while True:
    event, values = menu_window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "Unhide Folder":
        folder_path = sg.popup_get_folder("Enter the path of the folder to unhide:")
        if folder_path:
            set_folder_hidden(folder_path, hidden=False)
            sg.popup("The folder has been unhidden.")

    elif event == "Compress Files":
        # Layout for file compression
        compress_layout = [
            [sg.Text("Select files to compress:")],
            [sg.Input(key="files"), sg.FilesBrowse("Choose", file_types=(("All Files", "*.*"),))],
            [sg.Text("Select destination folder:")],
            [sg.Input(key="folder"), sg.FolderBrowse("Choose")],
            [sg.Text("Enter a password:"), sg.Input(password_char="*", key="password")],
            [sg.Text("Enter a name for the ZIP file (without .zip):")],
            [sg.Input(key="zip_name")],
            [sg.Text("Select compression level:")],
            [sg.Combo(["No Compression", "Fast", "Normal", "Maximum"], default_value="Normal", key="compression_level")],
            [sg.Button("Compress File"), sg.Button("Cancel")],
            [sg.Text(key="output")],
        ]

        compress_window = sg.Window("Compress Files", layout=compress_layout)

        while True:
            event, values = compress_window.read()
            if event == sg.WIN_CLOSED or event == "Cancel":
                break
            elif event == "Compress File":
                filepaths = values["files"].split(';')  # Get list of files
                folder = values["folder"]
                password = values["password"].encode()  # Get password and encode it
                zip_name = values["zip_name"]
                compression_level = {
                    "No Compression": pyzipper.ZIP_STORED,
                    "Fast": pyzipper.ZIP_DEFLATED,
                    "Normal": pyzipper.ZIP_LZMA,
                    "Maximum": pyzipper.ZIP_BZIP2,
                }[values["compression_level"]]

                if not filepaths or not folder or not password or not zip_name:
                    compress_window["output"].update(value="Please select files, a destination folder, enter a password, and provide a ZIP name.")
                    continue

                # Confirmation dialog before compression
                confirm = sg.popup_yes_no(f"Are you sure you want to compress the selected files into '{zip_name}.zip'?")
                if confirm == "No":
                    continue

                # Start compression in a separate thread
                output_elem = compress_window["output"]
                threading.Thread(target=compress_files, args=(filepaths, folder, password, zip_name, compression_level, output_elem)).start()

        compress_window.close()

    elif event == "Hide Folder":
        folder_path = sg.popup_get_folder("Enter the path of the folder to hide:")
        if folder_path:
            set_folder_hidden(folder_path, hidden=True)
            sg.popup("The folder has been hidden.")

    elif event == "Help":
        sg.popup("Help Section", "This application allows you to compress files with password protection, hide/unhide folders, and more.")

menu_window.close()
