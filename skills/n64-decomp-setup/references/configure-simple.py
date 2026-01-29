#!/usr/bin/env python3
"""
Simple build configuration for N64 decompilation projects.
Use this for initial setup - handles assembly-only builds.
For C compilation and assets, see configure-example.py
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

import ninja_syntax
import splat
import splat.scripts.split as split
from splat.segtypes.linker_entry import LinkerEntry

ROOT = Path(__file__).parent
BASENAME = "game"  # Change this to your game name
YAML_FILE = Path(f"{BASENAME}.yaml")

LD_PATH = f"{BASENAME}.ld"
MAP_PATH = f"build/{BASENAME}.map"
ELF_PATH = f"build/{BASENAME}.elf"
Z64_PATH = f"build/{BASENAME}.z64"
OK_PATH = f"build/{BASENAME}.ok"

CROSS = "mips-linux-gnu-"
CROSS_AS = f"{CROSS}as"
CROSS_CPP = f"{CROSS}cpp"
CROSS_LD = f"{CROSS}ld"
CROSS_OBJCOPY = f"{CROSS}objcopy"

INCLUDES = "-I include"
DEFINES = "-D_FINALROM -DNDEBUG"  # Add -DBUILD_VERSION=VERSION_H after identifying libultra version
AS_FLAGS = f"-EB -march=vr4300 -mtune=vr4300 -G 0 {INCLUDES}"


def clean():
    shutil.rmtree("asm", ignore_errors=True)
    shutil.rmtree("assets", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    if os.path.exists(".splache"):
        os.remove(".splache")


def create_build_script(linker_entries: list[LinkerEntry]):
    os.makedirs("build", exist_ok=True)

    ninja = ninja_syntax.Writer(open("build.ninja", "w"), width=9999)

    # Assembly rule - preprocess then assemble
    ninja.rule(
        "as",
        description="as $in",
        command=f"{CROSS_CPP} {INCLUDES} {DEFINES} $in | {CROSS_AS} {AS_FLAGS} -o $out",
    )

    # Binary linking rule
    ninja.rule(
        "bin",
        description="bin $in",
        command=f"{CROSS_LD} -r -b binary $in -o $out",
    )

    # Link rule
    ninja.rule(
        "ld",
        description="link $out",
        command=f"{CROSS_LD} -T undefined_funcs_auto.txt -T undefined_syms_auto.txt -Map $mapfile -T $in -o $out",
    )

    # ROM extraction rule
    ninja.rule(
        "z64",
        description="rom $out",
        command=f"{CROSS_OBJCOPY} $in $out -O binary",
    )

    # Checksum verification rule
    ninja.rule(
        "sha1sum",
        description="sha1sum $in",
        command="sha1sum -c $in && touch $out",
    )

    built_objects = []

    for entry in linker_entries:
        if entry.object_path is None:
            continue

        seg = entry.segment
        if seg.type[0] == ".":
            continue

        src = entry.src_paths[0]
        obj = entry.object_path

        if src.suffix == ".s":
            ninja.build(str(obj), "as", str(src))
            built_objects.append(str(obj))
        elif src.suffix == ".bin":
            ninja.build(str(obj), "bin", str(src))
            built_objects.append(str(obj))

    # Link
    ninja.build(
        ELF_PATH,
        "ld",
        LD_PATH,
        implicit=built_objects,
        variables={"mapfile": MAP_PATH},
    )

    # Extract ROM
    ninja.build(Z64_PATH, "z64", ELF_PATH)

    # Verify checksum
    ninja.build(OK_PATH, "sha1sum", "checksum.sha1", implicit=[Z64_PATH])

    ninja.default(OK_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure the build")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean build artifacts before configuring")
    args = parser.parse_args()

    if args.clean:
        clean()
        # Continue to configure after cleaning (don't exit)

    if not Path(f"baserom.z64").exists():
        print("baserom.z64 not found!")
        sys.exit(1)

    # Run splat
    split.main([YAML_FILE], modes=["all"], verbose=False)

    # Generate ninja build file
    create_build_script(split.linker_writer.entries)

    print("Build configured. Run 'ninja' to build.")
