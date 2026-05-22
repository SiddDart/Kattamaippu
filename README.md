# Kattamaippu
A topology-driven macro placement algorithm for fast chip design developed for Hudson River Trading × PARTCL. Achieved +28.4% average improvement over SA across all IBM benchmarks and outperformed Google's RePlAce on multiple designs with zero overlaps.

## Technical Overview

The pipeline begins with `parse_netlist.py`, which extracts structural information from benchmark netlists and transforms raw connectivity into graph-relevant data structures. `build_graph.py` constructs a weighted communication graph where nodes represent macros and edges encode interaction strength derived from net connectivity.

Since not all macros contribute equally to information flow:

- `detect_hubs.py` identifies highly connected communication centers  
- `classify_roles.py` assigns structural roles such as hubs, bridges, and peripheral nodes  
- `communication_backbone.py` extracts a reduced communication skeleton intended to preserve dominant information pathways  

The motivation for this graph stage originated from repeated observations that purely geometric methods scattered strongly connected macros across the floorplan and created large routing penalties despite visually compact layouts.

---

## Topology Generation

Once the graph hierarchy is built, placement transitions into topology generation.

The following modules establish organizational hierarchy:

- `preplace_anchor.py`
- `create_hub_rails.py`
- `place_boundary_nodes.py`
- `place_interdependent.py`

In this framework:

- Hubs become placement anchors
- Rails act as local communication corridors
- Neighboring structures remain spatially close
- Communication locality is preserved

The rail concept originated from treating strongly interacting macro groups as transportation corridors rather than isolated blocks.

Additional weighting modules:

- `adjacent_weights.py`
- `rail_weights.py`
- `port_weights.py`

These compute local interaction importance and modify placement decisions based on structural proximity and communication pressure.

`bridge_connector.py` explicitly handles bridge nodes to preserve long-range communication paths.

---

## Geometric Realization

After topology generation:

```text
Graph Topology
        ↓
commit_macro_positions.py
        ↓
Physical Coordinates
# Installation & Running

## 1. Clone the repository

```bash
git clone https://github.com/SiddDart/Kattamaippu.git
cd Kattamaippu
```

---

## 2. Install dependencies

This project uses `uv`.

Install:

```bash
pip install uv
```

Then sync the environment:

```bash
uv sync
```

or:

```bash
uv pip install -r requirements.txt
```

---

## 3. Repository placement

This repository was designed to live inside the PARTCL Macro Placement Challenge structure.

Expected structure:

```text
partcl-macro-place-challenge/
│
├── external/
├── macro_place/
├── submissions/
│      └── sidd/
│            ├── graph/
│            ├── parser/
│            ├── placement/
│            ├── eval_bridge.py
│            └── main.py
│
└── ...
```

Place the entire `sidd` folder inside:

```text
submissions/
```

Do NOT place only individual files.

Wrong:

```text
submissions/
    main.py
```

Correct:

```text
submissions/
    sidd/
        main.py
        eval_bridge.py
        graph/
        parser/
        placement/
```

---

## 4. Move to challenge root

Before running, your terminal should be inside:

```text
partcl-macro-place-challenge
```

Example:

```powershell
PS C:\Users\YOUR_NAME\partcl-macro-place-challenge>
```

Do NOT run inside:

```text
submissions/sidd/
```

or imports will fail.

---

## 5. Run all IBM benchmarks

```bash
uv run evaluate submissions/sidd/eval_bridge.py --all
```

This automatically runs:

```text
ibm01
ibm02
...
ibm18
```

through the repository evaluation framework.

---

## Common Errors

### ModuleNotFoundError: No module named 'submissions'

Cause:

Running from wrong directory.

Wrong:

```bash
cd submissions/sidd
uv run ...
```

Correct:

```bash
cd partcl-macro-place-challenge
uv run evaluate submissions/sidd/eval_bridge.py --all
```

---

### Failed to load placer

Cause:

Using:

```bash
uv run evaluate submissions.sidd.main --all
```

instead of:

```bash
uv run evaluate submissions/sidd/eval_bridge.py --all
```

Use file paths (`/`) not module notation (`.`).

---

### FileNotFoundError: eval_bridge.py

Cause:

Bridge file missing.

Ensure:

```text
submissions/sidd/eval_bridge.py
```

exists.

---

### placement returned NoneType

Cause:

`main()` completed but never returned placement.

Ensure:

```python
return placement
```

exists at the end of `main.py`.

---

### plc variable not defined

Cause:

Benchmark injection through evaluate bypasses internal benchmark loading.

Fix:

```python
if benchmark is None:
    benchmark, plc = load(...)
else:
    plc=benchmark.plc
```

---

## Evaluation Philosophy

The repository evaluator repeatedly injects benchmark instances:

```text
evaluate
    ↓
eval_bridge.py
    ↓
main.py
    ↓
graph construction
    ↓
topology generation
    ↓
legalization
    ↓
soft placement
```

The bridge layer preserves the nested architecture while allowing automatic execution across benchmark suites.

---

## Execute single benchmark

For development:

```bash
python -m uv run -m submissions.sidd.main
```

For full evaluation:

```bash
uv run evaluate submissions/sidd/eval_bridge.py --all
```
