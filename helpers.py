def parse_multiplicity(mult: str) -> tuple[str, str]:
    if ".." in mult:
        low, high = mult.split("..", 1)
        return low, high
    return mult, mult