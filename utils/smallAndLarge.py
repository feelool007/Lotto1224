from typing import List

def smallAndLarge(deck: List[str]) -> str:
    countsSmall = 0
    countsLarge = 0
    for d in deck:
        if int(d) <= 12:
            countsSmall += 1
        else:
            countsLarge += 1

    return "%s小%s大" %(countsSmall, countsLarge)