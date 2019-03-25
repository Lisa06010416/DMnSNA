import re
import copy
def inputfile(path):
    dataset = []
    with open(path,"r") as f:
        for i in f.readlines():
            data = re.split(r"{|}|,| ",i)
            temp = {}
            has_memcard = 0
            has_child = 0
            has_marital_status = 0
            has_age = 0
            has_income = 0
            for i in range(1,len(data),2):
                if data[i]=="0":
                    temp["marital_status"] = data[i+1]
                    has_marital_status = 1
                elif data[i]=="1":
                    temp["num_children_at_home"] = int(data[i+1])
                    has_child =1
                elif data[i] == "2":
                    temp["member_card"] = data[i + 1]
                    has_memcard = 1
                elif data[i] == "3":
                    temp["age"] = int(data[i + 1])
                    has_age = 1
                elif data[i]=="4":
                    temp["year_income"] = int(data[i+1])
                    has_income=1
            if(has_memcard==0):
                temp["member_card"] = "Basic"
            if(has_child==0):
                temp["num_children_at_home"] = 0
            if(has_marital_status==0):
                temp["marital_status"] = "S"
            if(has_age==0):
                temp["age"]=="N"
            if(has_income==0):
                temp["year_income"] = "N"

            dataset.append(temp)
    return dataset

def writeFile(predict, r_path, w_path):

    with open(r_path,'r') as f:
            test = f.readlines()

    with open(w_path,'w') as f:
        for i in range(len(test)):
            f.write(test[i][:-2]+" member_card = "+predict[i]+"\n")


def preprocess(dataset):
    pre_dataset = []
    attributeTable={"marital_status":[],"num_children_at_home":[],"member_card":[],"age":[],"year_income":[]}
    for data in dataset:
        t = {}
        for k in data:
            if k not in attributeTable.keys():
                attributeTable[k] = []

            d = ""
            if k == "marital_status":
                d=data[k]
            elif k == "num_children_at_home":
                if data[k] == 0:
                    d = "0"
                elif data[k]==1:
                    d = "1"
                elif data[k]==2:
                    d="2"
                elif data[k]==3:
                    d="3"
                elif data[k]==4:
                    d="4"
                else:
                    d="5"
            elif k == "member_card":
                d = data[k]
            elif k == "age":
                if data[k]=="N":
                    d="0"
                elif data[k] >= 0 and data[k] < 30:
                    d="1"
                elif data[k]>=30 and data[k] <40:
                    d="2"
                elif data[k]>=40 and data[k] <50:
                    d="3"
                elif data[k]>=50 and data[k] <60:
                    d="4"
                else:
                    d="5"
            elif k =="year_income":
                if data[k]=="N":
                    d="0"
                elif data[k] >= 0 and data[k] < 40000:
                    d="1"
                elif data[k]>=40000 and data[k] <80000:
                    d="2"
                elif data[k]>=80000 and data[k] <120000:
                    d="3"
                elif data[k]>=120000 and data[k] <140000:
                    d="4"
                else:
                    d="5"
                # d = str(data[k])

            if d not in attributeTable[k]:
                attributeTable[k].append(d)

            t[k] = d
        pre_dataset.append(t)

    return pre_dataset,attributeTable

class NaiveBayes():
    def __init__(self,dataset, attributeTable):
        self.dataset = dataset
        self.attributeTable = attributeTable
        self.countTable = self.get_countTable()
        self.likelihoodTable = self.get_likelihoodTable()

    def get_countTable(self):
        # build counttable
        ct = {}
        for at in self.attributeTable:
            if at == "member_card":
                continue
            ct[at]={}
            for ca in self.attributeTable[at]:
                ct[at][ca] = {}
                ct[at][ca]["total"] = 0
                for la in self.attributeTable['member_card']:
                    ct[at][ca][la] = 0

        # count
        for data in self.dataset:
            for at in data:
                if at == "member_card":
                    continue
                ct[at][data[at]][data["member_card"]] += 1
                ct[at][data[at]]["total"] +=1
        print("countTable :")
        print(ct)
        return ct

    def get_likelihoodTable(self):
        lt = copy.copy(self.countTable)

        count = {"Basic":0,"Normal":0,"Silver":0,"Gold":0}
        countALL = len(self.dataset)
        for data in self.dataset:
            if data["member_card"] == "Basic":
                count["Basic"]+=1
            elif data["member_card"] == "Normal":
                count["Normal"]+=1
            elif data["member_card"] == "Silver":
                count["Silver"]+=1
            elif data["member_card"] == "Gold":
                count["Gold"]+=1

        for at in self.countTable:
            for ca in self.countTable[at]:
                for la in self.countTable[at][ca]:
                    if la == "total":
                        lt[at][ca][la] /= countALL
                    else:
                        lt[at][ca][la] /= count[la]
        print("likelihoodTable : ")
        print(lt)
        return lt

    def predict(self, testDataset):
        answerP = []


        for data in testDataset:
            ans_pro = {"Basic": 1, "Normal": 1, "Silver": 1, "Gold": 1}

            for la in self.attributeTable["member_card"]:
                for at in data:

                    if at == "member_card" :
                        continue
                    ans_pro[la]+=self.likelihoodTable[at][data[at]][la]

            answerP.append(ans_pro)
        answer = []
        for i in answerP:
            maxLabel = ""
            max = -1
            for j in i:
                if i[j]>max:
                    max = i[j]
                    maxLabel = j
            answer.append(maxLabel)
        print("predic : ")
        print(answer)
        return  answer

trainPath = "training.txt"
testPath = "test.txt"
writePath = "output.txt"

dataset = inputfile(trainPath)
dataset, attributeTable = preprocess(dataset)
print("attributeTable :")
print(attributeTable)
print("dataset :")
print(dataset)
nb = NaiveBayes(dataset, attributeTable)

test = inputfile(testPath)
test, attributeTable = preprocess(test)
print("test dataset : ")
print(test)
predic = nb.predict(test)
writeFile(predic,testPath,writePath)


