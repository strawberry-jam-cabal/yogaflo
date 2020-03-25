import json
import markovify
import random
from typing import Dict, List, NamedTuple


class Pose(NamedTuple):
    name: str
    difficulty: int
    mirror: bool


def read_poses(posefile_path: str) -> List[Pose]:
    with open(posefile_path, "r") as handle:
        return [Pose(**row) for row in json.load(handle)]


def mirror(side: str) -> str:
    if side == "left":
        return "right"
    if side == "right":
        return "left"

    raise ValueError(f"Unknown side: {side}")


def remove_mirrors(
    pose_map: Dict[str, Pose], flow: List[str], side: str
) -> List[str]:
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
        elif pose_map[pose].mirror:
            latest_reversable = i

    return result


def choose_side(
    pose_map: Dict[str, Pose], flow: List[str], side: str
) -> List[str]:
    result = flow.copy()
    for i, pose in enumerate(result):
        if pose in pose_map and pose_map[pose].mirror is True:
            result[i] = f"{side} {pose}"

    return result


def desugar_flow(
    pose_map: Dict[str, Pose], flow: List[str], side: str
) -> List[str]:
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


def validate_flow(pose_map: Dict[str, Pose], flow: List[str]) -> bool:
    try:
        desugar_flow(pose_map, flow, "left")
        return True
    except Exception:
        return False


def build_model(
    pose_map: Dict[str, Pose], flows: List[List[str]], state_size: int
) -> markovify.Chain:
    if not all(validate_flow(pose_map, flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def main() -> None:
    poses = read_poses("poses.json")
    pose_map = {pose.name: pose for pose in poses}

    flows = json.load(open("flows/flows-tobin.json", "r"))

    model = build_model(pose_map, flows, state_size=2)

    seed = random.randint(0, 999)
    seed = 206
    random.seed(seed)
    for _ in range(3):
        print_flow(desugar_flow(pose_map, model.walk(), "left"))
        print()
    print(seed)


if __name__ == "__main__":
    main()
