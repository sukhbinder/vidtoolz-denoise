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
