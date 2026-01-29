#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "mapfile-parser",
#     "rabbitizer",
# ]
# ///
"""
Find the first difference(s) between the built ROM and the expected ROM.

Usage:
    uv run tools/first_diff.py
    uv run tools/first_diff.py -c 10  # Show 10 differences
"""

import argparse
from pathlib import Path

import mapfile_parser
import rabbitizer

BASENAME = "game"  # Change this to match your project

script_dir = Path(__file__).resolve().parent
root_dir = script_dir.parent
build_dir = root_dir / "build"
expected_build_dir = root_dir / "expected" / "build"


def decode_instruction(bytes_diff: bytes, map_file: mapfile_parser.MapFile) -> str:
    """Decode MIPS instruction bytes into readable assembly with symbol resolution."""
    word = (
        (bytes_diff[0] << 24)
        | (bytes_diff[1] << 16)
        | (bytes_diff[2] << 8)
        | (bytes_diff[3] << 0)
    )
    instr = rabbitizer.Instruction(word)
    imm_override = None

    if instr.isJumpWithAddress():
        # Instruction is a function call (jal) - resolve to symbol name
        sym_address = instr.getInstrIndexAsVram()
        sym_info = map_file.findSymbolByVramOrVrom(sym_address)
        if sym_info is not None:
            imm_override = sym_info.symbol.name

    return instr.disassemble(immOverride=imm_override, extraLJust=-20)


def main():
    parser = argparse.ArgumentParser(
        description="Find the first difference(s) between the built ROM and the expected ROM."
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=5,
        help="Find up to this many differences (default: 5)",
    )
    parser.add_argument(
        "-a", "--add-colons",
        action="store_true",
        help="Add colons between bytes in output",
    )
    args = parser.parse_args()

    mapfile_parser.frontends.first_diff.doFirstDiff(
        build_dir / f"{BASENAME}.map",
        expected_build_dir / f"{BASENAME}.map",
        build_dir / f"{BASENAME}.z64",
        expected_build_dir / f"{BASENAME}.z64",
        args.count,
        mismatchSize=True,
        addColons=args.add_colons,
        bytesConverterCallback=decode_instruction,
    )


if __name__ == "__main__":
    main()
