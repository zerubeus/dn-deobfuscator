import pytest
from dn_deobfuscator.app import extract_sysex_patches_to_markdown


def test_extract_sysex_patches_to_markdown(tmp_path):
    """Test extracting patches from a SysEx file and writing to markdown."""
    # Create a mock SysEx file with test data in the format we now expect
    # This simulates the Elektron Digitone format with prefix, name, and multiple tags
    test_sysex_data = bytes.fromhex(
        "F0 00 20 3C 0D 00 53 01 01 00 78 3E 6F 3A 4E 00"  # Header (standard for Digitone)
        "00 00 00 01 00 00 00 21 42 44 00 20 54 45 53 54"  # BD. TEST (prefix and name)
        "31 00 00 20 53 4D 00 00 00 00 02 00 00 55 0B 73"  # Patch data
        "12 12 00 00 13 00 40 00 40 00 00 2A 00 2A 00 03"  # More patch data
        "F7"  # End of SysEx
    )

    sysex_file = tmp_path / "test.syx"
    sysex_file.write_bytes(test_sysex_data)

    # Create output markdown file path
    output_md = tmp_path / "patches.md"

    # Call the function
    extract_sysex_patches_to_markdown(str(sysex_file), str(output_md))

    # Verify the markdown file exists
    assert output_md.exists()

    # Read and verify content
    content = output_md.read_text()

    # Check patch name is present with prefix
    assert "patch name: BD. TEST1" in content

    # Check tags are present (the function will assign tags based on name)
    assert "patch tags:" in content
    assert ", " in content  # Multiple tags should be comma-separated

    # Check hex dump format is present
    assert "00000000" in content  # Offset
    assert "|" in content  # ASCII section divider
    assert "F0 00 20 3C" in content.upper()  # Hex values (case-insensitive)

    # Check the binary data is properly formatted
    assert "|.. <..S...x>o:N.|" in content


def test_extract_sysex_patches_to_markdown_invalid_file(tmp_path):
    """Test handling of invalid SysEx file."""
    # Create an invalid SysEx file (no proper header/footer)
    invalid_data = bytes([0x00, 0x01, 0x02])
    invalid_file = tmp_path / "invalid.syx"
    invalid_file.write_bytes(invalid_data)

    output_md = tmp_path / "patches.md"

    # Call the function and check the error message
    with pytest.raises(ValueError) as excinfo:
        extract_sysex_patches_to_markdown(str(invalid_file), str(output_md))

    # Check the error message
    assert "No valid patches found" in str(excinfo.value)


def test_extract_sysex_patches_to_markdown_append_mode(tmp_path):
    """Test that patches are appended to existing markdown file."""
    # Create initial markdown content
    output_md = tmp_path / "patches.md"
    output_md.write_text("# Existing Patches\n\n")

    # Create test SysEx file similar to the first test
    test_sysex_data = bytes.fromhex(
        "F0 00 20 3C 0D 00 53 01 01 00 78 3E 6F 3A 4E 00"  # Header (standard for Digitone)
        "00 00 00 01 00 00 00 21 43 59 00 20 4A 41 5A 5A"  # CY. JAZZ (prefix and name)
        "59 00 00 20 53 4D 00 00 00 00 02 00 00 55 0B 73"  # Patch data
        "12 12 00 00 13 00 40 00 40 00 00 2A 00 2A 00 03"  # More patch data
        "F7"  # End of SysEx
    )

    sysex_file = tmp_path / "test.syx"
    sysex_file.write_bytes(test_sysex_data)

    # Extract patches with append=True
    extract_sysex_patches_to_markdown(str(sysex_file), str(output_md), append=True)

    # Verify content was appended
    content = output_md.read_text()
    assert content.startswith("# Existing Patches\n\n")
    assert "patch name: CY. JAZZY" in content
    assert "patch tags:" in content
