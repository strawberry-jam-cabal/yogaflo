from yogaflo.__main__ import parse_args, generate_flow


def test_entry() -> None:
    generate_flow(parse_args(""))
