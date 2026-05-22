# submissions/sidd/parser/parse_netlist.py

from collections import Counter


class MacroNode:

    def __init__(self, name):

        self.name = name
        self.attrs = {}

        self.width = 0.0
        self.height = 0.0

        self.x = 0.0
        self.y = 0.0

        self.type = ""

        self._active = None


    @property
    def area(self):

        return self.width * self.height



class NetlistParser:

    def __init__(self, filepath):

        self.filepath = filepath

        self.nodes = {}

        self.hard = []
        self.soft = []
        self.ports = []
        self.pins = []

        self.largest_macro = None



    def parse(self):

        print(
            f"\nReading: {self.filepath}"
        )

        current = None
        depth = 0


        with open(
            self.filepath,
            "r",
            encoding="utf8"
        ) as f:


            for raw in f:

                line = raw.strip()


                if line == "node {":

                    current = MacroNode(
                        "temp"
                    )

                    depth = 1

                    continue


                if current is None:

                    continue


                if line.endswith("{"):

                    depth += 1


                elif line == "}":

                    depth -= 1


                    if depth == 0:

                        self._finalize(
                            current
                        )

                        current = None


                    continue


                if line.startswith(
                    "name:"
                ):

                    try:

                        current.name = (
                            line.split('"')[1]
                        )

                    except Exception:

                        pass


                elif line.startswith(
                    "key:"
                ):

                    try:

                        current._active = (
                            line.split('"')[1]
                        )

                    except Exception:

                        pass


                elif "placeholder:" in line:

                    if current._active:

                        try:

                            value = (
                                line.split('"')[1]
                            )

                            current.attrs[
                                current._active
                            ] = value

                        except Exception:

                            pass


                elif line.startswith(
                    "f:"
                ):

                    if current._active:

                        try:

                            value=float(

                                line.split(
                                    ":"
                                )[1]

                            )

                            current.attrs[
                                current._active
                            ]=value

                        except Exception:

                            pass


        self.summary()


        return {

            "nodes":
            self.nodes,

            "hard":
            self.hard,

            "soft":
            self.soft,

            "ports":
            self.ports,

            "pins":
            self.pins,

            "largest":
            self.largest_macro,


            # added
            "modules":
            self.nodes,


            "nets":{

                x.name:x.attrs

                for x in self.pins

            }

        }



    def _finalize(
        self,
        node
    ):

        a=node.attrs


        node.type=a.get(
            "type",
            ""
        )


        node.width=a.get(
            "width",
            0.0
        )


        node.height=a.get(
            "height",
            0.0
        )


        node.x=a.get(
            "x",
            0.0
        )


        node.y=a.get(
            "y",
            0.0
        )


        self.nodes[
            node.name
        ]=node



        if node.type=="PORT":

            self.ports.append(
                node
            )

            return



        if (

            "/IP" in node.name

            or

            "/OP" in node.name

        ):

            self.pins.append(
                node
            )

            return



        if (

            "orientation"
            in a

        ):

            self.hard.append(
                node
            )


            if (

                self.largest_macro
                is None

                or

                node.area >

                self.largest_macro.area

            ):

                self.largest_macro=node


            return



        if (

            node.name.startswith(
                "Grp_"
            )

            and

            node.width>0

            and

            node.height>0

        ):

            self.soft.append(
                node
            )



    def summary(self):

        print(
            "\n"+"="*70
        )

        print(
            "COUNTS"
        )

        print(
            "="*70
        )


        print(
            f"Hard macros : {len(self.hard)}"
        )

        print(
            f"Soft macros : {len(self.soft)}"
        )

        print(
            f"Ports       : {len(self.ports)}"
        )

        print(
            f"Pins        : {len(self.pins)}"
        )


        print(
            "\n"+"="*70
        )

        print(
            "LARGEST HARD MACRO"
        )

        print(
            "="*70
        )


        if self.largest_macro:

            x=self.largest_macro


            print(
                f"name : {x.name}"
            )

            print(
                f"width : {x.width}"
            )

            print(
                f"height : {x.height}"
            )

            print(
                f"area : {x.area}"
            )


        print(
            "\n"+"="*70
        )

        print(
            "TYPE SUMMARY"
        )


        c=Counter()

        c["HARD"]=len(
            self.hard
        )

        c["SOFT"]=len(
            self.soft
        )

        c["PORT"]=len(
            self.ports
        )


        print(c)



if __name__=="__main__":

    FILE=(

        "external/"
        "MacroPlacement/"
        "Testcases/"
        "ICCAD04/"
        "ibm01/"
        "netlist.pb.txt"

    )


    p=NetlistParser(
        FILE
    )


    p.parse()
