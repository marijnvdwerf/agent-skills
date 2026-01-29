# Splat YAML Segments Reference

Complete reference for segments and vram_classes in splat.yaml.

## VRAM Classes

Define reusable VRAM addresses for overlays and complex layouts.

### Format

**Dictionary form:**
```yaml
vram_classes:
  - name: main
    vram: 0x80000000
  - name: overlay1
    vram: 0x80100000
    vram_symbol: overlay1_VRAM
  - name: overlay2
    vram: 0x80100000
    follows_classes: [overlay1]
```

**List form (shorthand):**
```yaml
vram_classes:
  - [main, 0x80000000]
  - [overlay1, 0x80100000]
```

### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | YES | Class identifier |
| `vram` | int | YES | VRAM address |
| `vram_symbol` | string | NO | Linker symbol (auto if follows_classes) |
| `follows_classes` | list | NO | Classes this must follow |

## Segment Properties

### Universal Properties

These properties are inherited from the base `Segment` class and available to **all segment types**:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `start` | hex/int or `auto` | - | **REQUIRED**. ROM offset |
| `type` | string | - | **REQUIRED**. Segment type |
| `name` | string | derived | Segment identifier |
| `vram` | hex/int | None | VRAM start address |
| `vram_class` | string | None | Reference to vram_class |
| `vram_symbol` | string | None | Custom linker symbol name |
| `follows_vram` | string | None | Follow another segment in VRAM |
| `align` | int | None | ROM alignment |
| `subalign` | int | global | VRAM sub-alignment (top-level only) |
| `extract` | bool | True | Whether to extract/split this segment |
| `dir` | string | "" | Output directory |
| `section_order` | list | global | Section order (.text, .data, .rodata, .bss) |
| `find_file_boundaries` | bool | global | Find file split boundaries |
| `symbol_name_format` | string | global | Symbol name format (with ROM) |
| `symbol_name_format_no_rom` | string | global | Symbol name format (without ROM) |
| `pair_segment` | string | None | Name of paired segment |
| `bss_contains_common` | bool | global | BSS contains common symbols |
| `linker_entry` | bool | True | Include in linker script |
| `linker_section` | string | None | Override linker section name |
| `linker_section_order` | string | None | Override linker section ordering |
| `ld_fill_value` | int | global | Linker fill value |
| `ld_align_segment_start` | int | global | Segment start alignment |
| `suggestion_rodata_section_start` | bool | global | Suggest rodata section starts |
| `exclusive_ram_id` | string | None | Exclusive RAM ID |

**Important notes:**
- **Mutually exclusive**: `vram`, `vram_class`, and `follows_vram` cannot be used together
- **Top-level only**: `subalign`, `ld_fill_value`, `ld_align_segment_start` only apply to top-level segments
- Most properties default to global options values

### Type-Specific Properties

Only a few properties are specific to certain segment types:

**Code segments (`code`):**
| Property | Type | Description |
|----------|------|-------------|
| `bss_size` | int | Total BSS section size |
| `subsegments` | list | **REQUIRED** - List of subsegments |

**Code subsegments (`asm`, `c`, `cpp`, `data`, `rodata`, `bss`, etc.):**
| Property | Type | Description |
|----------|------|-------------|
| `str_encoding` | string | String encoding for disassembly |
| `detect_redundant_function_end` | bool | Detect redundant function endings (IDO) |

**Data/rodata segments when used as groups:**
| Property | Type | Description |
|----------|------|-------------|
| `subsegments` | list | Optional list of subsegments |

**Library segments (`lib`):**
| Property | Type | Description |
|----------|------|-------------|
| `object` | string | **REQUIRED** - Object file name |
| `section` | string | Linker section (default: `.text`) |

**Binary inclusion (`textbin`, `databin`, `rodatabin`):**
| Property | Type | Description |
|----------|------|-------------|
| `use_src_path` | bool | Use src_path instead of data_path |

**N64 image segments (`ci4`, `ci8`, `i4`, `i8`, `ia4`, `ia8`, `ia16`, `rgba16`, `rgba32`):**
| Property | Type | Description |
|----------|------|-------------|
| `width` | int | **REQUIRED** - Image width in pixels (list form: 4th element) |
| `height` | int | **REQUIRED** - Image height in pixels (list form: 5th element) |
| `flip_x` | bool | Flip image horizontally (dict only) |
| `flip_y` | bool | Flip image vertically (dict only) |

**N64 color-indexed images (`ci4`, `ci8`):**
| Property | Type | Description |
|----------|------|-------------|
| `palettes` | list/string | Palette names or global_ids (list form: 6th element) |

**Default palette behavior:** If no palette is specified, automatically uses a palette segment with the same name as the CI image.

**N64 palette segments (`palette`):**
| Property | Type | Description |
|----------|------|-------------|
| `palette_size` | int | Size in bytes (0x20, 0x40, 0x80, 0x100, 0x200) |
| `global_id` | string | Global identifier for cross-segment palette references |

**N64 graphics segments (`gfx`, `vtx`):**
| Property | Type | Description |
|----------|------|-------------|
| `data_only` | bool | Output data-only format |

## Common Segment Types

### Code/Assembly Types

| Type | Description | Output |
|------|-------------|--------|
| `asm` | Disassemble as assembly | Splat overwrites file |
| `hasm` | Hand-written assembly | Splat preserves file |
| `asmtu` | Assembly translation unit | All sections together |
| `c` | C source file | Generate .c stub + function .s files |
| `cpp` | C++ source file | Generate .cpp stub + function .s files |
| `code` | Container for subsegments | No direct output |

### Data Types

| Type | Extracted | Output |
|------|-----------|--------|
| `data` | Yes | Standalone .data.s file |
| `.data` | No | From compiled object |
| `sdata` / `.sdata` | Yes/No | Small data section |
| `rodata` | Yes | Separate .rodata.s, uses INCLUDE_RODATA |
| `.rodata` / `.rdata` | Yes | Migrated into function .s files (default) |
| `bss` / `.bss` | No | Linker symbol only |
| `sbss` / `.sbss` | No | Small BSS linker symbol |

### Special Types

| Type | Description |
|------|-------------|
| `header` | Platform-specific ROM header |
| `bin` | Raw binary data |
| `pad` | Zero-filled padding (no output file) |
| `lib` | Link to library object |
| `linker_offset` | Linker symbol offset |
| `textbin` / `databin` / `rodatabin` | Binary with incbin |
| `gcc_except_table` | Exception handler table |

## Platform-Specific Segment Types

### N64 (Nintendo 64)

**Image Formats:**

All N64 images support both list and dictionary syntax. List form: `[start, type, name, width, height]`

| Type | Bits/Pixel | Size Formula | Description |
|------|-----------|--------------|-------------|
| `i4` | 4 | width × height ÷ 2 | Intensity 4-bit (grayscale) |
| `i8` | 8 | width × height | Intensity 8-bit (grayscale) |
| `ia4` | 4 | width × height ÷ 2 | Intensity+Alpha 4-bit |
| `ia8` | 8 | width × height | Intensity+Alpha 8-bit |
| `ia16` | 16 | width × height × 2 | Intensity+Alpha 16-bit |
| `ci4` | 4 | width × height ÷ 2 | Color-indexed 4-bit (+ palette) |
| `ci8` | 8 | width × height | Color-indexed 8-bit (+ palette) |
| `rgba16` | 16 | width × height × 2 | RGBA 16-bit |
| `rgba32` | 32 | width × height × 4 | RGBA 32-bit |

**Color-Indexed (CI) Images:** Require palette segments. Default uses palette with same name. Can reference multiple palettes (exports one PNG per palette) by name or `global_id`.

**Palettes:** Valid sizes: 0x20, 0x40, 0x80, 0x100, 0x200 bytes. Each entry is 2 bytes (16-bit RGBA).

**Other N64 Types:**
- `gfx` - F3DEX display lists
- `vtx` - Vertex data (16 bytes/vertex)
- `mio0` / `yay0` - Compressed data
- `ipl3` - IPL3 bootcode
- `rsp` - RSP microcode
- `palette` - Color palette

### PSX / PS2

- `header` (PSX) - PS-X EXE header
- `ctor`, `lit4`, `lit8`, `vtables` (PS2) - C++ sections

## Format Examples

### Basic Formats

```yaml
segments:
  # List form: [start, type, name]
  - [0x0, header, header]
  - [0x1000, asm, boot]
  - [0x8000]              # End marker (required for final segment)

  # Dictionary form: for vram, bss_size, subsegments, etc.
  - name: main
    type: code
    start: 0x1050
    vram: 0x80001050
    bss_size: 0x7DAC0
    subsegments:
      - [0x1050, asm]
      - [0x2000, c, player]
      - [0x3000, .rodata, player]
      - { start: 0xB1BD0, type: bss, vram: 0x800E2E00 }
```

### N64 Images

```yaml
segments:
  # Format: [start, type, name, width, height]
  - [0x10000, rgba16, texture, 32, 32]

  # CI with palette: [start, type, name, width, height, palette_name]
  - [0x11000, ci8, sprite, 64, 64, sprite_pal]
  - [0x12000, palette, sprite_pal]

  # CI without explicit palette uses same-name palette automatically
  - [0x13000, ci4, character, 32, 32]
  - [0x13200, palette, character]

  # Multiple palettes (exports multiple PNGs)
  - name: multi_tex
    type: ci4
    start: 0x20000
    width: 32
    height: 32
    palettes: [red_pal, blue_pal]

  # Shared palette via global_id
  - name: common_pal
    type: palette
    start: 0x1000
    global_id: shared
  - [0x2000, ci8, tex1, 64, 64, shared]
  - [0x3000, ci8, tex2, 32, 32, shared]
```

### VRAM Classes

```yaml
vram_classes:
  - [main, 0x80000000]
  - [overlay, 0x80100000]

segments:
  - name: main_code
    type: code
    start: 0x1000
    vram_class: main
    subsegments: [...]
```

### Rodata Migration

```yaml
# With migrate_rodata_to_functions: true (default)
# Use .rodata - symbols migrated into function .s files
subsegments:
  - [0x1000, c, main]
  - [0x2000, .rodata, main]

# With migrate_rodata_to_functions: false
# Use rodata - separate .rodata.s file with INCLUDE_RODATA
subsegments:
  - [0x1000, c, main]
  - [0x2000, rodata, main]
```

## Notes

- Segment offsets must be in ascending order
- Final segment requires an end marker `[offset]`
- `vram`, `vram_class`, and `follows_vram` are mutually exclusive
- BSS subsegments require both `type: bss` and `vram` address
- CI images default to a palette with the same name if not specified
