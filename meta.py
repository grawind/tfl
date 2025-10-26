import random
ALPHABET = "abc"

SIZE_ALPHABET = 3

RuleT = [
    ["cc", "aa"],
    ["aaa", "aa"],
    ["ababaabcba", "aaba"],
    ["aacb", "aa"],
    ["aabc", "aa"],
    ["aba", "a"],
    ["abc", "aa"],
    ["abba", "aca"],
    ["acb", "abb"],
    ["baa", "aa"],
    ["aaaba", "bb"],
    ["caa", "aa"],
    ["caca", "cba"],
    ["cbc", "c"]
]


RuleT2 = [
    ["cc", "aa"],
    ["aba", "a"],
    ["abc", "aa"],
    ["bba", "aca"],
    ["acb", "abb"],
    ["baa", "aa"],
    ["caa", "aa"],
    ["cbb", "cba"],
    ["cbc", "c"],
    ["bb", "aa"],
    ["ac", "aa"],
    ["abb", "aa"],
    ["cba", "aa"],
    ["aaa", "bb"]
]



SIZE_RuleT = 14



def randomString(n):
    s = ""
    for i in range(0, n):
        s += ALPHABET[random.randint(0, SIZE_ALPHABET-1)]
    return s

def randmSequenceRule(n):
    return [random.randint(0, SIZE_RuleT-1)  for i in range(0, n)]

def applyTheRule(s, rule, positions):
    return s[:positions] + s[positions:].replace(rule[0], rule[1], 1)

def find_overlaps(s, sub):
    positions = []
    i = 0
    while True:
        i = s.find(sub, i)
        if i == -1:
            break
        positions.append(i)
        i += 1
    return positions



def calculations_in_matrix_form(s):
    if s == "":
        return [[0, 0], [0, 0]]
    a = [[0, 0], [0, 0]]
    b = [[0, 1], [0, 0]]
    c = [[0, 0], [1, 0]]
    result = []
    if s[0] == "a":
        result = a
    elif s[0] == "b":
        result = b
    else:
        result = c
    for i in s[1:]:
        if i == "a":
            result = [[0, 0], [0, 0]]  # т. к. a = [[0, 0], [0, 0]], result*a=a
        elif i == "b":
            result = [
                [0, result[0][0]],
                [0, result[1][0]]] #т. к. b = [[0, 1], [0, 0]]
        else:
            result = [[result[0][1], 0],
                      [result[1][1], 0]] #т. к. c = [[0, 0], [1, 0]]
    return result


def multiplication_in_Z4(s):
    t = 1
    for i in s:
        if i == "b":
            t = t * 2
        else:
            t = 0
    t = t % 4
    return t


def test_invariant2(s0, s1):
    return multiplication_in_Z4(s0) == multiplication_in_Z4(s1)


def test_invariant(s0, s1):
    return calculations_in_matrix_form(s0) == calculations_in_matrix_form(s1)




fl = True
for j in range(0, 50000):
    ss = randomString(10)
    t = randmSequenceRule(20)
    s_0 = ss
    for i in t:
        pos = find_overlaps(ss, RuleT[i][0])
        k = len(pos)

        if k > 1:
            ss = applyTheRule(ss, RuleT[i], pos[random.randint(0, len(pos) - 1)])
        elif k == 1:
            ss = applyTheRule(ss, RuleT[i], pos[0])
    s_1 = ss

    if not test_invariant(s_0, s_1):
        print(s_0)
        print(s_1)
        fl = False

    if not test_invariant2(s_0, s_1):
        print(s_0)
        print(s_1)
        fl = False


if fl:
    print(True)



