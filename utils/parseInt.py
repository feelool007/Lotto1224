def parseInt(string: str) -> int:
    numberStr = "".join([s for s in string if s.isdigit()])
    if len(numberStr) == 0:
        return 0
    else:
        return int(numberStr)