from typing import Callable, List

from yogaflo import data, yogaflo


def find_matching(
    gen_flow: Callable[[], List[data.Pose]],
    constraint: Callable[[List[data.Pose]], bool],
    max_tries: int = 100,
) -> List[data.Pose]:
    for _ in range(max_tries):
        flow = gen_flow()
        if constraint(flow):
            return flow
    raise ValueError("Could not generate a flow matching the constraints")


def total_difficulty(flow: List[data.Pose]) -> int:
    return sum(pose.difficulty for pose in yogaflo.remove_mirrors(flow))


def is_easy(flow: List[data.Pose]) -> bool:
    avg_difficulty = total_difficulty(flow) / len(flow)

    return (10 <= len(flow) <= 20) and (avg_difficulty < 1.2)


def is_hard(flow: List[data.Pose]) -> bool:
    avg_difficulty = total_difficulty(flow) / len(flow)

    return (15 <= len(flow) <= 30) and (avg_difficulty > 1.4)
