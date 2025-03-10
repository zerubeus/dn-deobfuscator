# dn-deobfuscator

reverse engineering tool for dn2prj project files and dn2pst preset files

## Usage

The `dn-deobfuscator` tool can work with multiple file types:

- Elektron Digitone project files (`.dn2prj`)
- Elektron Digitone preset files (`.dn2pst`)
- SysEx files (`.syx`) with sounds/patches

### Basic Usage

```bash
python -m dn_deobfuscator.app <file_path>
```

This will extract the contents of a `.dn2prj` or `.dn2pst` file to the current directory.

### Command-line Options

```
usage: app.py [-h] [-d DESTINATION] [-s] [-a] file_path
```

#### Positional Arguments:

- `file_path` - Path to the file to extract (.dn2prj, .dn2pst, or .syx)

#### Optional Arguments:

- `-h, --help` - Show the help message and exit
- `-d DESTINATION, --destination DESTINATION` - Destination directory for extracted files (default: current directory)
- `-s, --sysex` - Process file as SysEx format and extract to markdown
- `-a, --append` - Append to output file instead of overwriting (only for SysEx extraction)

### Examples

#### Extract a Digitone project or preset file:

```bash
python -m dn_deobfuscator.app path/to/mysound.dn2pst
```

This will extract the binary data and create a text representation in the current directory.

#### Extract a Digitone project to a specific directory:

```bash
python -m dn_deobfuscator.app path/to/myproject.dn2prj -d output_folder
```

#### Extract SysEx patches to a markdown file:

```bash
python -m dn_deobfuscator.app path/to/patches.syx -s
```

This will create a markdown file named `patches.syx_patches.md` in the current directory, containing all patches found in the SysEx file. Each patch will include:

- Patch name with prefix (e.g., "BD. KICK", "CY. CRASH")
- Patch tags
- Hex dump of the patch binary data

#### Extract multiple SysEx files to the same markdown file:

```bash
python -m dn_deobfuscator.app path/to/first.syx -s
python -m dn_deobfuscator.app path/to/second.syx -s -a
```

The `-a` (append) option allows you to add patches from multiple SysEx files to the same markdown document.

#### Extract SysEx to a specific directory:

```bash
python -m dn_deobfuscator.app path/to/patches.syx -s -d output_folder
```

This will create the markdown file in the specified output folder.

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

## Sound Preset Parameters

This section documents the sound preset parameters found in Digitone 2 based on our reverse engineering work and the Digitone 2 User Manual.

### SYN Parameters (Page 1/4)

| Parameter | Possible Values        | Description                                                                         |
| --------- | ---------------------- | ----------------------------------------------------------------------------------- |
| ALGO      | 1-8                    | FM Algorithm (arrangement of operators)                                             |
| C         | 0.00-1.00              | Carrier operator level                                                              |
| A         | 0.00-1.00              | A operator level                                                                    |
| B         | [0.00-1.00, 0.00-1.00] | B1 and B2 operator levels                                                           |
| HARM      | -26.00 to +26.00       | Harmonic value - negative values change operator C, positive values change A and B1 |
| DTUN      | -48.00 to +48.00       | Detune value                                                                        |
| FDBK      | 0-127                  | Feedback amount                                                                     |
| MIX       | -64 to +63             | Mix value between carrier outputs X and Y                                           |

### SYN Parameters (Page 2/4)

| Parameter  | Possible Values                                    | Description          |
| ---------- | -------------------------------------------------- | -------------------- |
| A Envelope | { atk: 0-127, dec: 0-127, end: 0-127, lev: 0-127 } | A operator envelope  |
| B Envelope | { atk: 0-127, dec: 0-127, end: 0-127, lev: 0-127 } | B operators envelope |

### SYN Parameters (Page 3/4)

| Parameter | Possible Values | Description          |
| --------- | --------------- | -------------------- |
| ADEL      | 0-127           | A Delay value        |
| ATRG      | true/false      | A Trig (on/off)      |
| ARST      | true/false      | A Reset (on/off)     |
| PHRT      | "ALL", "OFF"    | Phase retrigger mode |
| BDEL      | 0-127           | B Delay value        |
| BTRG      | true/false      | B Trig (on/off)      |
| BRST      | true/false      | B Reset (on/off)     |

### SYN Parameters (Page 4/4)

| Parameter       | Possible Values  | Description              |
| --------------- | ---------------- | ------------------------ |
| Ratio Offset C  | -16.00 to +16.00 | Carrier ratio offset     |
| Ratio Offset A  | -16.00 to +16.00 | A operator ratio offset  |
| Ratio Offset B1 | -16.00 to +16.00 | B1 operator ratio offset |
| Ratio Offset B2 | -16.00 to +16.00 | B2 operator ratio offset |
| Key Track A     | -64 to +63       | A operator key tracking  |
| Key Track B1    | -64 to +63       | B1 operator key tracking |
| Key Track B2    | -64 to +63       | B2 operator key tracking |

### Filter Parameters

| Parameter  | Possible Values                                          | Description               |
| ---------- | -------------------------------------------------------- | ------------------------- |
| Type       | "Lowpass", "Bandpass", "Highpass" with 2-pole (12dB/oct) | Filter type               |
| Attack     | 0-127                                                    | Filter envelope attack    |
| Decay      | 0-127                                                    | Filter envelope decay     |
| Sustain    | 0-127                                                    | Filter envelope sustain   |
| Release    | 0-127                                                    | Filter envelope release   |
| Frequency  | 0-127                                                    | Filter cutoff frequency   |
| Resonance  | 0-127                                                    | Filter resonance          |
| Env Amount | -64 to +63                                               | Envelope amount (bipolar) |

### Amplifier Parameters

| Parameter | Possible Values           | Description          |
| --------- | ------------------------- | -------------------- |
| Attack    | 0-127                     | Amp envelope attack  |
| Decay     | 0-127                     | Amp envelope decay   |
| Sustain   | 0-127                     | Amp envelope sustain |
| Release   | 0-127                     | Amp envelope release |
| Reset     | true/false                | Reset flag           |
| Mode      | "ADSR", "AD"              | Envelope mode        |
| Pan       | "Left", "Center", "Right" | Pan position         |
| Volume    | 0-127                     | Output volume        |

### FX Parameters

| Parameter             | Possible Values             | Description                  |
| --------------------- | --------------------------- | ---------------------------- |
| Bit Reduction         | true/false                  | Bit reduction enabled        |
| Overdrive             | 0-127                       | Overdrive amount             |
| Sample Rate Reduction | 0-127                       | Sample rate reduction amount |
| Sample Rate Routing   | "Pre-filter", "Post-filter" | Routing mode                 |
| Delay                 | true/false                  | Delay enabled                |
| Reverb                | 0-127                       | Reverb amount                |
| Chorus                | 0-127                       | Chorus amount                |
| Overdrive Routing     | "Pre-filter", "Post-filter" | Overdrive routing            |

### LFO Parameters

| Parameter   | Possible Values                                                                                | Description      |
| ----------- | ---------------------------------------------------------------------------------------------- | ---------------- |
| Speed       | 0.00-127.00                                                                                    | LFO speed        |
| Multiplier  | 1, 2, 4, 8, 16, 32, 64                                                                         | Speed multiplier |
| Fade        | 0-127                                                                                          | Fade time        |
| Destination | SYN parameters (HARM, DTUN, FDBK, MIX), FLTR parameters (FREQ, RES), AMP parameters (PAN, VOL) | Target parameter |
| Waveform    | "Triangle", "Sine", "Square", "Sawtooth", "Exponential", "Ramp", "Random"                      | Waveform type    |
| Start Phase | 0-127                                                                                          | Start phase      |
| Mode        | "FREE", "TRIG", "HOLD", "ONE", "HALF"                                                          | LFO mode         |
| Depth       | -64.00 to +63.00                                                                               | Modulation depth |

_Note: Parameter values are based on both our reverse engineering of the HIDDEN TEARS preset and the official Digitone 2 User Manual._
