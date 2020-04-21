from typing import Dict, List

from yogaflo import data, yogaflo


_pose_map = None


def pose_map() -> Dict[str, data.Pose]:
    global _pose_map
    if _pose_map is None:
        _pose_map = data.read_poses()
    return _pose_map


def from_names(names: List[str]) -> List[data.Pose]:
    pm = pose_map()
    return [pm[name] for name in names]


def test_all_flows_valid() -> None:
    for flow in data.read_flows(pose_map()):
        assert yogaflo.validate_flow(flow)


def test_valid_flows() -> None:
    assert yogaflo.validate_flow(from_names(["mountain", "downward dog"]))

    assert not yogaflo.validate_flow(from_names(["mirror"]))
    assert not yogaflo.validate_flow(from_names(["downward dog", "mirror"]))

    assert yogaflo.validate_flow(from_names(["warrior 2", "mirror"]))
    assert not yogaflo.validate_flow(
        from_names(["warrior 2", "mirror", "mirror"])
    )


def test_repeat_mirror() -> None:
    assert [] == yogaflo.desugar_flow([])

    assert [
        pose_map()["warrior 2"]._replace(side=True),
        pose_map()["warrior 2"]._replace(side=False),
    ] == yogaflo.desugar_flow(from_names(["warrior 2", "mirror"]))

    assert [
        pose_map()["warrior 2"]._replace(side=True),
        pose_map()["reversed warrior"]._replace(side=True),
        pose_map()["warrior 2"]._replace(side=False),
        pose_map()["reversed warrior"]._replace(side=False),
    ] == yogaflo.desugar_flow(from_names(["warrior 2", "reversed warrior"]))
