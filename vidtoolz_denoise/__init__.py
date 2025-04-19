import vidtoolz

import subprocess
import argparse
import sys
import os


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_denoise.mp4")


PRESETS = {
    "mild": 1,  # One pass
    "moderate": 2,  # Two passes
    "aggressive": 2,  # Two passes
}

DEFAULT_NF = -30  # Default nf if not provided explicitly


def reduce_audio_noise(
    input_file, output_file, preset, nf_value, highpass=None, lowpass=None
):
    # Determine how many afftdn passes
    passes = PRESETS.get(preset, 2)

    # Use nf_value provided or fall back to default
    nf = nf_value if nf_value is not None else DEFAULT_NF

    # Build filter chain
    filters = [f"afftdn=nf={nf}"] * passes

    if highpass:
        filters.append(f"highpass=f={highpass}")
    if lowpass:
        filters.append(f"lowpass=f={lowpass}")

    af_filter = ",".join(filters)

    # FFmpeg command
    command = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        "copy",
        "-af",
        af_filter,
        output_file,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Cleaned video saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e}")
        sys.exit(1)


def create_parser(subparser):
    parser = subparser.add_parser(
        "denoise",
        description="Denoise audio in a video",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # Add subprser arguments here.
    parser.add_argument(
        "input",
        help="""
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
""",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Path to output video file with denoised audio. default: %(default)s",
    )

    parser.add_argument(
        "-p",
        "--preset",
        choices=["mild", "moderate", "aggressive"],
        default="aggressive",
        help="Noise reduction level (default: %(default)s",
    )
    parser.add_argument(
        "-nf",
        "--nf",
        type=float,
        default=None,
        help="Noise floor in dB (e.g., -20, -25, -30). Overrides preset’s nf if set. default: %(default)s",
    )
    parser.add_argument(
        "-hp",
        "--highpass",
        type=int,
        default=100,
        help="High-pass filter cutoff frequency in Hz (e.g., 100  to remove low hum) default: %(default)s",
    )
    parser.add_argument(
        "-lp",
        "--lowpass",
        type=int,
        default=8000,
        help="Low-pass filter cutoff frequency in Hz (e.g., 8000 to remove hiss) default: %(default)s",
    )
    return parser


class ViztoolzPlugin:
    """Denoise audio in a video"""

    __name__ = "denoise"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        output = determine_output_path(args.input, args.output)
        reduce_audio_noise(
            args.input, output, args.preset, args.nf, args.highpass, args.lowpass
        )

    def hello(self, args):
        # this routine will be called when "vidtoolz "denoise is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


denoise_plugin = ViztoolzPlugin()
