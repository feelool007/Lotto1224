def oddAndEven(deck: list) -> str:
    countsOdd = 0
    countsEvent = 0
    for d in deck:
        if int(d) % 2 == 0:
            countsEvent += 1
        else:
            countsOdd += 1

    return "%s單%s雙" %(countsOdd, countsEvent)
