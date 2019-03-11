import copy
import numpy as np


def inputFile(path):
    datas = []
    maxIndex = 0
    with open(path, 'r') as files:
        for f in files.readlines():
            data = []
            for item in f.split():
                data.append(int(item))
                if int(item) > maxIndex:
                    maxIndex = int(item)
            datas.append(data)
    return datas, maxIndex


def getFrequenceItemSet(candicate, countTable):
    FI = []
    for c in candicate:
        try:
            if float(countTable[c]) / float(dataNum) > minSupport:
                FI.append(c)
        except:
            continue
    return FI


def count(dataset, itemset):
    for i in dataset:
        for j in itemset:
            if set(i) >= set(j):
                if j not in countTable:
                    countTable[j] = 1
                else:
                    countTable[j] += 1
    # print("123")
    # print (countTable)
    return countTable


def getCandicate_1(dataset):
    candidate = []
    for i in dataset:
        for j in i:
            candidate.append(frozenset([j]))
    candidate = list(set(candidate))
    return candidate


def getCandidate(itemSet):
    candidate = []
    l = len(itemSet[0])

    for i in itemSet:
        for j in itemSet:
            c = list(set(copy.copy(list(i)) + copy.copy(list(j))))
            # print(c)
            c.sort()
            if len(c) == l + 1:
                candidate.append(frozenset(c))
    return list(set(candidate))


def get_strongRules(FI, subSet, countTable):
    strongRule = []

    for item in FI:
        for subItem in [x for i in subSet for x in i]:
            if set(item) > set(subItem):
                confidence = (countTable[item]) / (countTable[subItem])
                # print(confidence)
                if confidence >= minConfidence:
                    strongRule.append([subItem, item - subItem, confidence])

    return strongRule



# 使用者輸入
minSupport = float(input("請輸入minSupport  ex 0.2 : "))
minConfidence = float(input("請輸入minConfidence  ex 0.2 : "))

# 讀取檔案
dataset, maxIndex = inputFile('input.txt')
dataNum = len(dataset)

# 找出長度為1的candidate
candidate_1 = getCandicate_1(dataset)

frequenceItemset = []
countTable = {}  # 紀錄candidate出現的數量

# 計算每一個candidate出現的數量
count(dataset, candidate_1)
# 找出符合minsupport的candidate
FI = getFrequenceItemSet(candidate_1, countTable)
frequenceItemset.append(copy.copy(FI))


strongRule = [] # 紀錄找到的關聯規則

# 迴圈處理長度為2開始遞增的candicate
# 直到找到的集合為空
while (True):
    # 找出可能的candidate
    candicate_K = getCandidate(FI)
    if (len(candicate_K) == 0):
        break
    print("C")
    print(candicate_K)

    # 計算每一個candidate出現的數量
    countTable = count(dataset, candicate_K)
    print(countTable)

    # 找出符合minsupport的candidate
    FI = getFrequenceItemSet(candicate_K, countTable)
    if (len(FI) == 0):
        break
    frequenceItemset.append(copy.copy(FI))
    print("FI")
    print(FI)

    # 找出strongRule
    sr = get_strongRules(FI, frequenceItemset[:-1], countTable)
    strongRule.append(sr)

print("frequenceItemset :")
print(frequenceItemset)
print("countTables :")
print(countTable)

print("strong rule")
with open('output.txt','w') as file:
    for i in strongRule:
        for j in i:
            file.write(str(list(j[0]))+" => "+str(list(j[1]))+"     "+str(j[2])+"\n")
            print(j)
