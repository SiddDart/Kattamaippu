import math
import numpy as np
import torch

from submissions.sidd.graph.build_graph import GraphBuilder


class SoftMacroPlacer:

    def __init__(self, netlist_path):

        self.grid = 0.5
        self.margin = 0.0

        self.builder = GraphBuilder(
            netlist_path
        )

        self.G = self.builder.build()


    def overlap(

        self,

        x1,y1,w1,h1,
        x2,y2,w2,h2

    ):

        sx=(w1+w2)/2
        sy=(h1+h2)/2

        return (

            abs(x1-x2)<sx
            and
            abs(y1-y2)<sy

        )


    def legal(

        self,
        x,y,w,h,
        occupied,
        cw,ch

    ):

        if x-w/2<0:
            return False

        if x+w/2>cw:
            return False

        if y-h/2<0:
            return False

        if y+h/2>ch:
            return False


        for px,py,pw,ph in occupied:

            if self.overlap(

                x,y,w,h,
                px,py,pw,ph

            ):

                return False


        return True



    def place(

        self,
        benchmark,
        placement

    ):

        n_hard=benchmark.num_hard_macros
        n_soft=benchmark.num_soft_macros


        sizes=(

            benchmark
            .macro_sizes
            .cpu()
            .numpy()

        )


        cw=float(
            benchmark.canvas_width
        )

        ch=float(
            benchmark.canvas_height
        )


        occupied=[]
        macro_pos={}


        data=self.builder.data

        hard=data["hard"]
        soft=data["soft"]


        print(
            f"\nSOFT={n_soft}"
        )


        # --------------------------------
        # freeze hard macros
        # --------------------------------

        for i in range(n_hard):

            x=float(
                placement[i,0]
            )

            y=float(
                placement[i,1]
            )

            w=float(
                sizes[i,0]
            )

            h=float(
                sizes[i,1]
            )


            occupied.append(

                (
                    x,
                    y,
                    w,
                    h
                )

            )


            if i < len(hard):

                macro_pos[
                    hard[i].name
                ]=(x,y)



        placed=0


        # ------------------------------
        # largest soft first
        # ------------------------------

        areas=[]

        for sid in range(

            min(
                n_soft,
                len(soft)
            )

        ):

            idx=n_hard+sid

            a=(

                sizes[idx,0]
                *
                sizes[idx,1]

            )

            areas.append(
                (sid,a)
            )


        order=sorted(

            areas,

            key=lambda x:-x[1]

        )



        for sid,_ in order:


            idx=n_hard+sid

            node=soft[sid]

            name=node.name


            w=float(
                sizes[idx,0]
            )

            h=float(
                sizes[idx,1]
            )


            # -------------------
            # graph centroid
            # -------------------

            cx=0.0
            cy=0.0
            total=0.0


            if name in self.G:


                for nb in (

                    self.G.neighbors(
                        name
                    )

                ):


                    if nb not in macro_pos:

                        continue


                    px,py=macro_pos[
                        nb
                    ]


                    ww=(

                        self.G[
                            name
                        ][nb]

                        .get(
                            "weight",
                            1
                        )

                    )


                    cx+=ww*px
                    cy+=ww*py

                    total+=ww


            if total>0:

                cx/=total
                cy/=total

            else:

                cx=cw/2
                cy=ch/2



            found=False


            # -------------------
            # spiral search
            # -------------------

            for r in np.arange(

                0,
                12,
                self.grid

            ):


                for t in np.arange(

                    0,
                    2*np.pi,
                    np.pi/8

                ):


                    x=(
                        cx
                        +
                        r*
                        math.cos(t)
                    )

                    y=(
                        cy
                        +
                        r*
                        math.sin(t)
                    )


                    if self.legal(

                        x,y,w,h,
                        occupied,
                        cw,ch

                    ):


                        placement[
                            idx,
                            0
                        ]=torch.tensor(
                            float(x),
                            dtype=placement.dtype
                        )


                        placement[
                            idx,
                            1
                        ]=torch.tensor(
                            float(y),
                            dtype=placement.dtype
                        )


                        occupied.append(

                            (
                                x,
                                y,
                                w,
                                h
                            )

                        )


                        macro_pos[
                            name
                        ]=(x,y)


                        placed+=1


                        found=True

                        break


                if found:
                    break


            if not found:

                print(
                    f"{name} failed"
                )


        print(
            f"\nplaced={placed}/{n_soft}"
        )


        return placement