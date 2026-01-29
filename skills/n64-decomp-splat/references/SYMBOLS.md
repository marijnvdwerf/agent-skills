# Symbol Files Reference

Complete reference for `symbol_addrs.txt` and related symbol configuration.

## symbol_addrs.txt Format

```ini
symbol_name = address; // option1:value1 option2:value2
```

**Rules:**
- One symbol per line, exactly one semicolon
- Comments with `//` (inline or full line)
- Address in hex (`0x80001050`) or decimal
- Options are space-separated `key:value` pairs (no spaces around `:`)

**Example:**
```ini
osInitialize = 0x801378C0; // type:func
gGameState = 0x80200000; // type:u32 size:0x100 rom:0x12345
```

## Symbol Attributes

### Core Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `type` | string | Override auto-detection (see Type Values below) |
| `size` | int | Size in bytes |
| `rom` | int | ROM offset (required for overlays with same VRAM) |
| `segment` | string | Segment name from yaml (disambiguates same VRAM) |
| `name_end` | string | Emit symbol at end of data (e.g., `name_end:rspbootTextEnd`) |
| `filename` | string | Override filename for symbols with invalid chars |
| `align` | int | Emit `.align` directive (must be power of 2, address must be aligned) |

### Type Values

**Code:**
- `func` - Functions
- `jtbl` - Jump tables
- `jtbl_label` - Jump table labels (inside functions)
- `label` - Branch labels (inside functions)

**Data:**
- `s8`, `u8` - Byte (`.byte`)
- `s16`, `u16` - Halfword (`.short`)
- `s32`, `u32` - Word (`.word`) - default
- `s64`, `u64` - Doubleword
- `f32`, `Vec3f` - Float (`.float`)
- `f64` - Double (`.double`)
- `asciz`, `char*`, `char` - C string (`.asciz`)

Custom types starting with uppercase default to `.word`.

### Boolean Attributes

All accept: `true`/`false`, `yes`/`no`, `on`/`off`

| Attribute | Default | Description |
|-----------|---------|-------------|
| `defined` | false | Force symbol to be defined (won't appear in undefined_syms_auto.txt) |
| `ignore` | false | Prevent address from being symbolized. Combine with `size` for ranges |
| `force_migration` | false | Force rodata migration to function (requires reference) |
| `force_not_migration` | false | Prevent rodata migration |
| `allow_addend` | - | Allow symbol references with addends |
| `dont_allow_addend` | - | Disallow addend references |
| `can_reference` | true | Whether symbol can reference other symbols |
| `can_be_referenced` | true | Whether other symbols can reference this one |
| `allow_duplicated` | false | Allow duplicate VRAM/name (must be on ALL duplicates) |

### Rodata Migration

| Attribute | Description |
|-----------|-------------|
| `function_owner` | Function name that owns this rodata (overrides heuristics) |
| `force_migration` | Force migration to referencing function |
| `force_not_migration` | Keep rodata separate |

Only active when `migrate_rodata_to_functions: true` (default).

## Common Patterns

**Function:**
```ini
main = 0x80000400; // type:func size:0x100
```

**Data array:**
```ini
gLevelTable = 0x80200000; // type:u32 size:0x400
```

**Overlay symbol (same VRAM, different ROM):**
```ini
battle_init = 0x80500000; // type:func rom:0x100000 segment:battle
menu_init = 0x80500000; // type:func rom:0x150000 segment:menu
```

**RSP data with end marker:**
```ini
rspbootTextStart = 0x80084690; // name_end:rspbootTextEnd
```

**Ignore address range:**
```ini
D_80000000 = 0x80000000; // ignore:true size:0x10
```

**String with forced migration:**
```ini
helpString = 0x80450000; // type:asciz function_owner:printHelp
```

**Texture (no symbol references):**
```ini
mario_texture = 0x80300000; // can_reference:false size:0x800 align:0x8
```

## reloc_addrs.txt Format

Override automatic relocations when disassembler gets them wrong.

```ini
rom:0x04B440 reloc:MIPS_HI16 symbol:some_array addend:-0x4
```

| Attribute | Description |
|-----------|-------------|
| `rom` | ROM address of instruction/data to fix |
| `symbol` | Symbol to reference |
| `reloc` | Relocation type |
| `addend` | Optional offset (positive or negative) |

### Relocation Types

**Code (instructions):**
- `MIPS_HI16` - `%hi()` operator
- `MIPS_LO16` - `%lo()` operator
- `MIPS_GPREL16` - `%gp_rel()` operator
- `MIPS_26` - `jal`/`j` instructions
- `MIPS_PC16` - Branch instructions

**Data:**
- `MIPS_32` - `.word` reference
- `MIPS_GPREL32` - `.gpword` reference

**Special:**
- `MIPS_NONE` - No relocation (use raw value)

### Common Use Cases

**Negative array offset:**
```c
// C: return some_array[index - 1];
// Compiler emits: lui $v0, %hi(some_array - 0x4)
```
```ini
rom:0x0004 reloc:MIPS_HI16 symbol:some_array addend:-0x4
rom:0x0010 reloc:MIPS_LO16 symbol:some_array addend:-0x4
```

**Segment symbols in code:**
```ini
rom:0x000C reloc:MIPS_HI16 symbol:segment_menu_ROM_START
rom:0x0010 reloc:MIPS_LO16 symbol:segment_menu_ROM_START
```

**Segment symbols in data:**
```ini
rom:0x0100 reloc:MIPS_32 symbol:segment_menu_ROM_START
```

## YAML Configuration

```yaml
options:
  # Single file
  symbol_addrs_path: symbol_addrs.txt

  # Multiple files
  symbol_addrs_path:
    - symbols/functions.txt
    - symbols/data.txt
    - symbols/libultra.txt

  reloc_addrs_path: reloc_addrs.txt
```

## vram_classes

Define reusable VRAM addresses for overlays:

```yaml
vram_classes:
  - { name: battle, vram: 0x80200000 }
  - { name: menu, vram: 0x80200000, vram_symbol: menu_VRAM }
  - { name: world, vram: 0x80300000, follows_classes: [battle] }

segments:
  - name: battle_overlay
    type: code
    start: 0x100000
    vram_class: battle
    subsegments: [...]
```

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Class identifier |
| `vram` | Yes | VRAM address for disassembly |
| `vram_symbol` | No | Linker symbol name |
| `follows_classes` | No | Classes this must follow in memory |

Requires `ld_use_symbolic_vram_addresses: true` for linker script symbols.
