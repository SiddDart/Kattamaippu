# submissions/sidd/roles/classify_roles.py

import numpy as np
import networkx as nx
from collections import defaultdict


class RoleClassifier:

    def __init__(
        self,
        G,
        hubs,
        io_targets=None
    ):

        self.G = G

        self.hubs = hubs

        if io_targets is None:

            io_targets = {}

        self.io_targets = io_targets


    def classify(self):

        print(
            "\nClassifying roles..."
        )


        roles = {}


        # -------------------------
        # graph metrics
        # -------------------------

        degree = dict(
            self.G.degree()
        )


        print(
            "computing betweenness..."
        )

        bc = nx.betweenness_centrality(
            self.G,
            normalized=True,
            weight="weight"
        )


        max_degree = max(
            degree.values(),
            default=1
        )


        max_bc = max(
            bc.values(),
            default=1e-8
        )


        # -------------------------
        # global bridge threshold
        # -------------------------

        bc_values = list(
            bc.values()
        )


        bridge_cutoff = np.percentile(

            bc_values,

            95

        )


        print(
            f"Bridge cutoff={bridge_cutoff:.5f}"
        )


        # -------------------------
        # classify per hub
        # -------------------------

        for hub_id, nodes in (

            self.hubs.items()

        ):


            boundary_scores = {}


            # -------------------
            # compute scores
            # -------------------

            for n in nodes:


                deg = degree.get(
                    n,
                    0
                )


                b = bc.get(
                    n,
                    0
                )


                # IO count

                io_count = len(

                    self.io_targets.get(
                        n,
                        []
                    )

                )


                io_ratio = (

                    io_count

                    /

                    (deg+1)

                )


                deg_norm = (

                    deg

                    /

                    max_degree

                )


                bc_norm = (

                    b

                    /

                    max_bc

                )


                # ----------------
                # GraphRail score
                # ----------------

                score=(

                    0.4*io_ratio

                    +

                    0.3*(1-bc_norm)

                    +

                    0.3*(1-deg_norm)

                )


                boundary_scores[
                    n
                ]=score


            # ----------------------
            # local hub threshold
            # ----------------------

            vals=list(

                boundary_scores.values()

            )


            boundary_cutoff=(

                np.percentile(

                    vals,

                    75

                )

                if len(vals)>0

                else 0

            )


            hub_roles={

                "boundary":[],

                "bridge":[],

                "interdependent":[]

            }


            # ----------------------
            # assign
            # ----------------------

            for n in nodes:


                b=bc.get(
                    n,
                    0
                )


                score=boundary_scores[
                    n
                ]


                # bridge dominates

                if b>=bridge_cutoff:

                    hub_roles[
                        "bridge"
                    ].append(
                        n
                    )


                elif (

                    score

                    >=

                    boundary_cutoff

                ):

                    hub_roles[
                        "boundary"
                    ].append(
                        n
                    )


                else:

                    hub_roles[
                        "interdependent"
                    ].append(
                        n
                    )


            roles[
                hub_id
            ]=hub_roles


            print(
                f"\nHub {hub_id}"
            )

            print(
                f"Total={len(nodes)}"
            )

            print(
                f"Boundary={len(hub_roles['boundary'])}"
            )

            print(
                f"Bridge={len(hub_roles['bridge'])}"
            )

            print(
                f"Interdependent={len(hub_roles['interdependent'])}"
            )


        return roles