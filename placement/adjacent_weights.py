class AdjacentWeights:


    def __init__(

        self,

        backbone,
        rail_weights

    ):


        self.B=backbone

        self.rail_weights=rail_weights

        self.weights={}


        self.adjacent={

            "left":[
                "top",
                "bottom"
            ],

            "top":[
                "left",
                "right"
            ],

            "right":[
                "top",
                "bottom"
            ],

            "bottom":[
                "left",
                "right"
            ]

        }



    def run(self):


        print("\n"+"="*80)
        print("ADJACENT WEIGHTS")
        print("="*80)


        hubs=list(
            self.B.nodes()
        )


        for hid in hubs:


            score={

                "left":0.0,
                "top":0.0,
                "right":0.0,
                "bottom":0.0

            }


            # -------------------
            # inspect backbone
            # -------------------

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


                pref=(

                    self.rail_weights[
                        nb
                    ]

                )


                # -------------------
                # transfer FULL profile
                # -------------------

                for side,val in (

                    pref.items()

                ):


                    score[
                        side
                    ] += (

                        w*val

                    )


                    # nearby side pull

                    for s in (

                        self.adjacent[
                            side
                        ]

                    ):


                        score[
                            s
                        ] += (

                            0.35*
                            w*
                            val

                        )



            total=sum(
                score.values()
            )


            if total>0:


                for s in score:

                    score[s]/=total



            self.weights[
                hid
            ]=score


            print(
                f"\nHub {hid}"
            )


            best=max(

                score,

                key=score.get

            )


            print(
                f"Preferred={best}"
            )


            for s,v in (

                score.items()

            ):


                print(

                    f"{s:8}"

                    f": "

                    f"{v:.3f}"

                )



        print("\n"+"="*80)
        print("ADJACENT WEIGHTS COMPLETE")
        print("="*80)


        return self.weights