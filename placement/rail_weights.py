import math


class RailWeights:


    def __init__(

        self,

        hubs,
        roles,

        backbone,

        anchor,

        chip_width,
        chip_height

    ):


        self.hubs=hubs
        self.roles=roles

        self.B=backbone

        self.ax=anchor.x
        self.ay=anchor.y

        self.W=chip_width
        self.H=chip_height

        self.weights={}

        self.side_order=[
            "left",
            "top",
            "right",
            "bottom"
        ]



    def distance(

        self,

        x1,
        y1,

        x2,
        y2

    ):


        return math.sqrt(

            (x2-x1)**2+

            (y2-y1)**2

        )



    def side_point(

        self,

        side

    ):


        if side=="left":

            return(
                0,
                self.H/2
            )


        elif side=="top":

            return(
                self.W/2,
                self.H
            )


        elif side=="right":

            return(
                self.W,
                self.H/2
            )


        return(
            self.W/2,
            0
        )



    def compute(self):


        print("\n"+"="*80)
        print("RAIL WEIGHTS")
        print("="*80)


        for hid in self.hubs:


            if hid not in self.roles:

                continue


            boundary=len(
                self.roles[hid]["boundary"]
            )

            bridge=len(
                self.roles[hid]["bridge"]
            )

            members=len(
                self.hubs[hid]
            )


            scores={

                "left":0,
                "top":0,
                "right":0,
                "bottom":0

            }


            # -------------------------
            # anchor pull
            # -------------------------

            for side in self.side_order:


                sx,sy=(
                    self.side_point(
                        side
                    )
                )


                d=self.distance(

                    self.ax,
                    self.ay,

                    sx,
                    sy

                )


                pull=1/(d+1)


                scores[
                    side
                ] += 2.0*pull



            # -------------------------
            # boundary ratio
            # -------------------------

            bscore=(

                boundary
                /
                (members+1)

            )


            bridge_penalty=(

                bridge
                /
                (members+1)

            )


            for side in self.side_order:


                scores[
                    side
                ] += (

                    1.5*bscore

                )


                scores[
                    side
                ] -= (

                    0.8*
                    bridge_penalty

                )



            # -------------------------
            # DIRECTIONAL communication
            # -------------------------

            if hid in self.B:


                for nb in self.B.neighbors(
                    hid
                ):


                    w=(

                        self.B[
                            hid
                        ][nb]

                        .get(
                            "weight",
                            1
                        )

                    )


                    # deterministic side assignment
                    # based on hub id

                    pref=(
                        self.side_order[
                            nb % 4
                        ]
                    )


                    scores[
                        pref
                    ] += (

                        2.0*
                        w/50
                    )


                    # nearby pull

                    if pref=="left":

                        scores[
                            "top"
                        ] += (

                            w/100
                        )

                        scores[
                            "bottom"
                        ] += (

                            w/100
                        )


                    elif pref=="top":

                        scores[
                            "left"
                        ] += (

                            w/100
                        )

                        scores[
                            "right"
                        ] += (

                            w/100
                        )


                    elif pref=="right":

                        scores[
                            "top"
                        ] += (

                            w/100
                        )

                        scores[
                            "bottom"
                        ] += (

                            w/100
                        )


                    else:


                        scores[
                            "left"
                        ] += (

                            w/100
                        )

                        scores[
                            "right"
                        ] += (

                            w/100
                        )



            total=sum(
                scores.values()
            )


            if total>0:


                for s in scores:

                    scores[s]/=total



            self.weights[
                hid
            ]=scores


            print(
                f"\nHub {hid}"
            )

            print(
                f"members={members}"
            )

            print(
                f"boundary={boundary}"
            )

            print(
                f"bridge={bridge}"
            )


            for s,v in (

                scores.items()

            ):


                print(

                    f"{s:8}"
                    f": "
                    f"{v:.3f}"

                )



        print("\n"+"="*80)
        print("RAIL WEIGHTS COMPLETE")
        print("="*80)


        return self.weights