class CommitMacroPositions:


    def __init__(

        self,

        data,

        boundary_assignment,

        interdependent_assignment,

        bridge_assignment,

        chip_width,
        chip_height

    ):


        self.data=data

        self.boundary=(
            boundary_assignment
        )

        self.interior=(
            interdependent_assignment
        )

        self.bridge=(
            bridge_assignment
        )


        self.W=chip_width
        self.H=chip_height


        self.final={}



    def clip(

        self,
        x,
        y

    ):


        x=max(
            0.5,
            min(
                self.W-.5,
                x
            )
        )


        y=max(
            0.5,
            min(
                self.H-.5,
                y
            )
        )


        return x,y



    def insert(

        self,
        source,
        name

    ):


        print(
            f"\n{name}"
        )


        count=0


        for m,d in source.items():


            x,y=(

                self.clip(

                    d["x"],
                    d["y"]

                )

            )


            if m in self.final:


                print(
                    f"{m} duplicate"
                )

                continue


            self.final[m]={

                "x":x,
                "y":y,

                "hub":
                d.get(
                    "hub",
                    -1
                ),

                "source":
                name

            }


            if m in self.data:


                try:

                    self.data[
                        m
                    ].x=x

                    self.data[
                        m
                    ].y=y

                except AttributeError:

                    pass

                except KeyError:

                    pass

                except TypeError:

                    pass


            count+=1


        print(
            f"added={count}"
        )



    def run(self):


        print(
            "\n"+"="*80
        )

        print(
            "COMMIT POSITIONS"
        )

        print(
            "="*80
        )


        self.insert(

            self.boundary,
            "boundary"

        )


        self.insert(

            self.interior,
            "interdependent"

        )


        self.insert(

            self.bridge,
            "bridge"

        )


        print(
            "\n"+"="*80
        )

        print(
            "COMMIT COMPLETE"
        )

        print(
            "="*80
        )

        print(

            f"Total placed:"
            f"{len(self.final)}"

        )


        return self.final


if __name__=="__main__":

    pass