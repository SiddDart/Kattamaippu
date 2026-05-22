# graph/communication_backbone.py

import networkx as nx

from submissions.sidd.graph.build_graph import GraphBuilder
from submissions.sidd.graph.detect_hubs import HubDetector


class CommunicationBackbone:

    def __init__(self, G, hubs):

        self.G = G
        self.hubs = hubs

        self.backbone = nx.Graph()

        self.node_to_hub = {}


    def build(self):

        print(
            "\nBuilding communication backbone..."
        )

        # --------------------------------
        # reverse map:
        # macro -> hub id
        # --------------------------------

        for hid, members in self.hubs.items():

            for n in members:

                self.node_to_hub[n] = hid


        # --------------------------------
        # add hub nodes
        # --------------------------------

        for hid, members in self.hubs.items():

            self.backbone.add_node(

                hid,

                size=len(members)

            )


        # --------------------------------
        # count cross-hub communication
        # --------------------------------

        edge_weights = {}

        for u, v, data in self.G.edges(data=True):

            hu = self.node_to_hub[u]
            hv = self.node_to_hub[v]

            if hu == hv:
                continue


            pair = tuple(
                sorted([hu, hv])
            )

            w = data.get(
                "weight",
                1
            )


            if pair not in edge_weights:

                edge_weights[pair] = 0


            edge_weights[pair] += w


        # --------------------------------
        # create hub graph
        # --------------------------------

        for (h1, h2), w in edge_weights.items():

            self.backbone.add_edge(

                h1,
                h2,

                weight=w

            )


        self.summary()

        return self.backbone



    def summary(self):

        print(
            "\n"+"="*80
        )

        print(
            "COMMUNICATION BACKBONE"
        )

        print(
            "="*80
        )


        print(
            f"Hubs: "
            f"{self.backbone.number_of_nodes()}"
        )

        print(
            f"Connections: "
            f"{self.backbone.number_of_edges()}"
        )


        print(
            "\nStrongest hub links:\n"
        )


        edges = sorted(

            self.backbone.edges(
                data=True
            ),

            key=lambda x:
            x[2]["weight"],

            reverse=True

        )


        for h1, h2, d in edges[:20]:

            print(

                f"Hub{h1}"

                f" <--> "

                f"Hub{h2}"

                f" | weight="

                f"{d['weight']}"

            )



if __name__=="__main__":

    FILE = (
        r"external/MacroPlacement/"
        r"Testcases/ICCAD04/"
        r"ibm01/"
        r"netlist.pb.txt"
    )


    G = GraphBuilder(
        FILE
    ).build()


    hubs = HubDetector(
        G,
        min_hub_size=4
    ).detect()


    backbone = CommunicationBackbone(
        G,
        hubs
    ).build()