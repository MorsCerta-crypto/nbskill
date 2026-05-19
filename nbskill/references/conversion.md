# Conversion Reference

Use conversion tools when a Python module should become an nbdev notebook source.
Keep this out of the main skill path unless the task is specifically about converting `.py` files.

## `py2nb`

`py2nb` accepts either one Python file or a folder of Python files.

```bash
uv run py2nb path/to/module.py --nbs_path nbs
uv run py2nb path/to/python_folder --nbs_path nbs
```

For one file, `dest` can point at the exact notebook to create:

```bash
uv run py2nb path/to/module.py --dest nbs/module.ipynb
```

For a folder, `py2nb` searches recursively by default and writes one notebook per `.py` file under `nbs_path`, preserving the folder tree:

```bash
uv run py2nb src_package --nbs_path nbs/from_py
```

Useful options:

- `recursive=False`: only convert Python files directly in the folder.
- `maxdepth=N`: limit recursive folder depth.
- `preserve_tree=False`: flatten output notebooks into `nbs_path`.
- `class_lines` and `method_lines`: control when large classes have long methods split into `@patch` cells.

`py2nb` is the preferred conversion entry point for both files and folders.
