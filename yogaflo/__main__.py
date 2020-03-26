import json
import markovify
import random
from typing import Dict, List

from yogaflo.data import Pose, read_poses
from yogaflo.yogaflo import desugar_flow, print_flow, validate_flow


def build_model(
    pose_map: Dict[str, Pose], flows: List[List[str]], state_size: int
) -> markovify.Chain:
    if not all(validate_flow(pose_map, flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def console_entry() -> None:
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
    console_entry()
