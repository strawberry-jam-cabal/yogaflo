import json
import os
from typing import Dict

from yogaflo import data, yogaflo

_pose_map = None


def pose_map() -> Dict[str, data.Pose]:
    """Get the map of poses reading from file or using cache."""
    global _pose_map
    if _pose_map is None:
        path = os.path.join("data", "poses.json")
        _pose_map = {pose.name: pose for pose in data.read_poses(path)}
    return _pose_map


def test_all_flows_valid() -> None:
    for (dirpath, dirname, filenames) in os.walk("data/flows"):
        for filename in filenames:
            if filename.endswith(".json"):
                with open(os.path.join(dirpath, filename), "r") as handle:
                    for flow in json.load(handle):
                        assert yogaflo.validate_flow(pose_map(), flow)


def test_valid_flows() -> None:
    assert yogaflo.validate_flow(pose_map(), ["mountain", "downward dog"])

    assert not yogaflo.validate_flow(pose_map(), ["mirror"])
    assert not yogaflo.validate_flow(pose_map(), ["downward dog", "mirror"])

    assert yogaflo.validate_flow(pose_map(), ["warrior 2", "mirror"])
    assert not yogaflo.validate_flow(
        pose_map(), ["warrior 2", "mirror", "mirror"]
    )


def test_repeat_mirror() -> None:
    assert [] == yogaflo.desugar_flow(pose_map(), [], "left")
    assert ["left warrior 2", "right warrior 2"] == yogaflo.desugar_flow(
        pose_map(), ["warrior 2", "mirror"], "left"
    )
    assert ["left warrior 2", "right warrior 2"] == yogaflo.desugar_flow(
        pose_map(), ["warrior 2"], "left"
    )
