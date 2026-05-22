# submissions/sidd/graph/detect_hubs.py

from networkx.algorithms.community import (
    greedy_modularity_communities
)

from submissions.sidd.graph.build_graph import GraphBuilder


class HubDetector:

    def __init__(
        self,
        G,
        min_hub_size=4
    ):

        self.G = G

        self.min_hub_size = min_hub_size

        self.hubs = {}



    def detect(self):

        print(
            "\nDetecting communication hubs..."
        )


        communities = list(

            greedy_modularity_communities(

                self.G,

                weight="weight"

            )

        )


        communities=[

            sorted(list(c))

            for c in communities

        ]


        # -----------------------------
        # split large / tiny
        # -----------------------------

        large=[]
        tiny=[]


        for c in communities:

            if len(c)>=self.min_hub_size:

                large.append(c)

            else:

                tiny.append(c)



        # -----------------------------
        # merge tiny communities
        # by TOTAL EDGE WEIGHT
        # -----------------------------

        for t in tiny:


            node=t[0]


            nbrs=list(

                self.G.neighbors(
                    node
                )

            )


            # truly isolated

            if len(nbrs)==0:

                if len(large)>0:

                    # absorb into Hub0
                    large[0].extend(
                        t
                    )

                else:

                    large.append(
                        t
                    )

                continue


            best_hub=None

            best_score=-1


            for hub in large:


                score=0


                for hnode in hub:


                    if self.G.has_edge(

                        node,

                        hnode

                    ):


                        score += (

                            self.G[node]

                            [hnode]

                            .get(

                                "weight",

                                1

                            )

                        )


                if score>best_score:

                    best_score=score

                    best_hub=hub


            if best_hub:

                best_hub.extend(
                    t
                )

            else:

                large[0].extend(
                    t
                )



        communities=large


        # -----------------------------
        # final hub IDs
        # -----------------------------

        for i,c in enumerate(

            communities

        ):

            self.hubs[i]=sorted(c)


        self.summary()

        return self.hubs



    def summary(self):

        print(
            "\n"+"="*70
        )

        print(
            "HUB SUMMARY"
        )

        print(
            "="*70
        )


        total=0


        for hid,members in (

            self.hubs.items()

        ):


            total+=len(
                members
            )


            print(

                f"Hub {hid:<2}"

                f" | "

                f"total={len(members):<3}"

            )


        print(
            "\n"+"="*70
        )


        print(
            f"Total hubs: "
            f"{len(self.hubs)}"
        )

        print(
            f"Total macros: "
            f"{total}"
        )



if __name__=="__main__":


    FILE=(

        r"external/"
        r"MacroPlacement/"
        r"Testcases/"
        r"ICCAD04/"
        r"ibm01/"
        r"netlist.pb.txt"

    )


    G=GraphBuilder(
        FILE
    ).build()


    detector=HubDetector(

        G,

        min_hub_size=4

    )


    hubs=detector.detect()