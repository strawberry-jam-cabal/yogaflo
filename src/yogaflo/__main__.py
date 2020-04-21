import argparse
import markovify
import random
from typing import cast, List, Optional

from yogaflo import __about__, constraints, data, yogaflo


def parse_args(args: Optional[str] = None) -> argparse.Namespace:
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
        "--flows",
        default=None,
        help="Additional flows used for training",
        metavar="FLOW_FILE",
    )

    parser.add_argument(
        "--no-builtin-flows",
        action="store_true",
        help="Only run user input flows",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__about__.__version__}",
    )

    return parser.parse_args(args)


def build_model(
    flows: List[List[data.Pose]], state_size: int
) -> markovify.Chain:
    if not all(yogaflo.validate_flow(flow) for flow in flows):
        raise ValueError("Invalid flow as input")
    return markovify.Chain(flows, state_size)


def generate_flow(args: argparse.Namespace) -> None:
    pose_map = data.read_poses()

    flows = []
    if args.flows is not None:
        with open(args.flows, "r") as handle:
            string_flows = data.parse_flows(handle)
        actual_flows = data.pose_lookup(pose_map, string_flows)
        flows.extend(actual_flows)

    if not args.no_builtin_flows:
        builtin_flows = data.read_flows(pose_map)
        flows.extend(builtin_flows)

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


def console_entry() -> None:
    generate_flow(parse_args())


if __name__ == "__main__":
    console_entry()
