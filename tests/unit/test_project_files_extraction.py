import os
import shutil
import json
import pytest
import logging
from typing import NamedTuple

from dn_deobfuscator.app import extract_file_from_zip


logger = logging.getLogger(__name__)


class FileTestPaths(NamedTuple):
    extract_dir: str
    binary_path: str
    text_path: str
    source_file: str
    temp_zip: str


@pytest.fixture
def dn2prj_paths(data_dir) -> FileTestPaths:
    """Fixture providing paths for dn2prj test files"""
    extract_dir = os.path.join(data_dir, "extracted_dn2prj")
    return FileTestPaths(
        extract_dir=extract_dir,
        binary_path=os.path.join(extract_dir, "AUTOMATIC"),
        text_path=os.path.join(extract_dir, "automatic.txt"),
        source_file=os.path.join(data_dir, "automatic.dn2prj"),
        temp_zip=os.path.join(data_dir, "AUTOMATIC.zip"),
    )


@pytest.fixture
def hidden_tears_paths(data_dir) -> FileTestPaths:
    """Fixture providing paths for hidden tears test files"""
    extract_dir = os.path.join(data_dir, "extracted_dn2pst")
    return FileTestPaths(
        extract_dir=extract_dir,
        binary_path=os.path.join(extract_dir, "HIDDEN TEARS"),
        text_path=os.path.join(extract_dir, "hidden-tears.txt"),
        source_file=os.path.join(data_dir, "hidden-tears.dn2pst"),
        temp_zip=os.path.join(data_dir, "hidden-tears.zip"),
    )


@pytest.fixture(autouse=True)
def cleanup_extracted(data_dir):
    """Cleanup the extracted directory before and after test"""
    # Clean up any existing directories from previous test runs
    directories_to_clean = [
        os.path.join(data_dir, "extracted_dn2prj"),
        os.path.join(data_dir, "extracted_dn2pst"),
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
        os.path.join(data_dir, "AUTOMATIC.zip"),
        os.path.join(data_dir, "hidden-tears.zip"),
        os.path.join(data_dir, "temp-hidden-tears.zip"),
    ]

    for file_path in temp_files_to_clean:
        if os.path.exists(file_path):
            os.remove(file_path)


def verify_extraction(paths: FileTestPaths, data_dir: str):
    """Helper function to verify file extraction and paths"""
    binary_path, text_path = extract_file_from_zip(
        file_path=paths.source_file, destination_dir=data_dir
    )

    # Verify paths
    assert binary_path == paths.binary_path
    assert text_path == paths.text_path

    # Verify files exist
    assert os.path.exists(binary_path)
    assert os.path.exists(text_path)

    # Verify manifest exists
    manifest_path = os.path.join(paths.extract_dir, "manifest.json")
    assert os.path.exists(manifest_path)

    # Log manifest contents
    with open(manifest_path) as f:
        manifest_content = json.load(f)
        print(f"\nmanifest.json contents for {os.path.basename(paths.source_file)}:")
        print(json.dumps(manifest_content, indent=2))

    # Verify temp zip was cleaned
    assert not os.path.exists(paths.temp_zip)

    return binary_path, text_path


def verify_text_extraction(paths: FileTestPaths, data_dir: str):
    """Helper function to verify text extraction from binary"""
    binary_path, text_path = verify_extraction(paths, data_dir)

    # Read and verify text content
    with open(text_path) as f:
        text_content = f.read()

    # Log extracted text
    logger.info(
        f"\nExtracted readable text from {os.path.basename(paths.source_file)}:"
    )
    logger.info("-" * 40)
    logger.info(text_content)
    logger.info("-" * 40)

    # Verify text content
    assert text_content is not None
    assert len(text_content) > 0


@pytest.mark.parametrize(
    "fixture_name,test_name",
    [("dn2prj_paths", "dn2prj"), ("hidden_tears_paths", "hidden_tears")],
)
def test_unzip_file(fixture_name, test_name, data_dir, request):
    """Parameterized test for unzipping different file types"""
    paths = request.getfixturevalue(fixture_name)
    verify_extraction(paths, data_dir)


@pytest.mark.parametrize(
    "fixture_name,test_name",
    [("dn2prj_paths", "binary"), ("hidden_tears_paths", "hidden_tears")],
)
def test_extract_readable_text(fixture_name, test_name, data_dir, request):
    """Parameterized test for extracting readable text from different file types"""
    paths = request.getfixturevalue(fixture_name)
    verify_text_extraction(paths, data_dir)
