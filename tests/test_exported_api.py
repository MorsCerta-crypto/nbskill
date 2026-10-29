from pathlib import Path

from nbskill import foundation


def test_exported_parser_preserves_notebook_cell_kinds_and_source():
    assert Path(foundation.__file__).resolve().parent == Path(__file__).resolve().parents[1]/'nbskill'
    cells = foundation.parse_cells('%%markdown\n## Invoice\n---\n%%code\namount = 42')
    assert [cell['cell_type'] for cell in cells] == ['markdown', 'code']
    assert cells[0]['source'] == '## Invoice'
    assert cells[1]['source'] == 'amount = 42'
    assert all(cell['id'] for cell in cells)
