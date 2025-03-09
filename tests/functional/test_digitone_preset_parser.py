import os
import shutil

import pytest
from dn_deobfuscator.app import extract_file_from_zip, parse_digitone_preset

# Path to test data
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Path of hidden-tears.dn2pst file
HIDDEN_TEARS_PATH = os.path.join(TEST_DATA_DIR, "hidden-tears.dn2pst")


@pytest.fixture(autouse=True)
def clean_after_test():

    yield

    cleanup_dirs = [
        os.path.join(TEST_DATA_DIR, "extracted_dn2pst"),
        os.path.join(TEST_DATA_DIR, "extracted_dn2prj"),
    ]

    for dir in cleanup_dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)


def test_parse_hidden_tears_preset():
    """Test parsing the HIDDEN TEARS preset file and extracting its parameters."""

    text_path, binary_path = extract_file_from_zip(HIDDEN_TEARS_PATH, TEST_DATA_DIR)

    # Parse the binary file
    parameters = parse_digitone_preset(binary_path=binary_path)

    # Test all the expected parameters based on the Digitone screen values

    # SYN Page 1/4
    assert parameters["algo"] == 7
    assert parameters["c"] == 1.00
    assert parameters["a"] == 1.00
    assert parameters["b"][0] == 1.00  # B1
    assert parameters["b"][1] == 1.00  # B2
    assert parameters["harm"] == -14.50
    assert parameters["dtun"] == 38.71
    assert parameters["fdbk"] == 85
    assert parameters["mix"] == -28

    # SYN Page 2/4
    assert parameters["a_envelope"]["atk"] == 0
    assert parameters["a_envelope"]["dec"] == 124
    assert parameters["a_envelope"]["end"] == 0
    assert parameters["a_envelope"]["lev"] == 115

    assert parameters["b_envelope"]["atk"] == 0
    assert parameters["b_envelope"]["dec"] == 127
    assert parameters["b_envelope"]["end"] == 0
    assert parameters["b_envelope"]["lev"] == 127

    # SYN Page 3/4
    assert parameters["adel"] == 0
    assert parameters["atrg"] is True  # on
    assert parameters["arst"] is True  # on
    assert parameters["phrt"] == "ALL"
    assert parameters["bdel"] == 0
    assert parameters["btrg"] is True  # on
    assert parameters["brst"] is True  # on

    # SYN Page 4/4
    assert parameters["ratio_offset"]["c"] == 0.00
    assert parameters["ratio_offset"]["a"] == 0.00
    assert parameters["ratio_offset"]["b1"] == 0.00
    assert parameters["ratio_offset"]["b2"] == 0.00

    assert parameters["key_track"]["a"] == 0
    assert parameters["key_track"]["b1"] == 0
    assert parameters["key_track"]["b2"] == 0

    # Filter Page
    assert parameters["filter"]["type"] == "Lowpass 4"
    assert parameters["filter"]["attack"] == 41
    assert parameters["filter"]["decay"] == 70
    assert parameters["filter"]["sustain"] == 80
    assert parameters["filter"]["release"] == 106
    assert parameters["filter"]["frequency"] == 78.68
    assert parameters["filter"]["resonance"] == 64
    assert parameters["filter"]["env_amount"] == 9

    # AMP Page
    assert parameters["amp"]["attack"] == 53
    assert parameters["amp"]["decay"] == 87
    assert parameters["amp"]["sustain"] == 76
    assert parameters["amp"]["release"] == 60
    assert parameters["amp"]["reset"] is True  # on
    assert parameters["amp"]["mode"] == "ADSR"
    assert parameters["amp"]["pan"] == "Center"
    assert parameters["amp"]["volume"] == 70

    # FX Page
    assert parameters["fx"]["bit_reduction"] is False  # off
    assert parameters["fx"]["overdrive"] == 76
    assert parameters["fx"]["sample_rate_reduction"] == 0
    assert parameters["fx"]["sample_rate_routing"] == "Pre-filter"
    assert parameters["fx"]["delay"] is False  # off
    assert parameters["fx"]["reverb"] == 127
    assert parameters["fx"]["chorus"] == 59
    assert parameters["fx"]["overdrive_routing"] == "Pre-filter"

    # LFO 1
    assert parameters["lfo1"]["speed"] == 40.01
    assert parameters["lfo1"]["multiplier"] == 16
    assert parameters["lfo1"]["fade"] == 0
    assert parameters["lfo1"]["destination"] == "SYN HARM"
    assert parameters["lfo1"]["waveform"] == "Sine"
    assert parameters["lfo1"]["start_phase"] == 10
    assert parameters["lfo1"]["mode"] == "Free"
    assert parameters["lfo1"]["depth"] == -10.34

    # LFO 2
    assert parameters["lfo2"]["speed"] == 32.73
    assert parameters["lfo2"]["multiplier"] == 32
    assert parameters["lfo2"]["fade"] == 0
    assert parameters["lfo2"]["destination"] == "SYN P2A4"
    assert parameters["lfo2"]["waveform"] == "Triangle"
    assert parameters["lfo2"]["start_phase"] == 0
    assert parameters["lfo2"]["mode"] == "Trig"
    assert parameters["lfo2"]["depth"] == -0.16

    # LFO 3 - should be disabled or have default values
    assert "lfo3" in parameters
