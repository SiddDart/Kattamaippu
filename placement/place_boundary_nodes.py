from submissions.sidd.placement.create_hub_rails import CreateHubRails


class PlaceBoundaryNodes:


    def __init__(

        self,

        G,

        data,
        hubs,
        roles,

        rail_weights,
        adjacent_weights,

        chip_width,
        chip_height,

        anchor,

        rail_thickness=2

    ):


        self.G=G
        self.data=data

        self.hubs=hubs
        self.roles=roles

        self.rail_weights=rail_weights
        self.adjacent_weights=adjacent_weights

        self.W=chip_width
        self.H=chip_height

        self.anchor=anchor
        self.t=rail_thickness

        self.assignment={}
        self.rail_history=[]

        self.hub_home={}

        self.side_order=[

            "left",
            "top",
            "right",
            "bottom"

        ]


        self.side_cursor={

            "left":0.0,
            "top":0.0,
            "right":0.0,
            "bottom":0.0

        }


        self.buffer=.15



    def get_size(

        self,
        macro

    ):


        try:

            node=(
                self.G.nodes[
                    macro
                ]
            )


            w=node.get(
                "width",
                .5
            )

            h=node.get(
                "height",
                .5
            )

            return w,h


        except:

            return .5,.5




    def next_position(

        self,
        side,
        w,
        h

    ):


        c=self.side_cursor[
            side
        ]


        if side=="bottom":


            needed=w+self.buffer


            if c+w*.5>self.W-w*.5:

                c=0.0

                self.side_cursor[
                    side
                ]=0.0


            x=c+w*.5
            y=h*.5


            self.side_cursor[
                side
            ]+=needed




        elif side=="top":


            needed=w+self.buffer


            if c+w*.5>self.W-w*.5:

                c=0.0

                self.side_cursor[
                    side
                ]=0.0


            x=c+w*.5

            y=(
                self.H
                -
                h*.5
            )


            self.side_cursor[
                side
            ]+=needed




        elif side=="left":


            needed=h+self.buffer


            if c+h*.5>self.H-h*.5:

                c=0.0

                self.side_cursor[
                    side
                ]=0.0


            x=w*.5

            y=(
                c+
                h*.5
            )


            self.side_cursor[
                side
            ]+=needed




        else:


            needed=h+self.buffer


            if c+h*.5>self.H-h*.5:

                c=0.0

                self.side_cursor[
                    side
                ]=0.0


            x=(
                self.W
                -
                w*.5
            )


            y=(
                c+
                h*.5
            )


            self.side_cursor[
                side
            ]+=needed


        return x,y




    def run(self):


        print(
            "\n"+"="*80
        )

        print(
            "BOUNDARY PLANNER"
        )

        print(
            "="*80
        )


        rail_gen=CreateHubRails(

            self.W,
            self.H,

            self.rail_history,

            self.anchor,

            self.t

        )


        rail=rail_gen.create()


        hub_queue=[]


        for hid in self.hubs:


            if hid not in self.roles:
                continue


            members=(

                self.roles[
                    hid
                ][
                    "boundary"
                ]

            )


            if len(members)==0:
                continue


            hub_queue.append(
                [hid,members]
            )



        hub_queue.sort(

            key=lambda x:
            len(x[1]),

            reverse=True

        )



        while len(
            hub_queue
        )>0:



            hid,members=(

                hub_queue.pop(
                    0
                )

            )


            print(
                f"\nHub {hid}"
            )


            scores={}


            for s in self.side_order:


                rw=(

                    self.rail_weights[
                        hid
                    ][s]

                )


                aw=(

                    self.adjacent_weights[
                        hid
                    ][s]

                )


                scores[s]=(

                    .7*rw
                    +
                    .3*aw

                )



            ranked=sorted(

                scores,

                key=scores.get,

                reverse=True

            )


            print(
                f"Ranked={ranked}"
            )



            chosen=[]


            best=scores[
                ranked[0]
            ]


            for s in ranked:


                diff=(
                    best
                    -
                    scores[s]
                )


                if diff<0.03:

                    chosen.append(
                        s
                    )


            if len(chosen)==0:

                chosen.append(
                    ranked[0]
                )


            print(
                f"Using:{chosen}"
            )


            nside=len(
                chosen
            )


            split=[]


            base=(
                len(members)
                //
                nside
            )


            rem=(
                len(members)
                %
                nside
            )


            start=0


            for i,s in enumerate(
                chosen
            ):


                count=base


                if i<rem:
                    count+=1


                split.append(

                    (

                        s,

                        members[
                            start:
                            start+
                            count
                        ]

                    )

                )


                start+=count



            for side,group in split:


                print(
                    f"\nSide:{side}"
                )


                for macro in group:


                    w,h=(
                        self.get_size(
                            macro
                        )
                    )


                    x,y=(

                        self.next_position(

                            side,
                            w,
                            h

                        )

                    )


                    self.assignment[
                        macro
                    ]={

                        "rail":
                        rail["id"],

                        "side":
                        side,

                        "slot":-1,

                        "x":x,
                        "y":y,

                        "hub":hid

                    }


                    print(

                        f"{macro}"
                        f" -> "
                        f"{side}"
                        f" "
                        f"({x:.2f},"
                        f"{y:.2f})"

                    )


        print(
            "\n"+"="*80
        )

        print(
            "BOUNDARY PLAN COMPLETE"
        )

        print(
            "="*80
        )


        print(
            f"Assigned:"
            f"{len(self.assignment)}"
        )


        return(
            self.assignment,
            self.rail_history
        )