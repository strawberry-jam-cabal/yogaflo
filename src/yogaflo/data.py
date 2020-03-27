import json
import pkg_resources
from typing import IO, List, NamedTuple


class Pose(NamedTuple):
    name: str
    difficulty: int
    asymmetric: bool


def open_data(name: str) -> IO[bytes]:
    return pkg_resources.resource_stream(__name__, name)


def read_poses() -> List[Pose]:
    return [Pose(**row) for row in json.load(open_data("data/poses.json"))]


def read_flows() -> List[List[str]]:
    result = json.load(open_data("data/flows/flows-tobin.json"))

    if not isinstance(result, list):
        raise ValueError("Flow file does not contain a list of flows")

    for flow in result:
        if not isinstance(flow, list):
            raise ValueError("Flow is not a list of poses")

        for pose in flow:
            if not isinstance(pose, str):
                raise ValueError("Pose is not a string")

    return result
