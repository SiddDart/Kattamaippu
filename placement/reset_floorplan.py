# submissions/sidd/placement/reset_floorplan.py


class FloorplanReset:


    def __init__(

        self,

        parsed_data,

        hubs,

        roles,

        backbone

    ):

        self.data = parsed_data

        self.hubs = hubs

        self.roles = roles

        self.backbone = backbone


    def reset(self):


        print(
            "\n"+"="*80
        )

        print(
            "RESET FLOORPLAN"
        )

        print(
            "="*80
        )


        hard = self.data["hard"]

        reset_count = 0


        for macro in hard:


            # ----------------------
            # erase geometry only
            # ----------------------

            macro.x = None
            macro.y = None

            # future usage
            macro.fixed = False
            macro.placed = False
            macro.rotation = None

            # halo placeholder
            macro.halo = 0


            reset_count += 1


        print(
            f"Reset macros : "
            f"{reset_count}"
        )


        print(
            "\nPreserved:"
        )

        print(
            "  ✓ hubs"
        )

        print(
            "  ✓ roles"
        )

        print(
            "  ✓ communication graph"
        )

        print(
            "  ✓ backbone"
        )

        print(
            "  ✓ dimensions"
        )

        print(
            "  ✓ largest macro"
        )


        print(
            "\nRemoved:"
        )

        print(
            "  x old x"
        )

        print(
            "  x old y"
        )

        print(
            "  x placement state"
        )

        print(
            "  x fixed state"
        )


        print(
            "\nFloorplan now empty."
        )


        return {

            "data":self.data,

            "hubs":self.hubs,

            "roles":self.roles,

            "backbone":self.backbone

        }



if __name__=="__main__":

    print(
        "Run through main.py"
    )