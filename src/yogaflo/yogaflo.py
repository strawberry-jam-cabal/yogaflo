from typing import Dict, List

from yogaflo import data


PoseMap = Dict[str, data.Pose]


def mirror(side: str) -> str:
    if side == "left":
        return "right"
    if side == "right":
        return "left"

    raise ValueError(f"Unknown side: {side}")


def remove_mirrors(pose_map: PoseMap, flow: List[str], side: str) -> List[str]:
    latest_reversable = None
    result = flow.copy()

    for i, pose in enumerate(flow):
        if pose not in pose_map:
            raise ValueError(f"Unknown pose: {pose}")

        if pose == "mirror":
            if latest_reversable is None:
                raise ValueError("Nothing to mirror")
            result[i] = f"{mirror(side)} {result[latest_reversable]}"
            result[latest_reversable] = f"{side} {result[latest_reversable]}"
            latest_reversable = None
        elif pose_map[pose].asymmetric:
            latest_reversable = i

    return result


def choose_side(pose_map: PoseMap, flow: List[str], side: str) -> List[str]:
    result = flow.copy()
    for i, pose in enumerate(result):
        if pose in pose_map and pose_map[pose].asymmetric is True:
            result[i] = f"{side} {pose}"

    return result


def desugar_flow(pose_map: PoseMap, flow: List[str], side: str) -> List[str]:
    no_mirror = remove_mirrors(pose_map, flow, side)

    primary = choose_side(pose_map, no_mirror, side)
    secondary = choose_side(pose_map, no_mirror, mirror(side))
    if primary != secondary:
        if primary[-1] == secondary[0]:
            secondary = secondary[1:]
        return primary + secondary
    else:
        return primary


def print_flow(flow: List[str]) -> None:
    for pose in flow:
        print(pose)


def validate_flow(pose_map: PoseMap, flow: List[str]) -> bool:
    try:
        desugar_flow(pose_map, flow, "left")
        return True
    except Exception:
        return False
