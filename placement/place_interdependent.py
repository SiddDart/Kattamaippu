import math
import random


class PlaceInterdependent:


    def __init__(

        self,

        G,
        hubs,
        roles,

        boundary_assignment,

        chip_width,
        chip_height,

        anchor

    ):


        self.G=G

        self.hubs=hubs
        self.roles=roles

        self.boundary=boundary_assignment

        self.W=chip_width
        self.H=chip_height

        self.anchor=anchor

        self.assignment={}

        self.occupied=[]



    def neighbor_score(

        self,
        node,
        candidates

    ):


        score=[]


        neigh=set(

            self.G.neighbors(
                node
            )

        )


        for c in candidates:


            s=0


            if c in neigh:
                s+=1


            score.append(
                (s,c)
            )


        score.sort(
            reverse=True
        )


        if len(score)==0:

            return None


        return score[0][1]



    def get_xy(

        self,
        node

    ):


        if node in self.assignment:


            return(

                self.assignment[
                    node
                ]["x"],

                self.assignment[
                    node
                ]["y"]

            )


        if node in self.boundary:


            return(

                self.boundary[
                    node
                ]["x"],

                self.boundary[
                    node
                ]["y"]

            )


        return(

            self.anchor.x,
            self.anchor.y

        )



    def occupied_ok(

        self,
        x,
        y

    ):


        for ox,oy in self.occupied:


            d=(

                (x-ox)**2
                +
                (y-oy)**2

            )**0.5


            if d<1.0:

                return False


        return True



    def attach(

        self,

        px,
        py

    ):


        radius=1.2


        while radius<15:


            angle0=random.uniform(
                0,
                2*math.pi
            )


            for t in range(24):


                th=(

                    angle0
                    +
                    2*
                    math.pi*
                    t/24

                )


                x=(

                    px+

                    radius*
                    math.cos(th)

                )


                y=(

                    py+

                    radius*
                    math.sin(th)

                )


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


                if self.occupied_ok(
                    x,
                    y
                ):

                    return x,y


            radius+=0.8


        return(

            px+
            random.uniform(
                -2,
                2
            ),

            py+
            random.uniform(
                -2,
                2
            )

        )



    def run(self):


        print(
            "\n"+"="*80
        )

        print(
            "INTERDEPENDENT PLACEMENT"
        )

        print(
            "="*80
        )


        for hid in self.hubs:


            if hid not in self.roles:
                continue


            members=(

                self.roles[
                    hid
                ][
                    "interdependent"
                ]

            )


            if len(members)==0:
                continue


            print(
                f"\nHub {hid}"
            )


            boundary=[]


            for m,d in self.boundary.items():

                if d["hub"]==hid:

                    boundary.append(
                        m
                    )


            if len(boundary)==0:

                continue


            placed=list(
                boundary
            )


            for b in boundary:


                bx=(
                    self.boundary[
                        b
                    ]["x"]
                )


                by=(
                    self.boundary[
                        b
                    ]["y"]
                )


                self.occupied.append(
                    (
                        bx,
                        by
                    )
                )



            recent=[]


            for i,m in enumerate(
                members
            ):


                candidates=[]


                candidates.extend(
                    boundary
                )


                candidates.extend(
                    recent[-8:]
                )


                parent=(

                    self.neighbor_score(

                        m,
                        candidates

                    )

                )


                if parent is None:

                    parent=boundary[0]


                px,py=(

                    self.get_xy(
                        parent
                    )

                )


                x,y=(

                    self.attach(
                        px,
                        py
                    )

                )


                self.occupied.append(
                    (
                        x,
                        y
                    )
                )


                placed.append(
                    m
                )


                recent.append(
                    m
                )


                self.assignment[
                    m
                ]={

                    "x":x,

                    "y":y,

                    "hub":hid,

                    "parent":parent

                }


                print(

                    f"{m}"
                    f" -> "
                    f"({x:.2f},"
                    f"{y:.2f}) "

                    f"parent="
                    f"{parent}"

                )


        print(
            "\n"+"="*80
        )

        print(
            "INTERDEPENDENT COMPLETE"
        )

        print(
            "="*80
        )


        return self.assignment