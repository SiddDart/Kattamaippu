from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from submissions.sidd.main import main


class SiddPlacer:

    def place(self, benchmark):

        return main(
            benchmark=benchmark
        )
