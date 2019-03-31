def winNumCounter(results):
    t = dict()
    for r in results:
        for n in r:
            try:
                t[n] += 1
            except KeyError:
                t[n] = 1
    return t
