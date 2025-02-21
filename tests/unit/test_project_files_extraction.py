import os
import shutil
import json
import pytest

from dn_deobfuscator.app import extract_file_from_zip, extract_readable_text_from_binary

# Path to the test data directory containing the actual AUTOMATIC.dn2prj file
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SAMPLE_FILE = os.path.join(TEST_DATA_DIR, "AUTOMATIC.dn2prj")


def get_test_data_dir_path():
    expected_extract_dir = os.path.join(TEST_DATA_DIR, "extracted_dn2prj")
    expected_binary_path = os.path.join(expected_extract_dir, "AUTOMATIC")

    return expected_extract_dir, expected_binary_path


@pytest.fixture
def cleanup_extracted():
    """Cleanup the extracted directory after test"""
    yield

    # Cleanup extracted directory and temporary zip
    extracted_dir = os.path.join(TEST_DATA_DIR, "extracted_dn2prj")
    if os.path.exists(extracted_dir):
        shutil.rmtree(extracted_dir)

    temp_zip = os.path.join(TEST_DATA_DIR, "AUTOMATIC.zip")
    if os.path.exists(temp_zip):
        os.remove(temp_zip)


def test_unzip_dn2prj_file(cleanup_extracted):
    """Test that we can extract files from a .dn2prj file just like the manual
    process:
    mv AUTOMATIC.dn2prj AUTOMATIC.zip
    unzip AUTOMATIC.zip -d extracted_dn2prj
    """
    # Arrange
    expected_extract_dir, expected_binary_path = get_test_data_dir_path()

    # Act
    extracted_file_path = extract_file_from_zip(
        file_path=SAMPLE_FILE, destination_dir=TEST_DATA_DIR
    )

    # Assert
    assert extracted_file_path == expected_binary_path
    assert os.path.exists(extracted_file_path)

    # Verify manifest.json exists and log its contents
    manifest_path = os.path.join(expected_extract_dir, "manifest.json")
    assert os.path.exists(manifest_path)

    with open(manifest_path) as f:
        manifest_content = json.load(f)
        print("\nmanifest.json contents:")
        print(json.dumps(manifest_content, indent=2))

    # Verify the temporary zip file was cleaned up
    assert not os.path.exists(os.path.join(TEST_DATA_DIR, "AUTOMATIC.zip"))


def test_extract_readable_text_from_binary():
    """Test that we can extract readable text from a binary file"""
    # Arrange
    expected_extract_dir, expected_binary_path = get_test_data_dir_path()

    # Act
    extracted_file_path = extract_file_from_zip(
        file_path=SAMPLE_FILE, destination_dir=TEST_DATA_DIR
    )

    # Assert
    assert extracted_file_path == expected_binary_path
    assert os.path.exists(extracted_file_path)

    # Verify manifest.json exists and log its contents
    manifest_path = os.path.join(expected_extract_dir, "manifest.json")
    assert os.path.exists(manifest_path)

    # Act
    readable_text = extract_readable_text_from_binary(extracted_file_path)

    # Log the extracted text
    print("\nExtracted readable text:")
    print("-" * 40)
    print(readable_text)
    print("-" * 40)

    # Assert
    assert readable_text is not None
