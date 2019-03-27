def analysis(result, deck) -> int:
    count = 0
    for number in deck:
        if number in result:
            count += 1
    return count