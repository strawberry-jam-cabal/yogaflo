import json
import pkg_resources
from typing import Any, Dict, IO, List, NamedTuple, Optional


class Pose(NamedTuple):
    name: str
    difficulty: int
    can_mirror: bool
    side: Optional[bool]


def read_poses() -> Dict[str, Pose]:
    stream = pkg_resources.resource_stream(__name__, "data/poses.json")
    poses = [Pose(side=None, **row) for row in json.load(stream)]
    return {pose.name: pose for pose in poses}


def parse_flows(stream: IO[Any]) -> List[List[str]]:
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


def read_flows(pose_map: Dict[str, Pose]) -> List[List[Pose]]:
    result = []

    for name in pkg_resources.resource_listdir(__name__, "data/flows"):
        stream = pkg_resources.resource_stream(__name__, "data/flows/" + name)
        flows = pose_lookup(pose_map, parse_flows(stream))
        result.extend(flows)
    return result


def pose_lookup(
    pose_map: Dict[str, Pose], flows: List[List[str]]
) -> List[List[Pose]]:
    result = []
    for names in flows:
        flow = []
        for name in names:
            if name not in pose_map:
                raise ValueError(f"Unknown pose ({name}) in flow: {names}")
            flow.append(pose_map[name])
        result.append(flow)
    return result
