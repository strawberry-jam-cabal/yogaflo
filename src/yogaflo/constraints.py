from typing import Callable, Dict, List

from yogaflo import data


def find_matching(
    gen_flow: Callable[[], List[str]],
    constraint: Callable[[Dict[str, data.Pose], List[str]], bool],
    pose_map: Dict[str, data.Pose],
    max_tries: int = 100,
) -> List[str]:
    for _ in range(max_tries):
        flow = gen_flow()
        if constraint(pose_map, flow):
            return flow
    raise ValueError("Could not generate a flow matching the constraints")


def total_difficulty(pose_map: Dict[str, data.Pose], flow: List[str]) -> int:
    total = 0
    last_asymmetric = None
    for name in flow:
        pose = pose_map[name]
        if pose == "mirror":
            if last_asymmetric is None:
                raise ValueError("Nothing to mirror: " + str(flow))
            total += last_asymmetric.difficulty
        else:
            total += pose.difficulty

        if pose.asymmetric:
            last_asymmetric = pose

    return total


def is_easy(pose_map: Dict[str, data.Pose], flow: List[str]) -> bool:
    avg_difficulty = total_difficulty(pose_map, flow) / len(flow)

    return 10 <= len(flow) <= 20 and avg_difficulty < 1.2


def is_hard(pose_map: Dict[str, data.Pose], flow: List[str]) -> bool:
    avg_difficulty = total_difficulty(pose_map, flow) / len(flow)

    return 15 <= len(flow) <= 30 and avg_difficulty > 1.4
