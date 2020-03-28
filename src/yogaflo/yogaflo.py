from typing import Dict, List

from yogaflo import data


PoseMap = Dict[str, data.Pose]


def mirror(side: str) -> str:
    if side == "left":
        return "right"
    if side == "right":
        return "left"

    raise ValueError(f"Unknown side: {side}")


def remove_mirrors(flow: List[data.Pose]) -> List[data.Pose]:
    latest_reversable = None
    result = flow.copy()

    for i, pose in enumerate(flow):
        if pose.name == "mirror":
            if latest_reversable is None:
                raise ValueError("Nothing to mirror")

            result[i] = result[latest_reversable]._replace(side=False)
            result[latest_reversable] = result[latest_reversable]._replace(
                side=True
            )

            latest_reversable = None
        elif pose.can_mirror:
            latest_reversable = i

    return result


def desugar_flow(flow: List[data.Pose]) -> List[data.Pose]:
    def set_side(pose: data.Pose, side: bool) -> data.Pose:
        if pose.can_mirror and pose.side is None:
            return pose._replace(side=side)
        return pose

    result = remove_mirrors(flow)

    if any(pose.can_mirror and pose.side is None for pose in result):
        repeat = result[1:] if result[0] == result[-1] else result[::]
        result = [set_side(pose, True) for pose in result]
        return result + [set_side(pose, False) for pose in repeat]

    return result


def print_flow(
    flow: List[data.Pose], first_side: str = "left", second_side: str = "right"
) -> None:
    for pose in flow:
        if pose.side is True:
            print(f"{first_side} {pose.name}")
        elif pose.side is False:
            print(f"{second_side} {pose.name}")
        else:
            print(pose.name)


def validate_flow(flow: List[data.Pose]) -> bool:
    try:
        desugar_flow(flow)
        return True
    except Exception:
        return False
