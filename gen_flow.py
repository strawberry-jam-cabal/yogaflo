import json
import markovify
import random
from typing import Any, Dict, IO, List, NamedTuple


class PoseData(NamedTuple):
    mirror: bool

    @classmethod
    def from_json(cls, js: Any) -> "PoseData":
        return PoseData(js.get("mirror") is True)


def read_poses(posefile: IO[str]) -> Dict[str, PoseData]:
    poses = json.load(posefile)

    if not isinstance(poses, dict):
        raise ValueError("Poses are not a dict: " + str(poses))

    for name, value in poses.items():
        poses[name] = PoseData.from_json(value)
    return poses


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
    result = flow.copy()
    for i, pose in enumerate(result):
        if pose in poses and poses[pose].mirror:
            result[i] = f"{side} {pose}"

    return result


def desugar_flow(
    poses: Dict[str, PoseData], flow: List[str], side: str
) -> List[str]:
    no_mirror = remove_mirrors(poses, flow, side)

    primary = choose_side(poses, no_mirror, side)
    secondary = choose_side(poses, no_mirror, mirror(side))
    if primary != secondary:
        if primary[-1] == secondary[0]:
            secondary = secondary[1:]
        return primary + secondary
    else:
        return primary


def print_flow(flow: List[str]) -> None:
    for pose in flow:
        print(pose)


def validate_flow(poses: Dict[str, PoseData], flow: List[str]) -> bool:
    try:
        desugar_flow(poses, flow, "left")
        return True
    except Exception:
        return False


def build_model(
    poses: Dict[str, PoseData], flows: List[List[str]], state_size: int
) -> markovify.Chain:
    if not all(validate_flow(poses, flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def main() -> None:
    poses = read_poses(open("poses.json", "r"))

    flows = json.load(open("flows/flows-tobin.json", "r"))

    model = build_model(poses, flows, state_size=2)

    seed = random.randint(0, 999)
    seed = 206
    random.seed(seed)
    for _ in range(3):
        print_flow(desugar_flow(poses, model.walk(), "left"))
        print()
    print(seed)


if __name__ == "__main__":
    main()
