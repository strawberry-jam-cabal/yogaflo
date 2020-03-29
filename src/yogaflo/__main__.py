import argparse
import markovify
import random
from typing import cast, List

from yogaflo import __about__, constraints, data, yogaflo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="yogaflo", description="Generate a yoga flow"
    )

    parser.add_argument(
        "-c",
        "--context",
        default=1,
        type=int,
        help="Set the size of context in the markov chain",
        metavar="SIZE",
    )

    parser.add_argument(
        "-s",
        "--seed",
        default=random.random(),
        help="Set the random seed used to generate flows",
        metavar="SEED",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__about__.__version__}",
    )

    return parser.parse_args()


def build_model(
    flows: List[List[data.Pose]], state_size: int
) -> markovify.Chain:
    if not all(yogaflo.validate_flow(flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def console_entry() -> None:
    args = parse_args()

    flows = data.read_flows()

    model = build_model(flows, state_size=args.context)

    random.seed(args.seed)
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


if __name__ == "__main__":
    console_entry()
