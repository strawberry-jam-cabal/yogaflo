import markovify
import random
from typing import cast, Dict, List

from yogaflo import constraints, data, yogaflo


def build_model(
    pose_map: Dict[str, data.Pose], flows: List[List[str]], state_size: int
) -> markovify.Chain:
    if not all(yogaflo.validate_flow(pose_map, flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def console_entry() -> None:
    poses = data.read_poses()
    pose_map = {pose.name: pose for pose in poses}

    flows = data.read_flows()

    model = build_model(pose_map, flows, state_size=1)

    seed = random.randint(0, 9999)
    # seed = 206
    random.seed(seed)
    for constraint in [
        constraints.is_easy,
        constraints.is_hard,
        constraints.is_easy,
    ]:
        states = constraints.find_matching(
            lambda: cast(List[str], model.walk()), constraint, pose_map
        )
        flow = yogaflo.desugar_flow(pose_map, states, "left")
        yogaflo.print_flow(flow)
        print()
    # print(seed)


if __name__ == "__main__":
    console_entry()
