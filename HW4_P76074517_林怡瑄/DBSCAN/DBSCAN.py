import numpy as np
import pandas as pd
import math
import scipy.spatial
import matplotlib.pyplot as plt

def readfile(path):
    dataset = []
    with open(path,'r') as f:
        for data in f.readlines():
            temp = data.split()
            dataset.append([float(temp[0]),float(temp[1]),0,0,2])
    dataset = pd.DataFrame(dataset,columns=["x","y","visited","cluster","type"]) # type 1 => noise ,2 => not core ,3=>core

    return dataset

def get_dis(n1,n2):
    return math.sqrt((n1[0]-n2[0])**2+(n1[1]-n2[1])**2)

def get_distable(dataset):
    size,_ = dataset.shape
    disTable = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(dataset.values, 'euclidean'))
    disTable = pd.DataFrame(disTable,columns=[ str(i) for i in range(size)])

    return disTable

def writeFile(pathr,pathw,label):
    with open(pathr,'r') as f:
        files = f.readlines()
    with open(pathw,'w') as f:
        for input,label in zip(files,label):
            if label==0:
                f.write(input[0:-1]+" noise"+"\n")
            else:
                f.write(input[0:-1] + " " + str(label) + "\n")

def DBSCAN(dataset, distable):
    size, _ = dataset.shape
    cluster_each_corePoint = {} # 紀錄corepoint index
    print("find core point...")
    for d_index in range(size):
        row = distable.iloc[d_index].values
        neighbors = np.where(row<=Epsilon)[0]

        # neighbors = distable.where(distable<Epsilon).iloc[d_index]
        # 掃DB
        if len(neighbors)>=MinumumPoints: # 是core point
            dataset.iloc[d_index, 4] = 3  # 標為core point
            cluster_each_corePoint[str(d_index)] = list(neighbors)

    print("cluster_each_corePoint")
    print(cluster_each_corePoint)

    # 對每一群  如果有overlap的點 則分為同一群
    cluster = {}
    cluster_index = 0
    print("conbine cluster...")
    for c1 in cluster_each_corePoint:
        # 找c1是已經在其他群內
        c1_cluster = 0
        for c in cluster:
            if int(c1) in cluster[c]:
                c1_cluster = int(c)

        # 判斷是否要新增新的群
        if c1_cluster == 0:  # 如果點不屬於任何一群 => 標為新的一群
            cluster_index += 1
            cluster[str(cluster_index)] = set(cluster_each_corePoint[c1])
            c1_cluster = cluster_index
        else:  # 如果點已經有分群 => 去那一群看是否還要合併
            cluster_index = c1_cluster

        for c2 in cluster_each_corePoint:

            intersection = cluster[str(cluster_index)] & set(cluster_each_corePoint[c2])

            if len(list(intersection)) > IntersectionNum:  # 兩群有交集 且數量大於特定的數量
                c2_cluster = 0
                for c in cluster:
                    if int(c2) in cluster[c]:
                        c2_cluster = int(c)

                # 如果c2是另一群內的core point => 合併兩群  並移除被合併的
                if c2_cluster != 0 and c2_cluster != c1_cluster:
                    cluster[str(cluster_index)] = cluster[str(cluster_index)] | cluster[str(c2_cluster)]
                    del cluster[str(c2_cluster)]
                else:  # c2還沒被分群 或在c1群內
                    cluster[str(cluster_index)] = cluster[str(cluster_index)]|set(cluster_each_corePoint[c2])

    # label list
    labelList = [0 for i in range(size)]
    c_index = 1
    c_dic = {}
    for c in cluster:
        for point in list(cluster[c]):
            if c not in c_dic.keys():
                c_dic[str(c)] = c_index
                c_index+=1
            labelList[int(point)] = c_dic[str(c)]
    dataset["cluster"] = np.array(labelList)

    return dataset

# 參數設定
Epsilon = 5.5
MinumumPoints = 14
IntersectionNum = 22

finename = "Clustering_test5"

# get data
dataset = readfile("data/"+finename)
print("~~~~~~~~~~~~dataset~~~~~~~~~~~")
print(dataset)

# get distable
print("...get dis table...")
distable = get_distable(dataset)

# dbscan
print("...start dbscan...")
dataset = DBSCAN(dataset,distable)

# 寫檔
writeFile("data/"+finename,finename+"_output.txt",list(dataset["cluster"]))

# 畫分群圖
color = ['g','r','c','m','y','k']
cvalue = []
for i in dataset['cluster']:
    if i == 0:
        cvalue.append("b")
    else:
        index = i % 6
        cvalue.append(color[int(index)])

plt.scatter(list(dataset['x']),list(dataset['y']),c = cvalue)
plt.savefig(finename+".png")
plt.show()