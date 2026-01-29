---
name: n64-decomp-splat
description: |
  Splat YAML configuration reference for N64 decompilation projects. Use when working with splat configuration files (.yaml), including: (1) Creating or modifying splat.yaml files, (2) Configuring segments and subsegments, (3) Setting up build options, linker scripts, or paths, (4) Understanding splat configuration structure and options. Triggers on mentions of splat.yaml, splat configuration, segment setup, or when modifying decomp project settings.
---

# Splat YAML Configuration Reference

## Working with Splat YAML

This guide focuses on common operations when working with an existing splat.yaml configuration file.

**IMPORTANT**: After ANY changes to the yaml, run `python configure.py --clean` before rebuilding.

## Segment Formats

**Short form (list)**: `[start, type, name]` or `[start, type]`

```yaml
segments:
  - [0x0, header, header]
  - [0x1000, asm, boot]
  - [0x5000]            # End marker - boot ends at 0x5000
```

**Dictionary form**: For `vram`, `bss_size`, `subsegments`, etc.

```yaml
segments:
  - name: boot
    type: code
    start: 0x1000
    vram: 0x80000400
    bss_size: 0x80
    subsegments:
      - [0x1000, asm, main]
      - [0x2000, .rodata, main]
```

Each segment's end is the next segment's start. Final segment needs an end marker `[offset]`.

### Common Segment Types

**Code/Assembly:**
- `asm` - Generated assembly (splat overwrites on each run)
- `hasm` - Hand-written assembly (splat preserves)
- `c` - C source file
- `code` - Container with subsegments

**Data:**
- `data` - Extracted into standalone .data.s file
- `.data` - From compiled C object (not extracted)

**Read-only data:**
- `rodata` - Separate .rodata.s file, used with INCLUDE_RODATA
- `.rodata` / `.rdata` - Migrated into function .s files (default)

**Other:**
- `bss` / `.bss` - Uninitialized data (linker symbol only)
- `bin` - Raw binary
- `textbin` / `databin` / `rodatabin` - Binary with incbin
- `header` - ROM header
- `pad` - Zero-filled padding

### Subsegments in Code Segments

Code segments contain subsegments that become individual files:

```yaml
- name: main
  type: code
  start: 0x1050
  vram: 0x80001050
  bss_size: 0x7DAC0
  subsegments:
    - [0x1050, asm]                    # Creates asm/1050.s
    - [0x2000, asm, player]            # Creates asm/player.s
    - [0x3000, c, physics/movement]    # Creates src/physics/movement.c
    - [0x4000, .rodata, player]        # Creates asm/player.rodata.s
    - { start: 0xB1BD0, type: bss, vram: 0x800E2E00 } # Linker symbol only
```

Names with slashes create subdirectories. Omit name to use hex offset (e.g., `1050.s`).

## Common Operations

### Adding File Splits

When splat suggests file splits in its output, add them as subsegments:

```yaml
- name: main
  type: code
  start: 0x1050
  vram: 0x80001050
  subsegments:
    - [0x1050, asm]           # Original single file
    - [0x2000, asm]           # Add split at suggested offset
    - [0x3000, asm]           # Another split
```

### Renaming Files

Add or modify the third element (name). Names with slashes create subdirectories:

```yaml
subsegments:
  - [0x1050, asm]                    # Default: "1050.s"
  - [0x2000, asm, player]            # "player.s"
  - [0x3000, asm, physics/movement]  # "physics/movement.s"
```

### Converting ASM to C

Change file type from `asm` to `c` to begin decompilation:

```yaml
subsegments:
  - [0x2000, c, player]  # Changed from asm to c
```

This generates:
- `src/player.c` with function stubs
- Separate `.s` files per function in `asm/nonmatchings/player/`

### Adding BSS Size

```yaml
- name: main
  type: code
  start: 0x1050
  vram: 0x80001050
  bss_size: 0x7DAC0
  subsegments:
    - [0x1050, asm]
    - { start: 0xB1BD0, type: bss, vram: 0x800E2E00 }
```

### Organizing Libultra Files

```yaml
subsegments:
  - [0xA0CD0, asm, libultra/osContInit]
  - [0xA0D40, asm, libultra/osContStartReadData]
  - [0xA0E00, asm, libultra/__osViSwapContext]
```

## Data Section Types: Dot vs No-Dot

| Type | Extracted? | Output |
|------|------------|--------|
| `data` | Yes | Standalone .data.s file |
| `.data` | No | From compiled C object |
| `rodata` | Yes | Separate .rodata.s, uses INCLUDE_RODATA |
| `.rodata` | Yes | Migrated into function .s files (default) |

The `.rodata` behavior depends on `migrate_rodata_to_functions` (default: true). When enabled, rodata symbols are placed in each function's .s file.

## N64 Images

Format: `[start, type, name, width, height]` (CI images add palette as 6th element)

```yaml
segments:
  - [0x10000, rgba16, texture, 64, 64]
  - [0x30000, ci8, sprite, 32, 32, sprite_pal]
  - [0x30800, palette, sprite_pal]
```

**Types:** `i4`, `i8`, `ia4`, `ia8`, `ia16`, `ci4`, `ci8`, `rgba16`, `rgba32`

CI images default to a palette with the same name if not specified.

## Symbol Files

### symbol_addrs.txt

Define symbols to guide disassembly:

```ini
symbol_name = address; // option1:value1 option2:value2
```

```ini
main = 0x80000400; // type:func size:0x100
gGameState = 0x80200000; // type:u32 size:0x400
stringData = 0x80300000; // type:asciz
```

**Common attributes:**
- `type` - `func`, `jtbl`, `u8`/`s8`, `u16`/`s16`, `u32`/`s32`, `f32`, `asciz`
- `size` - Size in bytes
- `rom` - ROM offset (required for overlays with same VRAM)
- `segment` - Segment name (disambiguates same VRAM)
- `name_end` - Emit symbol at end (e.g., `name_end:dataEnd`)

**Boolean attributes:** `defined`, `ignore`, `force_migration`, `force_not_migration`

### Overlay Symbols

When multiple segments share the same VRAM, use `rom` or `segment`:

```ini
battle_func = 0x80500000; // type:func rom:0x100000 segment:battle
menu_func = 0x80500000; // type:func rom:0x150000 segment:menu
```

### vram_classes

Reduce duplication for overlays sharing VRAM:

```yaml
vram_classes:
  - [battle, 0x80200000]
  - [menu, 0x80200000]

segments:
  - name: battle_overlay
    type: code
    start: 0x100000
    vram_class: battle
```

## Advanced Reference

- **[references/OPTIONS.md](references/OPTIONS.md)** - All configuration options
- **[references/SEGMENTS.md](references/SEGMENTS.md)** - Complete segment reference
- **[references/SYMBOLS.md](references/SYMBOLS.md)** - Symbol files, reloc_addrs, vram_classes
