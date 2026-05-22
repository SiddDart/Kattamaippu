import torch
import math


class TopologyLegalizer:
    """
    Topology-preserving legalization.

    Goals:
    - remove overlaps
    - preserve hub clouds
    - preserve boundary placements
    - keep macros near original position
    - protect giant macros
    """

    def __init__(
        self,
        row_height=0.45,
        halo=0.05,
        search_radius=20,
        step=0.25
    ):
        self.row_height=row_height
        self.halo=halo
        self.search_radius=search_radius
        self.step=step


    def overlap(self,a,b):

        ax1=a["x"]-a["w"]/2-self.halo
        ay1=a["y"]-a["h"]/2-self.halo
        ax2=a["x"]+a["w"]/2+self.halo
        ay2=a["y"]+a["h"]/2+self.halo

        bx1=b["x"]-b["w"]/2-self.halo
        by1=b["y"]-b["h"]/2-self.halo
        bx2=b["x"]+b["w"]/2+self.halo
        by2=b["y"]+b["h"]/2+self.halo

        return not (

            ax2<=bx1 or
            ax1>=bx2 or
            ay2<=by1 or
            ay1>=by2

        )


    def legal(
        self,
        candidate,
        placed,
        W,
        H
    ):

        x=candidate["x"]
        y=candidate["y"]
        w=candidate["w"]
        h=candidate["h"]

        if x-w/2<0:
            return False

        if x+w/2>W:
            return False

        if y-h/2<0:
            return False

        if y+h/2>H:
            return False

        for p in placed:

            if self.overlap(
                candidate,
                p
            ):
                return False

        return True


    def place(
        self,
        benchmark,
        placement
    ):

        W=benchmark.canvas_width
        H=benchmark.canvas_height

        sizes=benchmark.macro_sizes

        movable=(
            benchmark.get_movable_mask()
            &
            benchmark.get_hard_macro_mask()
        )

        idxs=torch.where(
            movable
        )[0].tolist()

        # biggest first
        idxs.sort(

            key=lambda i:
            -(
                sizes[i,0].item()
                *
                sizes[i,1].item()
            )

        )

        placed=[]

        for idx in idxs:

            w=sizes[idx,0].item()
            h=sizes[idx,1].item()

            x0=placement[idx,0].item()
            y0=placement[idx,1].item()

            found=False

            # -------- local search first --------

            for r in range(
                self.search_radius
            ):

                radius=r*self.step

                for theta in range(
                    0,
                    360,
                    20
                ):

                    t=math.radians(
                        theta
                    )

                    x=x0+radius*math.cos(t)
                    y=y0+radius*math.sin(t)

                    y=round(
                        y/
                        self.row_height
                    )*self.row_height

                    candidate={

                        "x":x,
                        "y":y,
                        "w":w,
                        "h":h

                    }

                    if self.legal(

                        candidate,
                        placed,
                        W,
                        H

                    ):

                        placement[idx,0]=x
                        placement[idx,1]=y

                        placed.append(
                            candidate
                        )

                        found=True
                        break

                if found:
                    break


            # -------- global fallback --------

            if not found:

                best=None
                best_cost=1e9

                xs=torch.arange(
                    w/2,
                    W-w/2,
                    self.step
                )

                ys=torch.arange(
                    h/2,
                    H-h/2,
                    self.row_height
                )

                for x in xs:

                    for y in ys:

                        candidate={

                            "x":float(x),
                            "y":float(y),
                            "w":w,
                            "h":h

                        }

                        if not self.legal(

                            candidate,
                            placed,
                            W,
                            H

                        ):

                            continue


                        cost=(

                            (float(x)-x0)**2
                            +
                            (float(y)-y0)**2

                        )


                        if cost<best_cost:

                            best=candidate
                            best_cost=cost


                if best is not None:

                    placement[idx,0]=best["x"]
                    placement[idx,1]=best["y"]

                    placed.append(
                        best
                    )


        return placement