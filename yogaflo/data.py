import json
from typing import List, NamedTuple


class Pose(NamedTuple):
    name: str
    difficulty: int
    mirror: bool


def read_poses(posefile_path: str) -> List[Pose]:
    with open(posefile_path, "r") as handle:
        return [Pose(**row) for row in json.load(handle)]
