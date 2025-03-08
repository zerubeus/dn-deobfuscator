import os
import shutil
import json
import pytest
import logging

from dn_deobfuscator.app import extract_file_from_zip, extract_readable_text_from_binary


logger = logging.getLogger(__name__)

# Path to the test data directory containing the actual AUTOMATIC.dn2prj file
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SAMPLE_FILE = os.path.join(TEST_DATA_DIR, "AUTOMATIC.dn2prj")
HIDDEN_TEARS_FILE = os.path.join(TEST_DATA_DIR, "hidden-tears.dn2pst")


def get_test_data_dir_path():
    expected_extract_dir = os.path.join(TEST_DATA_DIR, "extracted_dn2prj")
    expected_binary_path = os.path.join(expected_extract_dir, "AUTOMATIC")

    return expected_extract_dir, expected_binary_path


def get_hidden_tears_paths():
    expected_extract_dir = os.path.join(TEST_DATA_DIR, "extracted_dn2pst")
    expected_binary_path = os.path.join(expected_extract_dir, "HIDDEN TEARS")

    return expected_extract_dir, expected_binary_path


@pytest.fixture(autouse=True)
def cleanup_extracted():
    """Cleanup the extracted directory before and after test"""
    # Clean up any existing directories from previous test runs
    directories_to_clean = [
        os.path.join(TEST_DATA_DIR, "extracted_dn2prj"),
        os.path.join(TEST_DATA_DIR, "extracted_dn2pst"),
    ]

    for dir_path in directories_to_clean:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    yield

    # Cleanup extracted directories and temporary zips after the test
    for dir_path in directories_to_clean:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    temp_files_to_clean = [
        os.path.join(TEST_DATA_DIR, "AUTOMATIC.zip"),
        os.path.join(TEST_DATA_DIR, "hidden-tears.zip"),
        os.path.join(TEST_DATA_DIR, "temp-hidden-tears.zip"),
    ]

    for file_path in temp_files_to_clean:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_unzip_dn2prj_file():
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
    logger.info("\nExtracted readable text:")
    logger.info("-" * 40)
    logger.info(readable_text)
    logger.info("-" * 40)

    # Assert
    assert readable_text is not None


def test_unzip_hidden_tears_file():
    """Test that we can extract files from a .dn2pst file just like the manual
    process:
    mv hidden-tears.dn2pst hidden-tears.zip
    unzip hidden-tears.zip -d extracted_dn2prj
    """
    # Arrange
    expected_extract_dir, expected_binary_path = get_hidden_tears_paths()

    # Act
    extracted_file_path = extract_file_from_zip(
        file_path=HIDDEN_TEARS_FILE, destination_dir=TEST_DATA_DIR
    )

    # Assert
    assert extracted_file_path == expected_binary_path
    assert os.path.exists(extracted_file_path)

    # Verify manifest.json exists and log its contents
    manifest_path = os.path.join(expected_extract_dir, "manifest.json")
    assert os.path.exists(manifest_path)

    with open(manifest_path) as f:
        manifest_content = json.load(f)
        print("\nhidden-tears manifest.json contents:")
        print(json.dumps(manifest_content, indent=2))

    # Verify the temporary zip file was cleaned up
    assert not os.path.exists(os.path.join(TEST_DATA_DIR, "hidden-tears.zip"))


def test_extract_readable_text_from_hidden_tears():
    """Test that we can extract readable text from the hidden-tears binary file"""
    # Arrange
    expected_extract_dir, expected_binary_path = get_hidden_tears_paths()

    # Act - First extract the binary file
    extracted_file_path = extract_file_from_zip(
        file_path=HIDDEN_TEARS_FILE, destination_dir=TEST_DATA_DIR
    )

    # Assert extraction was successful
    assert extracted_file_path == expected_binary_path
    assert os.path.exists(extracted_file_path)

    # Verify manifest.json exists
    manifest_path = os.path.join(expected_extract_dir, "manifest.json")
    assert os.path.exists(manifest_path)

    # Act - Extract readable text from the binary
    readable_text = extract_readable_text_from_binary(extracted_file_path)

    # Log the extracted text
    logger.info("\nExtracted readable text from hidden-tears:")
    logger.info("-" * 40)
    logger.info(readable_text)
    logger.info("-" * 40)

    # Assert
    assert readable_text is not None
    assert len(readable_text) > 0
