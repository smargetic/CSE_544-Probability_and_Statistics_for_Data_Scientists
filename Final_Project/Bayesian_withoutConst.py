import csv
import numpy as np
import datetime
import math
from scipy import integrate
import matplotlib.pyplot as plt
from scipy.stats import expon
import copy
from scipy.stats import gamma


def oilData(Date, Crude_Oil, Deaths):
    #days, oil, deaths
    data = [None]*len(Date)
    deaths = [None]*len(Deaths)

    #get sum of deaths
    deaths[0]=Deaths[0]
    for i in range(1,len(Date)):
        deaths[i] = Deaths[i]+deaths[i-1]

    count = 0
    #array of dictionaries with data
    for i in range(0,len(Date)):
        if(deaths[i]!=0):
            dic = {"date" : Date[i], "oil" : Crude_Oil[i], "deaths" : deaths[i]}
            data[count] = dic
            count = count +1
    for m in range(0, (len(Date)-count)):
        data.pop()

    return data
#read week 1,2,3,4 data
def getWeeks(data):
    #get data

    dataNew = copy.deepcopy(data)
    for i in range(1,len(data)):
        dataNew[i]["deaths"] = int(data[i]["deaths"])-int(data[i-1]["deaths"])
    data=copy.deepcopy(dataNew)
    
    #I get the 4 seperate weeks of data
    weeks = [[None] for j in range(0,4)]

    dateLoc = 0
    for i in range(0,4):
        tempDate = data[dateLoc]["date"].split("/")

        timeStart = datetime.date(int(tempDate[2]), int(tempDate[0]), int(tempDate[1]))
        timeEnd = timeStart + datetime.timedelta(7)

        firstFound =0
        #I get the dates between those ranges
        for j in range(dateLoc,len(data)):
            tempDateStr = data[j]["date"].split("/")
            tempDate = datetime.date(int(tempDateStr[2]), int(tempDateStr[0]), int(tempDateStr[1]))

            if(tempDate<timeEnd):
                if(firstFound==0):
                    weeks[i][0] = data[j]
                    firstFound = 1
                else:
                    weeks[i].append(data[j])
            else:
                dateLoc = j
                break
    
    return weeks

def MMEMean(weeks):
    n = len(weeks[0])
    sum = 0

    for i in range(0,n):
        sum = sum + int(weeks[0][i]["deaths"])
    
    # print(weeks[1])
    MMEmean = (1/n)*sum

    return MMEmean

def likelihood(mean, type, n):
    if(type == "exp"):
        temp = mean**n
        sum = 0 

def factorial(x):
    prod = 1
    for i in range(1,x):
        prod = prod*x
    return prod


# def integrandExp(x,lambdA,likelihoodPois):
#     return (lambdA*np.exp(-lambdA*x)*likelihoodPois)

# def integrandPoisson(x, prod, likeliAll, lambdA):
#     return (prod*likeliAll*lambdA*np.exp((-lambdA)*x))

def baysian(weeks):
    # bigConstArray = [None]*4
    # const = [None]*len(weeks[0])
    sumD1 =0
    sumArray = [None]*4
    lengthArray = [None]*4

    mean = MMEMean(weeks)
    print(mean)
    x = np.linspace(0, 5, 175)


    # prod=1

    #calculate the sum associated with it
    for m in range(0, len(weeks[0])):
        dataPoint = int(weeks[0][m]["deaths"])
        sumD1 = sumD1 + dataPoint
        # const[m] = 1/factorial(dataPoint)
        # prod = (const[m])*np.exp(-x)*((x)**dataPoint)*prod
    sumArray[0] = sumD1
    lengthArray[0] = len(weeks[0])


    #get alpha and beta
    alpha = sumD1 +1
    beta = (1/mean) + len(weeks[0])
    myScale = 1/beta

    #graph data
    gamma.pdf(x,alpha, scale = myScale )
    labelName = "Data 1" 
    plt.plot(x, gamma.pdf(x,alpha, scale = myScale ), label = labelName)

    #get map
    mapVal = sumD1/(len(weeks[0])+ (1/beta))
    print(labelName + " MAP Value : " +str(mapVal)) 

    for i in range(1,len(weeks)):
        sum =0
        for m in range(0, len(weeks[i])):
            sum = int(weeks[0][m]["deaths"]) + sum
        lengthArray[i] = lengthArray[i-1]+ len(weeks[i])
        sumArray[i] = sumArray[i-1] + sum

        #alpha and beta for gamma distr
        alpha = sumArray[i] +1
        beta = lengthArray[i] + (1/mean)

        myScale = 1/beta
        labelName = "Data " + str(i+1)

        plt.plot(x, gamma.pdf(x,alpha, scale = myScale ), label = labelName)

        mapVal = sumD1/(len(weeks[0])+ (1/beta))
        print(labelName + " MAP Value : " +str(mapVal)) 
    
    plt.title('Bayesian Inference for Deaths Per Day')
    plt.xlabel('Deaths Per Day')
    plt.ylabel('Values')
    plt.legend()

    plt.show()    
# def baysian2(weeks):
#     mean = MMEMean(weeks)
#     x = np.linspace(0, 40, 100)
#     bigConstArray = [None]*4
#     sumD1 =0

#     # prod = [None]*len(x)
#     prod=1
#     const = [None]*len(weeks[0])
#     for m in range(0, len(weeks[0])):
#         dataPoint = int(weeks[0][m]["deaths"])
#         sumD1 = sumD1 + dataPoint
#         const[m] = 1/factorial(dataPoint)
#         # prod[m] = (const[m])*np.exp(-x)*((x)**int(weeks[0][m]["deaths"]))
#         prod = (const[m])*np.exp(-x)*((x)**dataPoint)*prod

#     bigConst = 1/mean
#     for i in range(0,len(weeks[0])):
#         bigConst = bigConst*const[i]
#     bigConstArray[0] = bigConst


#     post = prod*(1/mean)*np.exp(-(1/mean)*x)

#     labelName = "Data 1" 
#     plt.plot(x,post, label = labelName)
#     for i in range(1,4):
#         prod = 1
#         # const = [None]*len(weeks[i])
#         for m in range(0,len(weeks[i])):
#             dataPoint = weeks[i][m]["deaths"]
#             #prod = np.exp(-dataPoint)*((dataPoint)**sumD1)*np.exp(-(mean)*dataPoint)
#             prod = np.exp(-dataPoint)*((dataPoint)**sumD1)*np.exp(-(1/mean)*dataPoint)
#         bigConstArray[i] = prod*(bigConstArray[i-1]**2)

#         post = prod*np.exp(-x)*((x)**sumD1)*np.exp(-(1/mean)*x)*(bigConstArray[i-1]**2)
#         #post = prod*np.exp(-x)*((x)**sumD1)*np.exp(-(mean)*x)*(bigConstArray[i-1]**2)

#         labelName = "Data " + str(i+1)
#         plt.plot(x,post, label = labelName)

#             # prod[m] = 
#             # const[m] = 1/factorial(int(weeks[0][m]["deaths"]))
#             # prod[m] = (const[m])*np.exp(-x)*((x)**int(weeks[0][m]["deaths"]))
        
#     plt.show()


# def baysian(weeks):
#     postArray = [None]*4
#     constArray = [None]*4
#     likeliArray = [None]*4

#     # x = np.linspace(expon.ppf(0.01), expon.ppf(0.99), 100)
#     x = np.linspace(0,40, 100)
#     lambdA = MMEMean(weeks)

#     #I calculate the pdf of the exp --> assuming continuous
#     pdfExp = [None]*len(x)
#     for i in range(0, len(x)):
#         pdfExp[i] = lambdA*np.exp(-lambdA*x[i])


    
#     #likelihood of first --> poisson
#     for j in range(len(weeks[0])):
#         prod = (1/(factorial(int(weeks[0][j]["deaths"]))))*(lambdA**int(weeks[0][j]["deaths"]))*(np.exp(-int(weeks[0][j]["deaths"])))
#     likelihoodPois = np.exp(-lambdA)*prod
#     print("likelihoodPois")
#     print(likelihoodPois)
#     likeliArray[0] = likelihoodPois


#     post = [None]*len(x)
#     for j in range(0, len(x)):
#         post[j] = (likelihoodPois*pdfExp[j])

#     #plot it
#     plt.plot(x, post)
#     postArray[0] = post

#     print(post)
#     # print(post)
#     for i in range(0,3):
#         likeliAll = 1
#         for m in range(0, len(likeliArray)):
#             if(likeliArray[m]!=None):
#                 likeliAll = likeliArray[m]*likeliAll
#         #likelihood
#         prod = 1
#         for m in range(0,len(weeks[i+1])):
#             prod = likeliAll*lambdA*np.exp((-lambdA)*float(weeks[i+1][m]["deaths"]))
        
#         # print("likeli")
#         # print(prod)
#         # print("\n")
 
#         likeliArray[i+1] = prod

#         post2= [None]*len(x)
#         #post pdf
#         for m in range(0,len(x)):
#             post2[m] = prod*likeliAll*lambdA*np.exp((-lambdA)*x[m])
#         #postArray[i+1] = prod*likeliAll*lambdA*np.exp((-lambdA)*(x))
#         postArray[i+1] = post2
#         print(postArray[i+1])

#         plt.plot(x,postArray[i+1])

#     # print("post array")
#     # print(postArray)
#     for i in range(0,len(postArray)):
#         print("MAP value: " + str(postArray[i][np.argmax(postArray[i])]))
#     plt.show()

# weeks = readData()
# print(MMEMean(weeks))
# print("bsdflsd")
# print(weeks[0])
# print(len(weeks[0]))
# print("\n")
# print(weeks[1])
# print(len(weeks[1]))
# print("\n")
# print(weeks[2])
# print(len(weeks[2]))
# print("\n")
# print(weeks[3])
# print(len(weeks[3]))
# baysian(weeks)

oil = [55.51, 54.09, 53.09, 53.33, 53.29, 52.19, 51.58, 50.06, 49.59, 50.87, 50.94, 50.34, 49.59, 50.0, 51.13, 51.41, 52.03, 52.1, 53.31, 53.77, 53.36, 51.36, 49.78, 48.67, 47.17, 44.83, 46.78, 47.27, 46.78, 45.9, 41.14, 31.05, 34.47, 33.13, 31.56, 31.72, 28.96, 26.96, 20.48, 25.09, 19.48, 23.33, 21.03, 20.75, 16.6, 15.48, 14.1, 20.51, 20.28, 25.18, 28.36, 26.21, 23.54, 24.97, 22.9, 22.36, 19.82, 18.31, 13.64, 15.06, 15.99, 12.17]
dates = ['1/23/2020', '1/24/2020', '1/27/2020', '1/28/2020', '1/29/2020', '1/30/2020', '1/31/2020', '2/3/2020', '2/4/2020', '2/5/2020', '2/6/2020', '2/7/2020', '2/10/2020', '2/11/2020', '2/12/2020', '2/13/2020', '2/14/2020', '2/18/2020', '2/19/2020', '2/20/2020', '2/21/2020', '2/24/2020', '2/25/2020', '2/26/2020', '2/27/2020', '2/28/2020', '3/2/2020', '3/3/2020', '3/4/2020', '3/5/2020', '3/6/2020', '3/9/2020', '3/10/2020', '3/11/2020', '3/12/2020', '3/13/2020', '3/16/2020', '3/17/2020', '3/18/2020', '3/19/2020', '3/20/2020', '3/23/2020', '3/24/2020', '3/25/2020', '3/26/2020', '3/27/2020', '3/30/2020', '3/31/2020', '4/1/2020', '4/2/2020', '4/3/2020', '4/6/2020', '4/7/2020', '4/8/2020', '4/9/2020', '4/13/2020', '4/16/2020', '4/17/2020', '4/22/2020', '4/23/2020', '4/24/2020', '4/27/2020']
deaths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 2, 0, 3, 4, 5, 6, 6, 7, 23, 25, 41, 46, 61, 115, 181, 258, 286, 373, 581, 843, 930, 1111, 1169, 1304, 1999, 1846, 1870, 1551, 2141, 2188, 2179, 2016, 1992, 1355]

data = oilData(dates, oil, deaths)
weeks = getWeeks(data)
baysian(weeks)

# baysian2(weeks)

    # bigConst = 1/mean
    # for i in range(0,len(weeks[0])):
    #     bigConst = bigConst*const[i]
    # bigConstArray[0] = bigConst


    # post = prod*(1/mean)*np.exp(-(1/mean)*x)