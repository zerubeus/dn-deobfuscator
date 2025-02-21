import os
import shutil


def extract_file_from_zip(file_path: str, destination_dir: str) -> str:
    """
    Extract files from a .dn2prj file by renaming it to .zip and extracting.

    Args:
        file_path: Path to the .dn2prj file
        destination_dir: Base directory where files should be extracted

    Returns:
        str: Path to the extracted binary file
    """
    # Create the extraction subdirectory
    extract_subdir = os.path.join(destination_dir, "extracted_dn2prj")
    os.makedirs(extract_subdir, exist_ok=True)

    # Get the base name without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create temporary zip file path
    zip_path = os.path.join(destination_dir, f"{base_name}.zip")

    # Copy and rename the .dn2prj to .zip
    shutil.copy2(file_path, zip_path)

    try:
        # Extract the zip file
        import zipfile

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_subdir)

        # Return path to the extracted binary file
        return os.path.join(extract_subdir, base_name)
    finally:
        # Clean up the temporary zip file
        os.remove(zip_path)
