
import pickle
from ways.graph import load_map_from_csv
import heapq
from betterWaze import  minAirDistance
import UC


def betterWaze(source, target,roads,abstractMap=None,isMain=0):
    'call function to find path using better ways algorithm, and return list of indices'
    centers = abstractMap.keys()
    pathAjunc1=UC.UC_faster(source,roads,centers,re_execute=1-isMain)
    junc1=pathAjunc1[0][0][1]
    junc1=abstractMap[junc1.index]
    junc2=minAirDistance(target,centers)
    dest = []
    dest.append(target.index)
    pathjunc2B=UC.UC_faster(roads[junc2],roads,dest,re_execute=1-isMain)
    dest2 = []
    dest2.append(junc2)
    pathjunc1junc2=UC.UC_faster(junc1,abstractMap,dest2,re_execute=1-isMain)

    if (isMain):
        if (pathAjunc1[0] and pathjunc2B[0] and pathjunc1junc2[0]):
            return pathAjunc1[0][0][2] + pathjunc1junc2[0][0][2] + pathjunc2B[0][0][2]
        else:
            pathSourceTarget = UC.UC_faster(source, roads, [target.index], re_execute=1 - isMain)
            return pathSourceTarget[0][0][2]
    else:

        if (pathAjunc1[0] and pathjunc2B[0] and pathjunc1junc2[0]):
            return [pathAjunc1[1] + pathjunc2B[1] + pathjunc1junc2[1],
                    pathAjunc1[0][0][0] + pathjunc2B[0][0][0] + pathjunc1junc2[0][0][0]]
        else:
            pathSourceTarget = UC.UC_faster(source, roads, [target.index],re_execute= 1 - isMain)
            print (len(abstractMap.keys()))
            return [pathSourceTarget[1] + pathAjunc1[1] + pathjunc2B[1] + pathjunc1junc2[1], pathSourceTarget[0][0][0]]




def openDataSet():
    datasetFile = open("dataSet.csv", 'r')
    dataSet = []
    for line in datasetFile:
        splitLine = line.split(',')
        dataSet.append([int(splitLine[0]), int(splitLine[1])])
    datasetFile.close()
    return dataSet

def base (src,dest,isMain=0):
    if isMain:
        roads = load_map_from_csv()
        ucResult=UC.UC_original_graph(roads[src],[dest],re_execute=1-isMain)
    else:
        ucResult=UC.UC_original_graph(src,[dest],re_execute=1-isMain)
    if (isMain):
        return ucResult[0][0][2]
    else:
        return ucResult[1],ucResult[0][0][0]

def betterWazeMain(source,target,abstractMap):
    roads=load_map_from_csv()
    return betterWaze(roads[source], roads[target],roads,abstractMap,isMain=1)




if __name__ == '__main__':
    roads=load_map_from_csv("tlv.csv")
    f=open("experiment.csv",'w')
    dataSet=openDataSet()
    abstractMap05 = pickle.load(open("abstract0.05.pkl",'rb'))
    abstractMap01=pickle.load(open("abstract0.01.pkl",'rb'))
    abstractMap005 = pickle.load(open("abstract0.005.pkl",'rb'))
    abstractMap0025 = pickle.load(open("abstract0.0025.pkl",'rb'))
    for x in dataSet:
        source=roads[int(x[0])]
        target=roads[int(x[1])]
        uniformcost=base(source,target.index)
        betterWaze1=betterWaze(source,target,roads,abstractMap05)
        betterWaze2= betterWaze(source, target, roads, abstractMap01)
        betterWaze3 = betterWaze(source, target, roads, abstractMap005)
        betterWaze4 = betterWaze(source, target, roads, abstractMap0025)
        f.write(str(x[0])+','+str(x[1])+','+str(uniformcost[0])+','+str(uniformcost[1])+','+str(betterWaze1[0])+','+str(betterWaze1[1])+','+str(betterWaze2[0])+','+str(betterWaze2[1])+','+str(betterWaze3[0])+','+str(betterWaze3[1])+','+str(betterWaze4[0])+','+str(betterWaze4[1])+'\n')
       # f.write(str(x[0]) + ',' + str(x[1]) + ',' + str(uniformcost[0]) + ',' + str(uniformcost[1]) + ',' + str(betterWaze4[0]) + ',' + str(betterWaze4[1])+'\n')
    f.close()
