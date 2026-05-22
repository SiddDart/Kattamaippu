# submissions/sidd/main.py

from submissions.sidd.graph.build_graph import GraphBuilder
from submissions.sidd.graph.detect_hubs import HubDetector
from submissions.sidd.graph.classify_roles import RoleClassifier
from submissions.sidd.graph.communication_backbone import CommunicationBackbone

from submissions.sidd.placement.reset_floorplan import FloorplanReset
from submissions.sidd.placement.preplace_anchor import PreplaceAnchor
from submissions.sidd.placement.port_weights import PortWeights

from submissions.sidd.placement.rail_weights import RailWeights
from submissions.sidd.placement.adjacent_weights import AdjacentWeights

from submissions.sidd.placement.place_boundary_nodes import (
    PlaceBoundaryNodes
)

from submissions.sidd.placement.place_interdependent import (
    PlaceInterdependent
)

from submissions.sidd.placement.bridge_connector import (
    BridgeConnector
)

from submissions.sidd.placement.commit_macro_positions import (
    CommitMacroPositions
)

from submissions.sidd.placement.legalize import (
    TopologyLegalizer
)

from macro_place.loader import load_benchmark
from macro_place.objective import compute_proxy_cost
from macro_place.utils import visualize_placement


FILE=(

    r"external/"
    r"MacroPlacement/"
    r"Testcases/"
    r"ICCAD04/"
    r"ibm01/"
    r"netlist.pb.txt"

)


def main(benchmark=None):

    print("\n"+"="*80)
    print("BUILD GRAPH")
    print("="*80)

    builder=GraphBuilder(FILE)

    G=builder.build()

    data=builder.data

    largest=data["largest"]

    print(
        f"\nLargest: {largest.name}"
    )


    print("\n"+"="*80)
    print("DETECT HUBS")
    print("="*80)

    hubs=HubDetector(
        G
    ).detect()


    print("\n"+"="*80)
    print("CLASSIFY")
    print("="*80)

    roles=RoleClassifier(

        G,
        hubs

    ).classify()


    # ==========================================
    # INTERDEPENDENT TEST
    # ==========================================

    print("\n"+"="*80)
    print("INTERDEPENDENT TEST")
    print("="*80)

    try:

        print(
            roles[0].keys()
        )

        sample=roles[0]["interdependent"][:5]

        print("\nSample:")
        print(sample)

        if len(sample)>0:

            m=sample[0]

            print("\nType:")
            print(type(m))

            print("\nMacro:")
            print(m)

            print("\nNeighbors:")

            print(

                list(
                    G.neighbors(m)
                )[:10]

            )

    except Exception as e:

        print(
            "\nTEST FAILED:"
        )

        print(e)



    print("\n"+"="*80)
    print("BACKBONE")
    print("="*80)

    B=CommunicationBackbone(

        G,
        hubs

    ).build()



    print("\n"+"="*80)
    print("RESET")
    print("="*80)

    FloorplanReset(

        data,
        hubs,
        roles,
        B

    ).reset()



    print("\n"+"="*80)
    print("PREPLACE")
    print("="*80)

    anchor_info=PreplaceAnchor(

        data,
        hubs

    ).run()



    print("\n"+"="*80)
    print("PORT PULL")
    print("="*80)

    anchor=PortWeights(

        anchor_info,

        chip_width=23,
        chip_height=23

    ).run()



    print("\n"+"="*80)
    print("RAIL WEIGHTS")
    print("="*80)

    rw=RailWeights(

        hubs,
        roles,

        B,

        anchor,

        chip_width=23,
        chip_height=23

    )

    rail_weights=rw.compute()



    print("\n"+"="*80)
    print("ADJACENT WEIGHTS")
    print("="*80)

    adj=AdjacentWeights(

        B,

        rail_weights

    )

    adjacent_weights=adj.run()



    print("\n"+"="*80)
    print("BOUNDARY PLANNING")
    print("="*80)

    planner=PlaceBoundaryNodes(

        G=G,

        data=data,

        hubs=hubs,

        roles=roles,

        rail_weights=rail_weights,

        adjacent_weights=adjacent_weights,

        chip_width=23,

        chip_height=23,

        anchor=anchor,

        rail_thickness=2

    )


    assignment,rail_history=(
        planner.run()
    )



    print("\n"+"="*80)
    print("INTERDEPENDENT")
    print("="*80)

    ip=PlaceInterdependent(

        G,
        hubs,
        roles,

        assignment,

        23,
        23,

        anchor

    )

    interdependent_assignment=(
        ip.run()
    )



    print("\n"+"="*80)
    print("BRIDGE")
    print("="*80)

    bc=BridgeConnector(

        B,
        hubs,
        roles,

        assignment,

        interdependent_assignment,

        23,
        23

    )

    bridge_assignment=(
        bc.run()
    )



    print("\n"+"="*80)
    print("COMMIT")
    print("="*80)

    commit=CommitMacroPositions(

        data,

        assignment,

        interdependent_assignment,

        bridge_assignment,

        23,
        23

    )

    final_assignment=(
        commit.run()
    )



    print("\n"+"="*80)
    print("RAIL SUMMARY")
    print("="*80)

    for r in rail_history:

        print(
            f"\nRail {r['id']}"
        )

        print(
            f"Left : {len(r['slots']['left'])}"
        )

        print(
            f"Top : {len(r['slots']['top'])}"
        )

        print(
            f"Right : {len(r['slots']['right'])}"
        )

        print(
            f"Bottom : {len(r['slots']['bottom'])}"
        )



    print("\n"+"="*80)
    print("FIRST ASSIGNMENTS")
    print("="*80)

    c=0

    for k,v in assignment.items():

        print(

            f"{k}"
            f" -> "
            f"Rail"
            f"{v['rail']} "
            f"{v['side']} "
            f"slot "
            f"{v['slot']}"

        )

        c+=1

        if c>=25:

            break



    print("\n"+"="*80)
    print("FINAL")
    print("="*80)

    print(
        f"x={anchor.x:.2f}"
    )

    print(
        f"y={anchor.y:.2f}"
    )



    print("\n"+"="*80)
    print("EVALUATION")
    print("="*80)


    # BENCHMARK LOADING

    if benchmark is None:
        benchmark,plc=load_benchmark(

            "external/MacroPlacement/Testcases/ICCAD04/ibm01/netlist.pb.txt",

            "external/MacroPlacement/Testcases/ICCAD04/ibm01/initial.plc"

        )

    else:

        plc=None


    placement=(

        benchmark
        .macro_positions
        .clone()

    )


    name_to_bidx={}

    if plc is not None:

        for bidx,idx in enumerate(

            plc.hard_macro_indices

        ):

            node=(
                plc.modules_w_pins[idx]
            )

            name_to_bidx[
                node.get_name()
            ]=bidx



    for name,d in (

        final_assignment.items()

    ):


        if name not in name_to_bidx:
            continue


        bidx=(
            name_to_bidx[name]
        )


        placement[
            bidx,
            0
        ]=d["x"]


        placement[
            bidx,
            1
        ]=d["y"]



    if anchor.name in name_to_bidx:

        bidx=(
            name_to_bidx[
                anchor.name
            ]
        )

        placement[
            bidx,
            0
        ]=anchor.x

        placement[
            bidx,
            1
        ]=anchor.y


    print("\n"+"="*80)
    print("LEGALIZATION")
    print("="*80)

    legalizer=TopologyLegalizer(

        row_height=.45,
        halo=.05,
        search_radius=20,
        step=.25

    )

    placement=legalizer.place(

        benchmark,
        placement

    )


    # compactor=MacroCompactor(
    #     iterations=10,
    #     step=0.35
    # )
    #
    # placement=compactor.place(
    #     benchmark,
    #     placement
    # )


    if plc is not None:

        metrics=compute_proxy_cost(

            placement,
            benchmark,
            plc

        )


        print("\nMetrics:\n")

        for k,v in metrics.items():

            print(
                f"{k}: {v}"
            )


    print(
        "\nLaunching challenge viewer..."
    )


    print("\n"+"="*80)
    print("FINAL MAIN CHECK")
    print("="*80)

    print(
        "XXXXXXXX NEW MAIN LOADED XXXXXXXX"
    )

    print("\nDONE\n")

    if plc is not None:

        visualize_placement(

            placement,
            benchmark,
            plc=plc

        )

    return placement


if __name__=="__main__":

    main()