# dn-deobfuscator

reverse engineering tool for dn2prj project files and dn2pst preset files

## Usage

```bash
python -m dn_deobfuscator.app
```

## Progress on Digitone 2 Preset Reverse Engineering

- [x] Created functional test for parsing the "HIDDEN TEARS" Digitone 2 preset file
- [x] Implemented `parse_digitone_preset` function to extract sound parameters
- [x] Identified the correct offset for the algorithm value (0x69)
- [x] Successfully parsed basic parameters from the binary file
- [x] Added detailed comments explaining parameter locations

### Parameter Locations Identified

- [x] Algorithm value: offset 0x69
- [x] Feedback value: offset 0x83
- [x] Filter parameters: around offset 0xA0-0xB0
- [x] Amplifier parameters: around offset 0xB0-0xC0
- [x] FX parameters: around offset 0xC0-0xD0
- [x] LFO parameters: around offset 0xD0-0xF0

### Next Steps

- [ ] Identify exact offsets for more parameters
- [ ] Implement conversion functions for floating-point values
- [ ] Add support for more preset files to validate the offsets
- [ ] Create a comprehensive mapping of parameter names to offsets
- [ ] Implement a function to modify parameters and save them back to the binary file
- [ ] Build a user interface for visualizing and editing presets
