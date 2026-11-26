from pathlib import Path

import pytest
from fastcore.nbio import mk_cell, new_nb, read_nb, write_nb

import nbskill.skill as nbs
from nbskill.core import parse_cells, source_hash
from nbskill.work import install_skill


def test_public_pyskill_surface():
    expected = {"nb_graph", "nb_arch", "impact", "trace_path", "nb_map", "generated_owner",
        "chapter_context", "symbol_context", "search_nb", "review_nb", "check_nb",
        "diff_nb", "notebook_state", "edit_nb", "exec_nb"}
    assert set(nbs.__all__) == expected


def test_symbol_context_handles_patch_and_distant_examples(tmp_path):
    nb_path = tmp_path / "00_box.ipynb"
    write_nb(new_nb([
        mk_cell("# Box", "markdown"), mk_cell("> Small container.", "markdown"),
        mk_cell("## Methods", "markdown"), mk_cell("`label` formats a box.", "markdown"),
        mk_cell("#| export\n@patch\ndef label(self: Box): return f'<{self.v}>'"),
        mk_cell("## Later", "markdown"), mk_cell("assert box.label() == '<1>'"),
    ]), nb_path)
    ctx = nbs.symbol_context("Box.label", scope=tmp_path)
    assert ctx.chapter == "Methods"
    assert ctx.examples == []
    assert ctx.distant_examples and ctx.distant_examples[0][0] == "Later"
    rep = nbs.review_nb(nb_path, include_style=False)
    assert "distant-example" in {d.code for d in rep.diagnostics}


def test_review_catches_structural_state_narrative_and_style_errors(tmp_path):
    nb_path = tmp_path / "broken.ipynb"
    write_nb(new_nb([
        mk_cell("#| default_exp broken"),
        mk_cell("### Jump", "markdown"),
        mk_cell("import os\nx = 1; z = 2"),
        mk_cell("y = later(1)"),
        mk_cell("#| eval: false\nonly_disabled = 5"),
        mk_cell("def later(v): return v + only_disabled"),
        mk_cell("#| hide\na = 1"), mk_cell("#| hide\nb = 2"),
        mk_cell("#| hide\nc = 3"), mk_cell("#| hide\nd = 4"),
        mk_cell("try:\n    1 / 0\nexcept ZeroDivisionError:\n    pass\nprint(y)"),
    ]), nb_path)
    rep = nbs.review_nb(nb_path, include_style=True)
    codes = {d.code for d in rep.diagnostics}
    assert {"missing-title-header", "heading-level-jump", "mixed-import-cell", "cell-order",
        "eval-false-dependency", "excessive-hidden-code", "hidden-implementation-run",
        "example-trailing-print", "example-try-except", "semicolon"} <= codes
    assert any(d.source == "chkstyle" and d.code == "semicolon" for d in rep.diagnostics)


def test_edit_and_exec_track_freshness_and_reject_bad_edits(tmp_path):
    nb_path = tmp_path / "flow.ipynb"
    cells = parse_cells("%%markdown\n## Calc\n---\n%%code\nbase = 20\n---\n%%code\ntotal = base + 1\nassert total == 21")
    write_nb(new_nb(cells), nb_path)
    assert nbs.exec_nb(nb_path, save_outputs=True).ok
    assert nbs.notebook_state(nb_path).counts["clean"] == 2

    cid = read_nb(nb_path).cells[1].id
    with pytest.raises(ValueError, match="not found"): nbs.edit_nb(nb_path, [dict(op="replace_text", cell_id=cid, old="missing", new="x")])
    with pytest.raises(ValueError, match="Stale hash"): nbs.edit_nb(nb_path, [dict(op="replace_text", cell_id=cid, old="20", new="30", expected_hash="000000")])

    res = nbs.edit_nb(nb_path, [dict(op="replace_text", cell_id=cid, old="20", new="30", expected_hash=source_hash("base = 20"))])
    assert res.changed and "+base = 30" in res.diff
    assert [c.state for c in nbs.notebook_state(nb_path).cells] == ["dirty", "stale"]


def test_install_skill_and_repository_self_review(tmp_path):
    first, second = install_skill(tmp_path), install_skill(tmp_path)
    assert (first["status"], second["status"]) == ("written", "unchanged")
    repo_nbs = Path(__file__).resolve().parents[1] / "nbs"
    rep = nbs.review_nb(repo_nbs, include_style=True)
    assert rep.diagnostics == [], str(rep)


def test_graph_architecture_impact_and_hybrid_checks(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "acme"\n')
    for d in ("nbs", "acme", "tests"): (tmp_path / d).mkdir()
    write_nb(new_nb([
        mk_cell("#| default_exp core"), mk_cell("# Core", "markdown"), mk_cell("> Base.", "markdown"),
        mk_cell("## Model", "markdown"), mk_cell("`Item` and `base_rate` live here.", "markdown"),
        mk_cell("#| export\nclass Item:\n    def __init__(self, v): self.v = v\ndef base_rate(): return 0.2"),
        mk_cell("#| export extra\ndef extra_fn(): return base_rate()"),
        mk_cell("assert Item(1).v == 1 and base_rate() == 0.2"),
    ]), tmp_path / "nbs/00_core.ipynb")
    write_nb(new_nb([
        mk_cell("#| default_exp app"), mk_cell("# App", "markdown"), mk_cell("> App. See [gone](99_gone.ipynb) and `Item.ghost`.", "markdown"),
        mk_cell("## Flow", "markdown"), mk_cell("Uses star import from `acme.core`.", "markdown"),
        mk_cell("#| export\nfrom acme.core import *"),
        mk_cell("#| export\n@patch\ndef priced(self: Item): return self.v * base_rate()\ndef _dead_helper(): return 0"),
        mk_cell("bad_order = later_call()"),
        mk_cell("def later_call(): return 1"),
    ]), tmp_path / "nbs/01_app.ipynb")
    (tmp_path / "acme/orphan.py").write_text("# AUTOGENERATED! DO NOT EDIT!\n# %% ../nbs/88_deleted.ipynb #deadbeef\nx = 1\n")
    (tmp_path / "tests/test_app.py").write_text("from acme.app import priced\nfrom acme.core import Item\nassert priced(Item(10)) == 2.0\n")

    arch = nbs.nb_arch(tmp_path)
    assert arch.counts["library"] == 2 and arch.counts["tests"] == 1
    assert "nbs/00_core.ipynb" in {m.id for m in arch.hubs}
    g = nbs.nb_graph(tmp_path)
    assert "flowchart LR" in g.to_mermaid() and '"package": "acme"' in g.to_json()

    imp = nbs.impact("base_rate", scope=tmp_path)
    assert "tests/test_app.py" in imp.test_files and any("pytest" in c for c in imp.suggested_commands)
    assert nbs.trace_path("01_app", "00_core", scope=tmp_path).found

    ctx = nbs.symbol_context("Item", scope=tmp_path)
    assert any("Item.priced" in p for p in ctx.patches)

    rep = nbs.review_nb(tmp_path / "nbs", include_style=False, include_arch=True)
    codes = {d.code for d in rep.diagnostics}
    # Internal star-import from acme.core is resolved, so `cell-order` still fires!
    assert {"cell-order", "orphan-generated-py", "dead-internal-export", "stale-doc-ref"} <= codes
