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

viewed_words = []

def DFS(s):
    if s == s_1:
        return True
    for rule in RuleT2:
        positions = find_overlaps(s, rule[0])
        if len(positions) > 0:
            for p in positions:
                s2 = applyTheRule(s, rule, p)
                if s2 not in viewed_words:
                    viewed_words.append(s2)
                    if s2 == s_1:
                        return True
                    if DFS(s2):
                        return True

    return False











fl = True
for j in range(0, 1000):
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

    viewed_words = []

    if not DFS(s_0):
        print(s_0, 1)
        print(s_1, 2)
        fl = False

if fl:
    print(True)



