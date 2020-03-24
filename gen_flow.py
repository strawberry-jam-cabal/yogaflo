import json
import markovify
from typing import Any, Dict, List, NamedTuple


class PoseData(NamedTuple):
    mirror: bool

    @classmethod
    def from_json(cls, js: Any) -> "PoseData":
        return PoseData(js.get("mirror") is True)


def mirror(side: str) -> str:
    if side == "left":
        return "right"
    if side == "right":
        return "left"

    raise ValueError(f"Unknown side: {side}")


def remove_mirrors(
    poses: Dict[str, PoseData], flow: List[str], side: str
) -> List[str]:
    latest_reversable = None
    result = flow.copy()

    for i, pose in enumerate(flow):
        if pose not in poses:
            raise ValueError(f"Unknown pose: {pose}")

        if pose == "mirror":
            if latest_reversable is None:
                raise ValueError("Nothing to mirror")
            result[i] = f"{mirror(side)} {result[latest_reversable]}"
            result[latest_reversable] = f"{side} {result[latest_reversable]}"
            latest_reversable = None
        elif poses[pose].mirror:
            latest_reversable = i

    return result


def choose_side(
    poses: Dict[str, PoseData], flow: List[str], side: str
) -> List[str]:
    result = remove_mirrors(poses, flow, side)

    for i, pose in enumerate(result):
        if pose in poses and poses[pose].mirror:
            result[i] = f"{side} {pose}"

    return result


def can_mirror(poses: Dict[str, PoseData], flow: List[str]) -> bool:
    return any(
        pose in poses and poses[pose].mirror
        for pose in remove_mirrors(poses, flow, "left")
    )


def validate_flow(poses: Dict[str, PoseData], flow: List[str]) -> bool:
    return choose_side(poses, flow, "left") is not None


def build_transition_graph(
    poses: Dict[str, PoseData], flows: List[List[str]], state_size: int
) -> markovify.Chain:
    if not all(validate_flow(poses, flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def main() -> None:
    poses = json.load(open("poses.json", "r"))
    for name, value in poses.items():
        poses[name] = PoseData.from_json(value)

    flows = json.load(open("flows/flows-tobin.json", "r"))

    model = build_transition_graph(poses, flows, state_size=2)

    for _ in range(3):
        flow = model.walk()

        if can_mirror(poses, flow):
            left = choose_side(poses, flow, "left")
            right = choose_side(poses, flow, "right")
            if left[-1] == right[0]:
                right = right[1:]
            flow = left + right
        else:
            flow = choose_side(poses, flow, "left")

        for pose in flow:
            print(pose)
        print()


if __name__ == "__main__":
    main()
