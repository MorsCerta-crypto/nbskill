# Conversion Reference

Use the MCP `convert` tool when Python modules should become nbdev notebook source.
Keep this out of the main skill path unless the task is specifically about converting `.py` files.

## `convert`

`convert` accepts one Python file, a folder of Python files, or a pure-Python project/package.

```python
convert(path="path/to/module.py", mode="notebook", nbs_path="nbs")
convert(path="path/to/python_folder", mode="notebook", nbs_path="nbs")
convert(path="path/to/python_project", mode="project", dest=".")
```

For one file, `dest` can point at the exact notebook to create:

```python
convert(path="path/to/module.py", dest="nbs/module.ipynb")
```

For a folder, `convert` searches recursively by default and writes one notebook per `.py` file under `nbs_path`, preserving the folder tree:

```python
convert(path="src_package", nbs_path="nbs/from_py")
```

Useful options:

- `recursive=False`: only convert Python files directly in the folder.
- `maxdepth=N`: limit recursive folder depth.
- `preserve_tree=False`: flatten output notebooks into `nbs_path`.
- `class_lines` and `method_lines`: control when large classes have long methods split into `@patch` cells.

`convert` is the public conversion entry point.
