# submissions/sidd/graph/build_graph.py

import networkx as nx
from collections import defaultdict
from pathlib import Path

from submissions.sidd.parser.parse_netlist import NetlistParser
from macro_place.loader import load_benchmark_from_dir


class GraphBuilder:

    def __init__(self, filepath):

        self.filepath=filepath

        self.parser=NetlistParser(
            filepath
        )

        self.data=self.parser.parse()

        self.hard=self.data["hard"]

        self.G=nx.Graph()


    def build(self):

        print(
            "\nBuilding communication graph..."
        )

        benchmark_root=Path(
            self.filepath
        ).parent


        _,plc=load_benchmark_from_dir(
            str(
                benchmark_root
            ).replace(
                "\\",
                "/"
            )
        )


        n_hard=len(
            self.hard
        )


        name_to_idx={}


        for bidx,idx in enumerate(

            plc.hard_macro_indices

        ):

            name=(
                plc.modules_w_pins[idx]
                .get_name()
            )

            name_to_idx[
                name
            ]=bidx


        # ----------------------------
        # add nodes
        # ----------------------------

        for macro in self.hard:

            self.G.add_node(

                macro.name,

                area=macro.area,

                width=macro.width,

                height=macro.height,

                x=macro.x,

                y=macro.y

            )


        edge_weights=defaultdict(
            float
        )


        # ----------------------------
        # HARD-HARD NETS ONLY
        # ----------------------------

        for driver,sinks in (

            plc.nets.items()

        ):


            macros=set()


            allpins=[driver]+sinks


            for pin in allpins:

                parent=pin.split(
                    "/"
                )[0]


                if parent in name_to_idx:

                    macros.add(
                        parent
                    )


            macros=list(
                macros
            )


            for i in range(
                len(macros)
            ):

                for j in range(
                    i+1,
                    len(macros)
                ):

                    a=macros[i]
                    b=macros[j]


                    key=tuple(

                        sorted(
                            [a,b]
                        )

                    )


                    edge_weights[
                        key
                    ]+=1.0


        # ----------------------------
        # create graph
        # ----------------------------

        for (

            a,
            b

        ),w in (

            edge_weights.items()

        ):


            self.G.add_edge(

                a,
                b,

                weight=w

            )


        print(
            "\n"+"="*70
        )

        print(
            "GRAPH SUMMARY"
        )

        print(
            "="*70
        )


        print(
            f"Nodes : "
            f"{self.G.number_of_nodes()}"
        )

        print(
            f"Edges : "
            f"{self.G.number_of_edges()}"
        )


        n=self.G.number_of_nodes()

        avg=0


        if n>0:

            avg=(

                sum(

                    dict(
                        self.G.degree()
                    ).values()

                )

                /n

            )


        print(
            f"Average degree : "
            f"{avg:.2f}"
        )


        largest=sorted(

            self.G.degree,

            key=lambda x:x[1],

            reverse=True

        )[:20]


        print(
            "\nTop connected:\n"
        )


        for name,d in largest:

            print(
                f"{name:<15}"
                f"degree={d}"
            )


        return self.G