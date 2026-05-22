import math


class BridgeConnector:


    def __init__(

        self,

        B,
        hubs,
        roles,

        boundary_assignment,
        interdependent_assignment,

        chip_width,
        chip_height

    ):


        self.B=B

        self.hubs=hubs
        self.roles=roles

        self.boundary=boundary_assignment

        self.interior=(
            interdependent_assignment
        )

        self.W=chip_width
        self.H=chip_height


        self.assignment={}



    def hub_center(

        self,
        hid

    ):


        xs=[]
        ys=[]


        for m,d in (

            self.boundary.items()

        ):


            if d["hub"]==hid:

                xs.append(
                    d["x"]
                )

                ys.append(
                    d["y"]
                )


        for m,d in (

            self.interior.items()

        ):


            if d["hub"]==hid:

                xs.append(
                    d["x"]
                )

                ys.append(
                    d["y"]
                )


        if len(xs)==0:

            return (

                self.W/2,
                self.H/2

            )


        return (

            sum(xs)/len(xs),

            sum(ys)/len(ys)

        )



    def strongest_neighbor(

        self,
        hid

    ):


        if hid not in self.B:

            return None


        best=None
        bestw=-1


        for nb in (

            self.B.neighbors(
                hid
            )

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


            if w>bestw:

                bestw=w
                best=nb


        return best



    def run(self):


        print(
            "\n"+"="*80
        )

        print(
            "BRIDGE CONNECTOR"
        )

        print(
            "="*80
        )


        spread=0


        for hid in self.hubs:


            if hid not in self.roles:
                continue


            bridges=(

                self.roles[
                    hid
                ][
                    "bridge"
                ]

            )


            if len(bridges)==0:
                continue


            nb=(

                self.strongest_neighbor(
                    hid
                )

            )


            c1x,c1y=(

                self.hub_center(
                    hid
                )

            )


            if nb is None:

                c2x=(
                    self.W/2
                )

                c2y=(
                    self.H/2
                )

            else:

                c2x,c2y=(

                    self.hub_center(
                        nb
                    )

                )


            print(
                f"\nHub {hid}"
            )

            print(
                f"target={nb}"
            )


            for i,m in enumerate(
                bridges
            ):


                alpha=(

                    i+1

                )/(

                    len(bridges)+1

                )


                x=(

                    c1x*(1-alpha)

                    +

                    c2x*alpha

                )


                y=(

                    c1y*(1-alpha)

                    +

                    c2y*alpha

                )


                x+=(
                    math.cos(
                        spread
                    )*0.8
                )

                y+=(
                    math.sin(
                        spread
                    )*0.8
                )


                spread+=1


                x=max(
                    1,
                    min(
                        self.W-1,
                        x
                    )
                )

                y=max(
                    1,
                    min(
                        self.H-1,
                        y
                    )
                )


                self.assignment[
                    m
                ]={

                    "x":x,
                    "y":y,

                    "hub":hid,

                    "target":nb

                }


                print(

                    f"{m}"
                    f" -> "
                    f"({x:.2f},"
                    f"{y:.2f}) "

                    f"to Hub{nb}"

                )



        print(
            "\n"+"="*80
        )

        print(
            "BRIDGE COMPLETE"
        )

        print(
            "="*80
        )


        return self.assignment