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


def extract_readable_text_from_binary(binary_path: str) -> str:
    """
    Extract readable text from a binary file using multiple techniques and
    filtering.

    Args:
        binary_path: Path to the binary file

    Returns:
        str: Readable text from the binary file, filtered for meaningful content
    """
    # Read the binary file as bytes
    with open(binary_path, "rb") as f:
        binary_data = f.read()

    # Try different approaches to extract text
    text_chunks = []

    # Attempt 1: Try decoding with 'ascii' and ignore errors
    ascii_text = binary_data.decode("ascii", errors="ignore")
    text_chunks.append(ascii_text)

    # Attempt 2: Try decoding with 'utf-16' and ignore errors
    utf16_text = binary_data.decode("utf-16", errors="ignore")
    text_chunks.append(utf16_text)

    # Combine all extracted text
    combined_text = "\n".join(chunk for chunk in text_chunks if chunk.strip())

    # Filter out non-printable characters except for whitespace
    import string
    import re

    # Define what we consider meaningful text
    printable = set(string.printable)

    # First pass: Keep only printable characters
    filtered_text = "".join(char for char in combined_text if char in printable)

    # Second pass: Extract words that look meaningful
    # Look for sequences of 3 or more letters/numbers
    pattern = r"[A-Za-z0-9]{3,}"
    words = re.findall(pattern, filtered_text)

    # Third pass: Filter out common binary patterns
    hex_chars = set("0123456789ABCDEFabcdef")
    meaningful_words = [
        word
        for word in words
        if not all(c in hex_chars for c in word)  # Skip hex-like strings
        and not word.startswith("0x")  # Skip hex numbers
        and not all(c.isdigit() for c in word)  # Skip pure numbers
    ]

    return "\n".join(meaningful_words)
