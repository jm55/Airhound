def find_iterations(charset:str, min:int, max:int):
    iterations = 0
    if min == max:
        return pow(len(charset),min)
    while min <= max:
        iterations += pow(len(charset),min)
        min += 1    
    return iterations

tests = [
            ["abc", "1", "3"],
            ["abc", "3", "3"]
        ]

for t in tests:
    print(t[0], t[1], t[2], find_iterations(t[0], int(t[1]), int(t[2])))