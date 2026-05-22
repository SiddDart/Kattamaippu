# submissions/sidd/placement/preplace_anchor.py

import math


class PreplaceAnchor:


    def __init__(

        self,

        parsed_data,

        hubs

    ):


        self.data = parsed_data

        self.hubs = hubs


        self.anchor = self.data[
            "largest"
        ]


        self.nets = self.data[
            "nets"
        ]


        self.modules = self.data[
            "modules"
        ]



    def run(self):


        print(
            "\n"+"="*80
        )

        print(
            "PREPLACE ANCHOR"
        )

        print(
            "="*80
        )


        print(
            f"Anchor : "
            f"{self.anchor.name}"
        )


        # --------------------------
        # locate hub
        # --------------------------

        hub_id=None


        for hid,members in (

            self.hubs.items()

        ):


            if (

                self.anchor.name

                in

                members

            ):


                hub_id=hid

                break


        print(
            f"Hub : {hub_id}"
        )


        # --------------------------
        # connected ports
        # --------------------------

        connected_ports=[]


        for pin_name,pin_data in (

            self.nets.items()

        ):


            parent=(

                pin_name
                .split("/")[0]

            )


            if (

                parent

                !=

                self.anchor.name

            ):

                continue


            for name,node in (

                self.modules.items()

            ):


                if (

                    getattr(
                        node,
                        "type",
                        ""
                    )

                    ==

                    "PORT"

                ):


                    connected_ports.append(

                        {

                            "name":
                            name,

                            "x":
                            node.x,

                            "y":
                            node.y

                        }

                    )


        print(
            "\nConnected ports:\n"
        )


        for p in connected_ports:


            print(

                f"{p['name']} "

                f"("

                f"{p['x']:.2f},"

                f"{p['y']:.2f}"

                f")"

            )


        # --------------------------
        # cluster nearby ports
        # --------------------------

        clusters=[]

        threshold=10


        for p in connected_ports:


            inserted=False


            for c in clusters:


                cx=(

                    sum(
                        x["x"]
                        for x in c
                    )

                    /

                    len(c)

                )


                cy=(

                    sum(
                        x["y"]
                        for x in c
                    )

                    /

                    len(c)

                )


                d=math.sqrt(

                    (p["x"]-cx)**2+

                    (p["y"]-cy)**2

                )


                if d<threshold:


                    c.append(
                        p
                    )

                    inserted=True

                    break


            if not inserted:

                clusters.append(
                    [p]
                )


        print(
            "\nPort clusters:\n"
        )


        for i,c in enumerate(
            clusters
        ):


            print(

                f"Cluster {i}"

                f" size={len(c)}"

            )


        chosen=max(

            clusters,

            key=lambda x:len(x)

        )


        print(
            "\nChosen cluster:\n"
        )


        for p in chosen:

            print(
                p["name"]
            )


        return {

            "anchor":

                self.anchor,

            "hub":

                hub_id,

            "ports":

                chosen

        }



if __name__=="__main__":

    print(
        "Call from main.py"
    )
