import json
import pkg_resources
from typing import IO, List, NamedTuple


class Pose(NamedTuple):
    name: str
    difficulty: int
    asymmetric: bool


def read_poses() -> List[Pose]:
    stream = pkg_resources.resource_stream(__name__, "data/poses.json")
    return [Pose(**row) for row in json.load(stream)]


def parse_flows(stream: IO[bytes]) -> List[List[str]]:
    result = json.load(stream)

    if not isinstance(result, list):
        raise ValueError("Flow file does not contain a list of flows")

    for flow in result:
        if not isinstance(flow, list):
            raise ValueError("Flow is not a list of poses")

        for pose in flow:
            if not isinstance(pose, str):
                raise ValueError("Pose is not a string")

    return result


def read_flows() -> List[List[str]]:
    result = []

    for name in pkg_resources.resource_listdir(__name__, "data/flows"):
        stream = pkg_resources.resource_stream(__name__, "data/flows/" + name)
        result.extend(parse_flows(stream))

    return result
