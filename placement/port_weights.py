# submissions/sidd/placement/port_weights.py

import math


class PortWeights:

    def __init__(
        self,
        anchor_info,
        chip_width,
        chip_height
    ):

        self.anchor = anchor_info["anchor"]

        self.ports = anchor_info["ports"]

        self.W = chip_width
        self.H = chip_height


    def run(self):

        print("\n"+"="*80)
        print("PORT PULL")
        print("="*80)

        print(
            f"Connected ports: "
            f"{len(self.ports)}"
        )


        x=self.W*0.5
        y=self.H*0.5


        print(
            f"Start:"
            f" ({x:.2f},{y:.2f})"
        )


        weight=1.0

        step=0


        while weight>0.1:


            fx=0
            fy=0


            for p in self.ports:


                dx=(

                    p["x"]

                    -

                    x

                )


                dy=(

                    p["y"]

                    -

                    y

                )


                d=math.sqrt(

                    dx*dx

                    +

                    dy*dy

                )


                if d<1e-6:

                    continue


                fx += (

                    weight

                    *

                    (dx/d)

                )


                fy += (

                    weight

                    *

                    (dy/d)

                )


            # ---------------------------------
            # NEW FIX
            # average force instead of sum
            # ---------------------------------

            n=max(
                len(self.ports),
                1
            )

            fx/=n
            fy/=n


            # controlled movement

            x+=3.0*fx
            y+=3.0*fy


            x=max(
                0.5,
                min(
                    x,
                    self.W-0.5
                )
            )


            y=max(
                0.5,
                min(
                    y,
                    self.H-0.5
                )
            )


            if step<10:

                print(

                    f"iter={step} "

                    f"fx={fx:.3f} "

                    f"fy={fy:.3f} "

                    f"x={x:.2f} "

                    f"y={y:.2f}"

                )


            step+=1

            weight*=0.80



        self.anchor.x=x
        self.anchor.y=y

        self.anchor.fixed=True
        self.anchor.placed=True


        print("\nFinal:")

        print(
            f"({x:.2f},"
            f"{y:.2f})"
        )


        return self.anchor