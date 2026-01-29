# Splat YAML Options Reference

Complete reference for all options in the `options:` section of splat.yaml.

## Project Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `basename` | string | - | **REQUIRED**. Project basename for generated files |
| `platform` | string | - | **REQUIRED**. Target: `n64`, `psx`, `ps2`, `psp` |
| `compiler` | string | `IDO` | Compiler: `GCC`, `SN64`, `IDO`, `KMC`, `EGCS`, `PSYQ`, `MWCCPS2`, `EEGCC` |
| `base_path` | path | `.` | Base path for all relative paths |
| `target_path` | path | - | **REQUIRED**. Path to target binary |
| `elf_path` | path | - | Path to final ELF target |
| `endianness` | string | platform | `big` or `little` (auto-detected by platform) |
| `section_order` | list | `[.text, .data, .rodata, .bss]` | Default section order for linker |
| `is_unsupported_platform` | bool | `False` | Disable platform validation |
| `allow_segment_overrides` | bool | `False` | Allow platform segment overrides |

## Paths

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `src_path` | path | `src` | Source code directory |
| `asm_path` | path | `asm` | Assembly output directory |
| `data_path` | path | `asm/data` | Assembly data directory |
| `nonmatchings_path` | path | `asm/nonmatchings` | Unmatched function directory |
| `matchings_path` | path | `asm/matchings` | Matched function directory |
| `asset_path` | path | `assets` | Extracted asset directory |
| `build_path` | path | `build` | Build output directory |
| `cache_path` | path | `.splache` | Cache file location |
| `symbol_addrs_path` | path/list | `symbol_addrs.txt` | Symbol addresses file(s) |
| `reloc_addrs_path` | path/list | `reloc_addrs.txt` | Relocation addresses file(s) |
| `extensions_path` | path | `tools/splat_ext` | Custom extensions directory |
| `lib_path` | path | `lib` | Library files directory |
| `elf_section_list_path` | path | `elf_sections.txt` | ELF section list file |
| `hasm_in_src_path` | bool | `False` | Place hand-written assembly in src_path |

### Auto-Generated Files

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `create_undefined_funcs_auto` | bool | `True` | Generate `undefined_funcs_auto.txt` |
| `undefined_funcs_auto_path` | path | `undefined_funcs_auto.txt` | Path for undefined functions |
| `create_undefined_syms_auto` | bool | `True` | Generate `undefined_syms_auto.txt` |
| `undefined_syms_auto_path` | path | `undefined_syms_auto.txt` | Path for undefined symbols |

## Linker Script

### Basic Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ld_script_path` | path | `{basename}.ld` | Output linker script path |
| `ld_symbol_header_path` | path | - | Header file with linker symbols |
| `subalign` | int | `16` | Sub-alignment (bytes), or `null` |
| `emit_subalign` | bool | `True` | Emit SUBALIGN directive |
| `auto_link_sections` | list | `[.data, .rodata, .bss]` | Sections for automatic linking |

### Section Control

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ld_discard_section` | bool | `True` | Add wildcard discard section |
| `ld_sections_allowlist` | list | `[]` | Sections to preserve |
| `ld_sections_denylist` | list | `[]` | Sections to discard |
| `ld_wildcard_sections` | bool | `False` | Use wildcards for section linking |

### VRAM Address Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ld_use_symbolic_vram_addresses` | bool | `True` | Use symbolic VRAM addresses |
| `ld_sort_segments_by_vram_class_dependency` | bool | `False` | Sort by vram class dependencies |

### Alignment and Filling

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ld_align_segment_start` | int | `null` | Segment start alignment (bytes) |
| `ld_align_segment_vram_end` | bool | `True` | Align segment VRAM end symbols |
| `ld_align_section_vram_end` | bool | `True` | Align section VRAM end symbols |
| `ld_fill_value` | int | `0` | FILL statement value (or `null`) |
| `ld_bss_is_noload` | bool | platform | BSS in NOLOAD (`True` except PSX) |

### Advanced Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ld_legacy_generation` | bool | `False` | Don't impose section_order |
| `ld_partial_linking` | bool | `False` | Allow partial linking |
| `ld_partial_scripts_path` | path | - | Directory for partial linker scripts |
| `ld_partial_build_segments_path` | path | - | Directory for partially linked segments |
| `ld_dependencies` | bool | `False` | Generate `.d` dependency files |
| `ld_rom_start` | int | `0` | ROM address symbol offset |
| `segment_end_before_align` | bool | `False` | Place end symbol before alignment |
| `segment_symbols_style` | string | `splat` | Symbol style: `splat` or `makerom` |
| `ld_generate_symbol_per_data_segment` | bool | `False` | Generate linker symbol per data file |
| `ld_bss_contains_common` | bool | `False` | Default BSS contains common |

### GP Register

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `gp_value` | int | - | Value of `$gp` for %gp_rel relocations |
| `ld_gp_expression` | string | - | Expression for `_gp` (enables shiftable) |

## Code Generation

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `generated_c_preamble` | string | `#include "common.h"` | Code at start of `.c` files |
| `generated_s_preamble` | string | `` | Code at start of assembly files |
| `generated_macro_inc_content` | string | - | Extra content for `macro.inc` |
| `generate_asm_macros_files` | bool | `True` | Regenerate macro files each run |
| `include_asm_macro_style` | string | `default` | `default` or `maspsx_hack` |
| `generated_asm_macros_directory` | path | `include` | Directory for macro files |
| `o_as_suffix` | bool | `False` | Use `.o` as suffix vs append |

## C File Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `create_c_files` | bool | `True` | Create new `.c` files if missing |
| `auto_decompile_empty_functions` | bool | `True` | Auto-decompile empty functions |
| `do_c_func_detection` | bool | `True` | Detect matched/unmatched functions |
| `c_newline` | string | compiler | Newline character(s) in C files |
| `use_legacy_include_asm` | bool | `False` | Use longer legacy INCLUDE_ASM |
| `named_regs_for_c_funcs` | bool | `True` | Use named registers in C |

## Disassembly Options

### Symbols and File Detection

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `symbol_name_format` | string | `$VRAM` | Default symbol name format |
| `symbol_name_format_no_rom` | string | `$VRAM_$SEG` | Format without ROM address |
| `find_file_boundaries` | bool | `True` | Detect file boundaries |
| `pair_rodata_to_text` | bool | `True` | Detect rodata-to-text pairing |
| `migrate_rodata_to_functions` | bool | `True` | Migrate rodata into function .s files (use `.rodata` type) |
| `suggestion_rodata_section_start` | bool | `True` | Suggest rodata section starts |

### Assembly Macros

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `asm_inc_header` | string | compiler | Header in included asm files |
| `asm_function_macro` | string | compiler | Macro for function declarations |
| `asm_function_alt_macro` | string | compiler | Macro for alternate entry points |
| `asm_jtbl_label_macro` | string | compiler | Macro for jumptable labels |
| `asm_data_macro` | string | compiler | Macro for data symbols |
| `asm_end_label` | string | compiler | Macro for function end |
| `asm_data_end_label` | string | compiler | Macro for data symbol end |
| `asm_ehtable_label_macro` | string | compiler | Macro for exception tables |
| `asm_nonmatching_label_macro` | string | compiler | Macro for nonmatching symbols |
| `asm_emit_size_directive` | bool | compiler | Emit `.size` directive |
| `add_set_gp_64` | bool | platform | Add `.set gp=64` directive |

### Formatting and Registers

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mnemonic_ljust` | int | `11` | Left-justify mnemonics |
| `rom_address_padding` | bool | `False` | Pad ROM addresses |
| `mips_abi_gpr` | string | `o32` | GPR naming: `numeric`, `32`, `o32`, `n32`, `n64` |
| `mips_abi_float_regs` | string | `numeric` | Float naming: `numeric`, `32`, `o32`, `n32`, `n64` |
| `use_gp_rel_macro` | bool | `True` | Use %gp_rel on asm/hasm |
| `use_gp_rel_macro_nonmatching` | bool | `True` | Use %gp_rel on c functions |

### Strings and Data

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `string_encoding` | string | - | Rodata string encoding |
| `data_string_encoding` | string | - | Data string encoding |
| `rodata_string_guesser_level` | int | - | Rodata guesser (0=disabled) |
| `data_string_guesser_level` | int | - | Data guesser (0=disabled) |
| `allow_data_addends` | bool | `True` | Allow data symbols with addends |

### Other Disassembly Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `disasm_unknown` | bool | `False` | Disassemble unknown instructions |
| `detect_redundant_function_end` | bool | `True` | Detect redundant ends (IDO) |
| `disassemble_all` | bool | `False` | Disassemble all functions |
| `make_full_disasm_for_code` | bool | `False` | Emit full `.s` per code segment |
| `create_asm_dependencies` | bool | `False` | Generate `.asmproc.d` files |
| `global_vram_start` | int | - | Override global VRAM start |
| `global_vram_end` | int | - | Override global VRAM end |
| `check_consecutive_segment_types` | bool | `True` | Check non-consecutive types |
| `dump_symbols` | bool | `False` | Enable symbol dumping |

## Platform-Specific

### N64

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `header_encoding` | string | `ASCII` | ROM header encoding |
| `gfx_ucode` | string | `f3dex2` | Graphics: `f3d`, `f3db`, `f3dex`, `f3dexb`, `f3dex2` |
| `libultra_symbols` | bool | `False` | Use named libultra symbols |
| `ique_symbols` | bool | `False` | Use named iQue symbols |
| `hardware_regs` | bool | `False` | Use named hardware registers |
| `image_type_in_extension` | bool | `False` | Append type (`.ci4.png`) |

### PS2

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `align_on_branch_labels` | bool | compiler | Emit alignment on branches |

## Notes

- All paths are relative to `base_path`
- `symbol_addrs_path` and `reloc_addrs_path` accept string or list
- Options marked "compiler" or "platform" in Default column inherit from those settings
