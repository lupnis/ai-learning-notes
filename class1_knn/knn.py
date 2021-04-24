# copyright Lupnis <lupnis@outlook.com> in RiverENC 2021
# this is my first program using python:P
import math
import pandas as pd

CSV_PATH='./iris.csv'# you can change the paths as you like
TEST_PATH='./iris-test.csv'# the same as the above comment:)

def findidx(arr, item):
    if item not in arr:
        return -1
    else:
        for i in range(len(arr)):
            if(arr[i] == item):
                return i

classificationMap=[] # record the classifications of iris
dataMap=[] # [classification][[s-l,s-w,p-l,p-w],[s-l,s-w,p-l,p-w],...]
dataColor=[] # colors just make the process more interesting, no use indeed:P
testList=[] # test datas

dataStream=pd.read_csv(CSV_PATH)

coloridx=32
for singleData in dataStream.iterrows():
    '''
    print('dix:',singleData[0],
    '  s-l=',singleData[1][0],', s-w=',singleData[1][1],
    ', p-l=',singleData[1][2],', p-w=',singleData[1][3],
    '  clf=\x1B[34m',singleData[1][4],'\x1B[0m ',end="")
    '''
    if singleData[1][4] not in classificationMap:
        #print("\x1B[32m Vacant.\x1B[0m")
        classificationMap.append(singleData[1][4])
        dataColor.append(str('\x1B['+str(coloridx)+'m'))
        coloridx=coloridx+1
        dataMap.append([[singleData[1][0],singleData[1][1],singleData[1][2],singleData[1][3]]])
    else:
        #print("\x1B[31m Occupied.\x1B[0m")
        idx=findidx(classificationMap,singleData[1][4])
        dataMap[idx].append([singleData[1][0],singleData[1][1],singleData[1][2],singleData[1][3]])

################

testStream=pd.read_csv(TEST_PATH)

for singleData in testStream.iterrows():
    testList.append([singleData[1][0],singleData[1][1],singleData[1][2],singleData[1][3]])

disSets=[] # [idisset]

for i in range(len(classificationMap)):
    tempDisSet=[]
    for j in range(len(testList)): 
        for k in range(len(dataMap[i])):
            disSL=math.pow(testList[j][0]-dataMap[i][k][0],2)
            disSW=math.pow(testList[j][1]-dataMap[i][k][1],2)
            disPL=math.pow(testList[j][2]-dataMap[i][k][2],2)
            disPW=math.pow(testList[j][3]-dataMap[i][k][3],2)
            dis=math.sqrt(disSL+disSW+disPL+disPW)
            tempDisSet.append(dis)
    disSets.append(tempDisSet)

newDisSets=[]
k=20
for i in range(len(classificationMap)):
    tempNewDisSet=[]
    tmpK=k
    for j in range(int((len(disSets[i]))/(len(dataMap[i])))):
        tempNewDisSet.append(disSets[i][tmpK:tmpK+len(dataMap[i])])
        tmpK=tmpK+len(dataMap[i])
    newDisSets.append(tempNewDisSet)

disSets=newDisSets

sumSets=[]
for i in range(len(classificationMap)):
    tempSumSet=[]
    for j in range(len(disSets[i])):
        disSets[i][j].sort()
        del disSets[i][j][len(testList):len(disSets[i][j])]
        tempSumSet.append(sum(disSets[i][j]))
    sumSets.append(tempSumSet)

for i in range(len(testList)):
    min=2147483647
    minidx=0
    for j in range(len(classificationMap)):
        if(sumSets[j][i]<=min):
            min=sumSets[j][i]
            minidx=j
    testList[i].append(dataColor[minidx]+classificationMap[minidx])

for i in range(len(testList)):
    print('test[',i,'],result=',testList[i][4],'\x1B[0m')
