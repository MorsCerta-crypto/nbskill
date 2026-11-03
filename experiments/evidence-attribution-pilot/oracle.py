"""Independent public-API checks, fixed before either candidate was inspected."""
from tempfile import gettempdir
from fastcore.nbio import mk_cell
from nbskill.skill import context
from nbskill.foundation import write_demo_notebook


def evaluate():
    cells = [
        mk_cell("#| export\ndef twice(value):\n    return value * 2", id="oracle-definition"),
        mk_cell("result = twice(3)\nraise RuntimeError('context must not execute me')", id="oracle-example"),
        mk_cell("assert result == 6", id="oracle-result-check"),
        mk_cell("other = 99\nassert other == 99", id="oracle-unrelated"),
        mk_cell("def deferred_check():\n    assert result == 6", id="oracle-nested"),
        mk_cell("result = 99", id="oracle-rebinding"),
        mk_cell("assert result == 99", id="oracle-after-rebinding"),
        mk_cell("assert twice(4) == 8", id="oracle-direct-check"),
        mk_cell("#| export\ndef following(value):\n    return value", id="oracle-next-definition"),
        mk_cell("assert twice(2) == 4", id="oracle-outside-bundle"),
    ]
    rows = []
    with write_demo_notebook("evidence_attribution_oracle.ipynb", cells=cells, base=gettempdir()) as path:
        before = path.read_bytes()
        for mode in ("review", "edit"):
            selected = context(f"{path}#twice", mode=mode, verbose=False)["selection"]["examples"]
            ids = {item["cell_id"] for item in selected}
            checks = dict(
                direct_example="oracle-example" in ids and "oracle-direct-check" in ids,
                separated_assertion="oracle-result-check" in ids,
                unrelated_excluded="oracle-unrelated" not in ids,
                rebound_excluded="oracle-rebinding" not in ids and "oracle-after-rebinding" not in ids,
                nested_excluded="oracle-nested" not in ids,
                boundary_respected="oracle-outside-bundle" not in ids,
                read_only_no_execution=path.read_bytes() == before,
            )
            rows.append(dict(mode=mode, checks=checks, passed=sum(checks.values()), total=len(checks),
                selected_ids=sorted(ids), execution_metadata=all("execution" in item for item in selected)))
    return rows
