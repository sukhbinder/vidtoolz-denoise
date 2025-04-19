# vidtoolz-denoise

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-denoise.svg)](https://pypi.org/project/vidtoolz-denoise/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-denoise?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-denoise/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-denoise/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-denoise/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-denoise/blob/main/LICENSE)

Denoise audio in a video

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-denoise
```
## Usage

type ``vid denoise --help`` to get help

```bash
usage: vid denoise [-h] [-o OUTPUT] [-p {mild,moderate,aggressive}] [-nf NF]
                   [-hp HIGHPASS] [-lp LOWPASS]
                   input

Denoise audio in a video

positional arguments:
  input                 
                        Reduce background noise and hum from video audio using FFmpeg's afftdn filter.
                        
                        You can choose from presets (mild, moderate, aggressive) or fine-tune using --nf directly.
                        Presets define how many afftdn passes are used:
                          mild       = 1 pass (light cleanup)
                          moderate   = 2 passes (balanced)
                          aggressive = 2 passes (default, heavy cleanup)
                        
                        Use --nf to override the default noise floor (e.g. -20, -25, -30, -35).
                        
                        Examples:
                          vid denoise input.mp4 
                          vid denoise input.mp4  --preset moderate
                          vid denoise input.mp4  --nf -25 --highpass 100 --lowpass 8000

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to output video file with denoised audio. default: None
  -p {mild,moderate,aggressive}, --preset {mild,moderate,aggressive}
                        Noise reduction level (default: moderate
  -nf NF, --nf NF       Noise floor in dB (e.g., -20, -25, -30). Overrides preset’s nf if set. default: None
  -hp HIGHPASS, --highpass HIGHPASS
                        High-pass filter cutoff frequency in Hz (e.g., 100  to remove low hum) default: 100
  -lp LOWPASS, --lowpass LOWPASS
                        Low-pass filter cutoff frequency in Hz (e.g., 8000 to remove hiss) default: 8000

```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-denoise
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
