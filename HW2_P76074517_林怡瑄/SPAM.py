from bitarray import bitarray
import copy


def intputFile():
    with open("seqdata.dat.txt") as file:
        seqDataset = {}
        seq_size = []
        item_1_set = []
        for f in file.readlines():

            s = f.split()
            key = tuple([int(s[0])])
            seqDataset[key] = []
            seq = []
            for i in range(2, len(s), 2):
                seq.append([s[i - 1], s[i]])
                if tuple([int(s[i])]) not in item_1_set:
                    item_1_set.append(tuple([int(s[i])]))

            item_1_set = sorted(item_1_set, key=lambda x: x[0])
            seq_sort = sorted(seq, key=lambda x: x[0])

            for i in range(len(seq_sort)):
                if i > 0 and seq_sort[i][0] == seq_sort[i - 1][0]:
                    seqDataset[key][-1].append(int(seq_sort[i][1]))
                    continue
                seqDataset[key].append([int(seq_sort[i][1])])
            seq_size.append(len(seqDataset[key]))

    return seqDataset, seq_size, item_1_set

def writefile(bitmap):
    with open("output.txt",'w') as f:
        for i in bitmap:
            f.write(str(i) + "  SUP:"+str(spam.getCount(bitmap[i])) +"\n")

class SPAM():
    def __init__(self, seqDataset, seq_size, item_1_set):
        self.seqDataset = seqDataset
        self.seq_size = seq_size
        self.t_num = sum(seq_size)
        self.item_1_set = item_1_set
        self.bitmap = self.getBitmap()

        self.FreItemSet_1 = self.getFreItemSet_1()

    # 對所有交易與長度為1的item建bitmap
    def getBitmap(self):
        bitmap = {}
        for i in self.item_1_set:
            a = bitarray(self.t_num)
            a.setall(False)
            bitmap[i] = a

        index = 0
        for seqData in seqDataset:
            for item_list in seqDataset[seqData]:
                for item in item_list:
                    # print(index)
                    # print(item)
                    # os.system("pause")
                    bitmap[tuple([item])][index] = True
                index += 1
        print("get bitmap ! ")
        # print(bitmap)
        return bitmap

    # 刪掉長度為1的item小於minsupport者
    def getFreItemSet_1(self):
        itemset = []
        dellist = []
        for i in self.bitmap:
            c = self.getCount(self.bitmap[i])
            if c >= min_support:
                itemset.append(i)
            else : # 從bitmap刪掉
                dellist.append(i)

        for i in dellist:
            del self.bitmap[i]
        print("FreItemSet_1 : ")
        print(itemset)
        return itemset

    # 計算出現幾次
    def getCount(self, bitArray):
        index = 0
        count = 0

        for j in self.seq_size:  # 對每筆C_ID的紀錄
            findFirst = 0
            for k in range(j):  # 看該C_ID有幾筆交易T_ID
                if(bitArray[index] == 1 and findFirst == 0):  # 找到1後
                    count+=1
                    findFirst = 1
                index+=1
        return count
    # 取得intput的mask
    def getMask(self, bitArray):
        mask = copy.copy(bitArray)
        index = 0

        for j in self.seq_size:  # 對每筆C_ID的紀錄
            findFirst = 0
            for k in range(j): # 看該C_ID有幾筆交易T_ID
                if (findFirst == 0):  # 還沒找到第一個1
                    if (bitArray[index] == 1):  # 找到1
                        findFirst = 1
                        mask[index] = 0
                elif (findFirst == 1):  # 已找到第一個1後其餘bit改成1
                    mask[index] = 1
                index += 1

        return mask

    def getNewNode_S(self, a, b):
        c = list(a)
        c.extend(list(b))
        return tuple(c)

    def getNewNode_I(self, a, b):
        c = list(a)
        if (type(c[-1]) == int):
            c[-1] = [c[-1]]
            c[-1].extend(list(b))
            c[-1] = tuple(c[-1])
        else:
            c[-1] = list(c[-1])
            c[-1].extend(list(b))
            c[-1] = tuple(c[-1])

        return tuple(c)

    def dfs_pruning(self, node, Sn, In):

        # print("node S")
        # print(node)
        Stemp = []  # 下一層後面可能接的
        Itemp = []  # 下一層後面可能接的

        S_Ntemp = []  # 這一層全部產生的的S SPAM node
        I_Ntemp = []

        # ~~~~S_SPAM~~~~
        for i in Sn:  # 對每個Node去 往後串聯有可能的成為frequence itemset的item
            # 如果node連接上i > min_support
            mask = self.getMask(self.bitmap[node])
            # print(self.bitmap[node])
            ba = mask & self.bitmap[i]
            # print(mask)
            # print(self.bitmap[i])
            c = self.getCount(ba)
            if c >= min_support:
                n = self.getNewNode_S(node, i)
                S_Ntemp.append(n)
                self.bitmap[n] = ba  # 紀錄新node的bitmap
                Stemp.append(i)

        for n in range(len(S_Ntemp)):
            self.dfs_pruning(S_Ntemp[n], Stemp, Stemp[n + 1:])

        # ~~~~~I_SPAM~~~~~
        for i in In:  # 對每個Node去 往後串聯有可能的成為frequence itemset的item
            ba = self.bitmap[node] & self.bitmap[i]
            c = self.getCount(ba)
            if c >= min_support:
                n = self.getNewNode_I(node, i)
                I_Ntemp.append(n)
                self.bitmap[n] = ba  # 紀錄新node的bitmap
                Itemp.append(i)

        for n in range(len(I_Ntemp)):
            self.dfs_pruning(I_Ntemp[n], Stemp, Itemp[n + 1:])

        # print("SN:")
        # print(S_Ntemp)
        # print("IN")
        # print(I_Ntemp)


min_support =  int(input("請輸入minSupport  ex 100 : "))

# 資料前處理
seqDataset, seq_size, item_1_set = intputFile()
print("seqDataset : ")  # 每個customer買的緒列資料
print(seqDataset)
print("seq_size :")  # 每個緒列資料內有幾個item
print(seq_size)
print("item_1_set :")  # 所有長度為1的item
print(item_1_set)

# 宣告spam物件
spam = SPAM(seqDataset, seq_size, item_1_set)


# 遞迴求所有的swquence pattern
for n in range(len(spam.FreItemSet_1)):
    spam.dfs_pruning(spam.FreItemSet_1[n], spam.FreItemSet_1, spam.FreItemSet_1[n + 1:])

# 在掃一次min support
print("~~~~~~~~~~~~~~ALL swquence pattern ~~~~~~~~~~~~~~~~")
print(spam.bitmap.keys())
writefile(spam.bitmap)
