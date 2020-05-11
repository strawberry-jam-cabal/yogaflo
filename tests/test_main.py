from yogaflo.__main__ import parse_args, generate_flow

import random


def test_entry() -> None:
    random.seed(666)
    generate_flow(parse_args(""))
