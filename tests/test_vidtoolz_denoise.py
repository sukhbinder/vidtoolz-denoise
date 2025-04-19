import pytest
import vidtoolz_denoise as w
from unittest.mock import patch, call

from argparse import ArgumentParser


def test_create_parser():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None

    args = parser.parse_args(["input.mp4"])
    assert args.input == "input.mp4"
    assert args.output is None
    assert args.preset == "aggressive"
    assert args.nf is None
    assert args.highpass == 100
    assert args.lowpass == 8000


def test_parser_custom_args():
    subparser = ArgumentParser().add_subparsers()
    parser = w.create_parser(subparser)

    assert parser is not None
    args = parser.parse_args(
        [
            "input.mp4",
            "-o",
            "cleaned.mp4",
            "--preset",
            "moderate",
            "--nf",
            "-25",
            "--highpass",
            "120",
            "--lowpass",
            "7000",
        ]
    )
    assert args.input == "input.mp4"
    assert args.output == "cleaned.mp4"
    assert args.preset == "moderate"
    assert args.nf == -25
    assert args.highpass == 120
    assert args.lowpass == 7000


def test_plugin(capsys):
    w.denoise_plugin.hello(None)
    captured = capsys.readouterr()
    assert "Hello! This is an example ``vidtoolz`` plugin." in captured.out


@patch("vidtoolz_denoise.subprocess.run")
def test_reduce_audio_noise_with_nf(mock_run):
    w.reduce_audio_noise(
        "in.mp4", "out.mp4", preset="moderate", nf_value=-28, highpass=150, lowpass=6000
    )

    expected_filters = ",".join(
        ["afftdn=nf=-28", "afftdn=nf=-28", "highpass=f=150", "lowpass=f=6000"]
    )

    mock_run.assert_called_once_with(
        ["ffmpeg", "-i", "in.mp4", "-c:v", "copy", "-af", expected_filters, "out.mp4"],
        check=True,
    )


@patch("vidtoolz_denoise.subprocess.run")
def test_reduce_audio_noise_with_default_nf(mock_run):
    w.reduce_audio_noise(
        "x.mp4", "y.mp4", preset="mild", nf_value=None, highpass=90, lowpass=9000
    )

    expected_filters = ",".join(
        [f"afftdn=nf={w.DEFAULT_NF}", "highpass=f=90", "lowpass=f=9000"]
    )

    mock_run.assert_called_once_with(
        ["ffmpeg", "-i", "x.mp4", "-c:v", "copy", "-af", expected_filters, "y.mp4"],
        check=True,
    )
