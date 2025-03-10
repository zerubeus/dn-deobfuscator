import os
import pytest
import shutil
from pathlib import Path


@pytest.fixture
def patch_dir(tmp_path):
    """Create a temporary directory with sample patches for testing."""
    # Create directory structure
    patch_dir = tmp_path / "test_patches"
    patch_dir.mkdir()

    # Copy a few dn2pst files from the real data dir
    source_dir = (
        Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        / "data"
        / "dn2_patches"
    )
    sample_files = sorted(list(source_dir.glob("*.dn2pst")))[
        :3
    ]  # Just take the first 3 files

    for file in sample_files:
        shutil.copy2(file, patch_dir)

    return patch_dir


@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


def test_extract_patches_from_directory(patch_dir, output_dir):
    """Test extracting multiple patches from a directory."""
    from dn_deobfuscator.app import extract_patches_from_directory

    # Run the function to be tested
    output_md_path = output_dir / "patches_summary.md"
    extract_patches_from_directory(
        patches_dir=str(patch_dir),
        destination_dir=str(output_dir),
        output_markdown_path=str(output_md_path),
    )

    # Verify extraction_dir exists
    extraction_dir = output_dir / "extracted_dn2pst"
    assert extraction_dir.exists(), "Extraction directory was not created"

    # Verify the markdown file exists
    assert output_md_path.exists(), "Output markdown file was not created"

    # Read the content of the markdown file
    with open(output_md_path, "r") as f:
        md_content = f.read()

    # Get the list of files we extracted
    patch_files = list(patch_dir.glob("*.dn2pst"))

    # Verify each patch is mentioned in the markdown
    for patch_file in patch_files:
        patch_name = patch_file.stem
        assert (
            patch_name in md_content
        ), f"Patch {patch_name} not found in markdown content"

    # Verify that each patch has corresponding binary, text, and JSON files
    for patch_file in patch_files:
        base_name = patch_file.stem
        assert (extraction_dir / base_name).exists() or any(
            f.name.startswith(base_name) for f in extraction_dir.glob("*")
        ), f"Binary file for {base_name} not found"

        assert (
            extraction_dir / f"{base_name}.txt"
        ).exists(), f"Text file for {base_name} not found"

        # Verify the markdown contains the expected sections for each patch
        assert (
            f"- patch name: {base_name}" in md_content
        ), f"Patch name section for {base_name} not found in markdown"

        assert "- patch tags:" in md_content, "Patch tags section not found in markdown"

        assert (
            "- patch binary:" in md_content
        ), "Patch binary section not found in markdown"

        assert "00000000" in md_content, "Hex dump not found in markdown"
