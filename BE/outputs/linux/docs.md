# linux — Auto-generated documentation

## Overview

Repository: torvalds/linux

Total Files: 68318
Total Directories: 4205

Analyzed 25 Python files.

## File tree

- root (12 files)
- Documentation (2 files)
- Documentation/ABI (1 files)
- Documentation/ABI/obsolete (25 files)
- Documentation/ABI/removed (16 files)
- Documentation/ABI/stable (49 files)
- Documentation/ABI/testing (95 files)


## Code Statistics

- **Total Functions**: 182
- **Total Classes**: 28
- **Total Relationships**: 805

## API / Code Context Graph

### Functions and Classes


#### 📄 `Documentation/conf.py`

- **function** `config_init` (line 59)
- **function** `have_command` (line 130)
- **function** `get_cline_version` (line 300)
- **function** `setup` (line 593)

#### 📄 `Documentation/sphinx/automarkup.py`

- **function** `markup_refs` (line 69)
- **function** `failure_seen` (line 115)
- **function** `note_failure` (line 117)
- **function** `markup_func_ref_sphinx3` (line 124)
- **function** `markup_c_ref` (line 146)
- **function** `markup_doc_ref` (line 183)
- **function** `markup_abi_ref` (line 199)
- **function** `add_and_resolve_xref` (line 217)
- **function** `markup_abi_file_ref` (line 249)
- **function** `get_c_namespace` (line 253)
- **function** `markup_git` (line 262)
- **function** `auto_markup` (line 273)
- **function** `text_but_not_a_reference` (line 276)
- **function** `setup` (line 301)

#### 📄 `Documentation/sphinx/kernel_abi.py`

- **function** `get_kernel_abi` (line 57)
- **function** `setup` (line 73)
- **function** `run` (line 98)
- **function** `do_parse` (line 171)
- **class** `KernelCmd` (line 83)

#### 📄 `Documentation/sphinx/kernel_feat.py`

- **function** `ErrorString` (line 45)
- **function** `setup` (line 50)
- **function** `warn` (line 72)
- **function** `run` (line 78)
- **function** `nestedParse` (line 117)
- **class** `KernelFeat` (line 59)

#### 📄 `Documentation/sphinx/kernel_include.py`

- **function** `ErrorString` (line 108)
- **function** `read_rawtext` (line 151)
- **function** `apply_range` (line 170)
- **function** `xref_text` (line 206)
- **function** `literal` (line 267)
- **function** `code` (line 298)
- **function** `run` (line 316)
- **function** `check_missing_refs` (line 392)
- **function** `merge_xref_info` (line 423)
- **function** `init_xref_docs` (line 431)
- **function** `setup` (line 437)
- **class** `KernelInclude` (line 113)

#### 📄 `Documentation/sphinx/kerneldoc.py`

- **function** `cmd_str` (line 54)
- **function** `handle_args` (line 95)
- **function** `run_cmd` (line 193)
- **function** `parse_msg` (line 221)
- **function** `run_kdoc` (line 247)
- **function** `run` (line 265)
- **function** `do_parse` (line 283)
- **function** `setup_kfiles` (line 287)
- **function** `setup` (line 300)
- **class** `KernelDocDirective` (line 77)

#### 📄 `Documentation/sphinx/kfigure.py`

- **function** `which` (line 74)
- **function** `mkdir` (line 86)
- **function** `file2literal` (line 90)
- **function** `isNewer` (line 96)
- **function** `pass_handle` (line 105)
- **function** `setup` (line 128)
- **function** `setupTools` (line 168)
- **function** `convert_image` (line 244)
- **function** `dot2format` (line 339)
- **function** `svg2pdf` (line 365)
- **function** `svg2pdf_by_rsvg` (line 406)
- **function** `visit_kernel_image` (line 436)
- **function** `run` (line 456)
- **function** `visit_kernel_figure` (line 473)
- **function** `run` (line 492)
- **function** `visit_kernel_render` (line 511)
- **function** `run` (line 581)
- **function** `build_node` (line 584)
- **function** `add_kernel_figure_to_std_domain` (line 626)
- **class** `kernel_image` (line 444)
- **class** `KernelImage` (line 448)
- **class** `kernel_figure` (line 481)
- **class** `KernelFigure` (line 484)
- **class** `kernel_render` (line 556)
- **class** `KernelRender` (line 560)

#### 📄 `Documentation/sphinx/load_config.py`

- **function** `loadConfig` (line 10)

#### 📄 `Documentation/sphinx/maintainers_include.py`

- **function** `ErrorString` (line 28)
- **function** `setup` (line 33)
- **function** `parse_maintainers` (line 45)
- **function** `run` (line 175)
- **class** `MaintainersInclude` (line 41)

#### 📄 `Documentation/sphinx/parser_yaml.py`

- **function** `rst_parse` (line 63)
- **function** `parse` (line 100)
- **function** `setup` (line 112)
- **class** `YamlParser` (line 29)

#### 📄 `Documentation/sphinx/rstFlatTable.py`

- **function** `setup` (line 58)
- **function** `c_span` (line 72)
- **function** `r_span` (line 83)
- **function** `run` (line 113)
- **function** `__init__` (line 141)
- **function** `buildTableNode` (line 146)
- **function** `buildTableRowNode` (line 189)
- **function** `raiseError` (line 207)
- **function** `parseFlatTableNode` (line 215)
- **function** `roundOffTableDefinition` (line 228)
- **function** `pprint` (line 295)
- **function** `parseRowItem` (line 316)
- **function** `parseCellItem` (line 350)
- **class** `rowSpan` (line 95)
- **class** `colSpan` (line 96)
- **class** `FlatTable` (line 100)
- **class** `ListTableBuilder` (line 136)

#### 📄 `Documentation/sphinx/translations.py`

- **function** `apply` (line 37)
- **function** `process_languages` (line 69)
- **function** `setup` (line 91)
- **class** `LanguagesNode` (line 31)
- **class** `TranslationsTransform` (line 34)

#### 📄 `drivers/comedi/drivers/ni_routing/tools/convert_csv_to_c.py`

- **function** `c_to_o` (line 11)
- **function** `routedict_to_structinit_single` (line 17)
- **function** `routedict_to_routelist_single` (line 63)
- **function** `__init__` (line 224)
- **function** `to_listinit` (line 227)
- **function** `save` (line 277)
- **function** `__init__` (line 412)
- **function** `to_structinit` (line 415)
- **function** `save` (line 466)
- **class** `DeviceRoutes` (line 116)
- **class** `RouteValues` (line 289)

#### 📄 `drivers/comedi/drivers/ni_routing/tools/convert_py_to_csv.py`

- **function** `iter_src_values` (line 14)
- **function** `iter_src` (line 17)
- **function** `create_csv` (line 21)
- **function** `to_csv` (line 51)

#### 📄 `drivers/comedi/drivers/ni_routing/tools/csv_collection.py`

- **function** `__init__` (line 14)
- **class** `CSVCollection` (line 5)

#### 📄 `drivers/comedi/drivers/ni_routing/tools/make_blank_csv.py`

- **function** `to_csv` (line 12)

#### 📄 `drivers/comedi/drivers/ni_routing/tools/ni_names.py`

- **function** `get_ni_names` (line 28)

#### 📄 `drivers/gpu/drm/msm/registers/gen_header.py`

- **function** `__init__` (line 16)
- **function** `__init__` (line 20)
- **function** `has_name` (line 24)
- **function** `names` (line 30)
- **function** `dump` (line 33)
- **function** `dump_pack_struct` (line 47)
- **function** `__init__` (line 51)
- **function** `ctype` (line 75)
- **function** `tab_to` (line 112)
- **function** `mask` (line 118)
- **function** `field_name` (line 121)
- **function** `indices_varlist` (line 135)
- **function** `indices_prototype` (line 138)
- **function** `indices_strides` (line 142)
- **function** `is_number` (line 148)
- **function** `sanitize_variant` (line 155)
- **function** `__init__` (line 161)
- **function** `get_address_field` (line 171)
- **function** `dump_regpair_builder` (line 177)
- **function** `dump_pack_struct` (line 215)
- **function** `dump` (line 267)
- **function** `__init__` (line 297)
- **function** `index_ctype` (line 330)
- **function** `indices` (line 337)
- **function** `total_offset` (line 349)
- **function** `dump` (line 357)
- **function** `dump_pack_struct` (line 380)
- **function** `dump_regpair_builder` (line 383)
- **function** `__init__` (line 387)
- **function** `indices` (line 406)
- **function** `total_offset` (line 415)
- **function** `reg_offset` (line 421)
- **function** `dump` (line 427)
- **function** `dump_pack_struct` (line 443)
- **function** `dump_regpair_builder` (line 447)
- **function** `dump_py` (line 450)
- **function** `__init__` (line 455)
- **function** `error` (line 478)
- **function** `prefix` (line 482)
- **function** `parse_field` (line 492)
- **function** `parse_varset` (line 522)
- **function** `parse_variants` (line 529)
- **function** `add_all_variants` (line 549)
- **function** `add_all_usages` (line 566)
- **function** `do_validate` (line 575)
- **function** `do_parse` (line 611)
- **function** `parse` (line 627)
- **function** `parse_reg` (line 633)
- **function** `start_element` (line 670)
- **function** `end_element` (line 722)
- **function** `character_data` (line 745)
- **function** `dump_reg_usages` (line 748)
- **function** `has_variants` (line 789)
- **function** `dump` (line 792)
- **function** `dump_regs_py` (line 810)
- **function** `dump_reg_variants` (line 820)
- **function** `dump_structs` (line 896)
- **function** `dump_c` (line 904)
- **function** `dump_c_defines` (line 949)
- **function** `dump_c_pack_structs` (line 954)
- **function** `dump_py_defines` (line 959)
- **function** `main` (line 978)
- **class** `Error` (line 15)
- **class** `Enum` (line 19)
- **class** `Field` (line 50)
- **class** `Bitset` (line 160)
- **class** `Array` (line 296)
- **class** `Reg` (line 386)
- **class** `Parser` (line 454)

#### 📄 `drivers/tty/vt/gen_ucs_fallback_table.py`

- **function** `generate_fallback_map` (line 36)
- **function** `get_special_overrides` (line 63)
- **function** `organize_by_pages` (line 210)
- **function** `compress_ranges` (line 229)

### Relationships

- `config_init` → `setup` (calls)
- `setup` → `config_init` (calls)
- `markup_refs` → `markup_func_ref_sphinx3` (calls)
- `markup_refs` → `markup_c_ref` (calls)
- `markup_refs` → `markup_doc_ref` (calls)
- `markup_refs` → `markup_abi_ref` (calls)
- `markup_refs` → `markup_abi_file_ref` (calls)
- `markup_refs` → `markup_git` (calls)
- `failure_seen` → `note_failure` (calls)
- `failure_seen` → `markup_func_ref_sphinx3` (calls)
- `failure_seen` → `markup_c_ref` (calls)
- `failure_seen` → `add_and_resolve_xref` (calls)
- `note_failure` → `failure_seen` (calls)
- `note_failure` → `markup_func_ref_sphinx3` (calls)
- `note_failure` → `markup_c_ref` (calls)
- `note_failure` → `add_and_resolve_xref` (calls)
- `markup_func_ref_sphinx3` → `failure_seen` (calls)
- `markup_func_ref_sphinx3` → `note_failure` (calls)
- `markup_func_ref_sphinx3` → `markup_c_ref` (calls)
- `markup_func_ref_sphinx3` → `add_and_resolve_xref` (calls)
- `markup_c_ref` → `markup_doc_ref` (calls)
- `markup_c_ref` → `add_and_resolve_xref` (calls)
- `markup_doc_ref` → `markup_abi_ref` (calls)
- `markup_doc_ref` → `add_and_resolve_xref` (calls)
- `markup_abi_ref` → `add_and_resolve_xref` (calls)
- `add_and_resolve_xref` → `markup_abi_ref` (calls)
- `add_and_resolve_xref` → `markup_abi_file_ref` (calls)
- `add_and_resolve_xref` → `get_c_namespace` (calls)
- `markup_abi_file_ref` → `markup_abi_ref` (calls)
- `markup_abi_file_ref` → `get_c_namespace` (calls)
- `markup_abi_file_ref` → `markup_git` (calls)
- `markup_abi_file_ref` → `auto_markup` (calls)
- `markup_abi_file_ref` → `text_but_not_a_reference` (calls)
- `get_c_namespace` → `markup_git` (calls)
- `get_c_namespace` → `auto_markup` (calls)
- `get_c_namespace` → `text_but_not_a_reference` (calls)
- `markup_git` → `markup_refs` (calls)
- `markup_git` → `get_c_namespace` (calls)
- `markup_git` → `auto_markup` (calls)
- `markup_git` → `text_but_not_a_reference` (calls)
- `markup_git` → `setup` (calls)
- `auto_markup` → `markup_refs` (calls)
- `auto_markup` → `get_c_namespace` (calls)
- `auto_markup` → `text_but_not_a_reference` (calls)
- `auto_markup` → `setup` (calls)
- `text_but_not_a_reference` → `markup_refs` (calls)
- `text_but_not_a_reference` → `auto_markup` (calls)
- `text_but_not_a_reference` → `setup` (calls)
- `setup` → `auto_markup` (calls)
- `get_kernel_abi` → `setup` (calls)
- `setup` → `get_kernel_abi` (calls)
- `setup` → `run` (calls)
- `run` → `get_kernel_abi` (calls)
- `ErrorString` → `setup` (calls)
- `ErrorString` → `warn` (calls)
- `ErrorString` → `run` (calls)
- `setup` → `warn` (calls)
- `setup` → `run` (calls)
- `warn` → `run` (calls)
- `run` → `nestedParse` (calls)
- `ErrorString` → `literal` (calls)
- `ErrorString` → `code` (calls)
- `ErrorString` → `run` (calls)
- `read_rawtext` → `ErrorString` (calls)
- `read_rawtext` → `apply_range` (calls)
- `apply_range` → `xref_text` (calls)
- `xref_text` → `apply_range` (calls)
- `xref_text` → `literal` (calls)
- `xref_text` → `code` (calls)
- `literal` → `code` (calls)
- `code` → `run` (calls)
- `check_missing_refs` → `merge_xref_info` (calls)
- `check_missing_refs` → `init_xref_docs` (calls)
- `merge_xref_info` → `check_missing_refs` (calls)
- `merge_xref_info` → `init_xref_docs` (calls)
- `merge_xref_info` → `setup` (calls)
- `init_xref_docs` → `check_missing_refs` (calls)
- `init_xref_docs` → `merge_xref_info` (calls)
- `init_xref_docs` → `setup` (calls)
- `setup` → `check_missing_refs` (calls)
- `setup` → `merge_xref_info` (calls)
- `setup` → `init_xref_docs` (calls)
- `run_cmd` → `parse_msg` (calls)
- `parse_msg` → `run_kdoc` (calls)
- `parse_msg` → `do_parse` (calls)
- `run_kdoc` → `cmd_str` (calls)
- `run_kdoc` → `handle_args` (calls)
- `run_kdoc` → `run_cmd` (calls)
- `run_kdoc` → `parse_msg` (calls)
- `run_kdoc` → `run` (calls)
- `run_kdoc` → `do_parse` (calls)
- `run` → `cmd_str` (calls)
- `run` → `handle_args` (calls)
- `run` → `run_cmd` (calls)
- `run` → `run_kdoc` (calls)
- `run` → `do_parse` (calls)
- `run` → `setup_kfiles` (calls)
- `run` → `setup` (calls)
- `do_parse` → `setup_kfiles` (calls)
- `do_parse` → `setup` (calls)