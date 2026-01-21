---
name: n64-decomp-ido
description: |
  IDO build configuration for N64 decompilation. Use when setting up C compilation for an IDO-based N64 decomp project. Covers asm-processor setup and build integration.
---

# IDO Build Configuration

Splat detects the compiler and sets `options.compiler: IDO` in the yaml. This skill covers how to configure the build for IDO.

## asm-processor

IDO doesn't support inline assembly the way modern compilers do. asm-processor solves this by:
1. Replacing `GLOBAL_ASM` blocks with dummy C code of matching sizes
2. Compiling everything together with IDO
3. Overwriting the dummy output with actual assembly

This lets assembly and C coexist without recompilation complexity. It also handles tricky cases like "late_rodata" (read-only data emitted in two passes by IDO).

See https://github.com/simonlindholm/asm-processor for details.

### Download

Download prebuilt binaries from https://github.com/simonlindholm/asm-processor/releases

URL pattern:
```
https://github.com/simonlindholm/asm-processor/releases/download/1.0.1/asm-processor-{triple}.tar.xz
```

Triples: `aarch64-apple-darwin`, `x86_64-apple-darwin`, `x86_64-pc-windows-msvc` (.zip), `aarch64-unknown-linux-gnu`, `x86_64-unknown-linux-gnu`

### Build Integration

asm-processor wraps the IDO compiler. See https://github.com/ethteck/pokemonsnap/blob/main/configure.py for a full example.

The command pattern:
```
tools/asm_proc/asm-processor {IDO_CC} -- {CROSS_AS} {AS_FLAGS} -- {IDO_FLAGS} -c -o $out $in
```

Where:
- First `--` separates IDO path from assembler
- Second `--` separates assembler from IDO flags
