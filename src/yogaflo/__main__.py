import markovify
import random
from typing import cast, List

from yogaflo import constraints, data, yogaflo


def build_model(
    flows: List[List[data.Pose]], state_size: int
) -> markovify.Chain:
    if not all(yogaflo.validate_flow(flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def console_entry() -> None:
    flows = data.read_flows()

    model = build_model(flows, state_size=1)

    seed = random.randint(0, 9999)
    # seed = 206
    random.seed(seed)
    for constraint in [
        constraints.is_easy,
        constraints.is_hard,
        constraints.is_easy,
    ]:
        states = constraints.find_matching(
            lambda: cast(List[data.Pose], model.walk()), constraint
        )
        flow = yogaflo.desugar_flow(states)
        yogaflo.print_flow(flow)
        print()
    # print(seed)


if __name__ == "__main__":
    console_entry()
