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
