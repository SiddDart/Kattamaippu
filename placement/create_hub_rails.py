# submissions/sidd/placement/create_hub_rails.py

class CreateHubRails:

    def __init__(

        self,

        chip_width,
        chip_height,

        rail_history,

        anchor,

        thickness

    ):

        self.W=chip_width
        self.H=chip_height

        self.anchor=anchor

        self.t=thickness

        self.history=rail_history


    def create(self):


        print("\n"+"="*80)
        print("CREATE RAIL")
        print("="*80)


        if len(self.history)==0:


            left=0
            right=self.W

            bottom=0
            top=self.H


        else:


            prev=self.history[-1]


            left=(
                prev["left"]
                +self.t
            )

            right=(
                prev["right"]
                -self.t
            )

            bottom=(
                prev["bottom"]
                +self.t
            )

            top=(
                prev["top"]
                -self.t
            )


        rail_id=(
            len(
                self.history
            )+1
        )


        rail={

            "id":rail_id,

            "left":left,
            "right":right,

            "top":top,
            "bottom":bottom,

            "thickness":self.t,


            "slots":{

                "left":[],

                "top":[],

                "right":[],

                "bottom":[]

            },


            "occupied":{

                "left":0,

                "top":0,

                "right":0,

                "bottom":0

            },


            "hub_regions":{

                "left":[],

                "top":[],

                "right":[],

                "bottom":[]

            }

        }


        # much denser
        spacing=.35


        # ----------------
        # LEFT
        # ----------------

        y=bottom


        while y<=top:


            x=left


            if not self._inside_anchor(

                x,
                y

            ):

                rail["slots"][
                    "left"
                ].append(

                    (x,y)

                )


            y+=spacing



        # ----------------
        # TOP
        # ----------------

        x=left


        while x<=right:


            y=top


            if not self._inside_anchor(

                x,
                y

            ):

                rail["slots"][
                    "top"
                ].append(

                    (x,y)

                )


            x+=spacing



        # ----------------
        # RIGHT
        # ----------------

        y=top


        while y>=bottom:


            x=right


            if not self._inside_anchor(

                x,
                y

            ):

                rail["slots"][
                    "right"
                ].append(

                    (x,y)

                )


            y-=spacing



        # ----------------
        # BOTTOM
        # ----------------

        x=right


        while x>=left:


            y=bottom


            if not self._inside_anchor(

                x,
                y

            ):

                rail["slots"][
                    "bottom"
                ].append(

                    (x,y)

                )


            x-=spacing



        self.history.append(
            rail
        )


        total=(

            len(
                rail["slots"]["left"]
            )

            +

            len(
                rail["slots"]["top"]
            )

            +

            len(
                rail["slots"]["right"]
            )

            +

            len(
                rail["slots"]["bottom"]
            )

        )


        print(
            f"Rail {rail_id}"
        )

        print(
            f"Total slots:{total}"
        )


        return rail



    def _inside_anchor(

        self,

        x,
        y

    ):


        ax1=(

            self.anchor.x
            -
            self.anchor.width/2

        )


        ax2=(

            self.anchor.x
            +
            self.anchor.width/2

        )


        ay1=(

            self.anchor.y
            -
            self.anchor.height/2

        )


        ay2=(

            self.anchor.y
            +
            self.anchor.height/2

        )


        return(

            x>=ax1
            and
            x<=ax2

            and

            y>=ay1
            and
            y<=ay2

        )