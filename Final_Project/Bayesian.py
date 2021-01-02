import csv
import numpy as np
import datetime
import math
from scipy import integrate
import matplotlib.pyplot as plt
from scipy.stats import expon
import copy

#read week 1,2,3,4 data
# def readData():
#     #get data
#     with open('cleaned_OilVsDeaths_without0.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         data = list(reader)

#     # data[0]["deaths"] = int(data[0]["deaths"])
#     dataNew = copy.deepcopy(data)
#     for i in range(1,len(data)):
#         dataNew[i]["deaths"] = int(data[i]["deaths"])-int(data[i-1]["deaths"])
#     data=copy.deepcopy(dataNew)

#     #I get the 4 seperate weeks of data
#     weeks = [[None] for j in range(0,4)]

#     dateLoc = 0
#     for i in range(0,4):
#         tempDate = data[dateLoc]["date"].split("/")

#         timeStart = datetime.date(int(tempDate[2]), int(tempDate[0]), int(tempDate[1]))
#         timeEnd = timeStart + datetime.timedelta(7)

#         firstFound =0
#         #I get the dates between those ranges
#         for j in range(dateLoc,len(data)):
#             tempDateStr = data[j]["date"].split("/")
#             tempDate = datetime.date(int(tempDateStr[2]), int(tempDateStr[0]), int(tempDateStr[1]))

#             if(tempDate<timeEnd):
#                 if(firstFound==0):
#                     weeks[i][0] = data[j]
#                     firstFound = 1
#                 else:
#                     weeks[i].append(data[j])
#             else:
#                 dateLoc = j
#                 break
#     return weeks
def oilData(Date, Crude_Oil, Deaths):
    #days, oil, deaths
    data = [None]*len(Date)
    deaths = [None]*len(Deaths)

    #get sum of deaths
    deaths[0]=Deaths[0]
    for i in range(1,len(Date)):
        deaths[i] = Deaths[i]+deaths[i-1]

    #array of dictionaries with data
    for i in range(0,len(Date)):
        dic = {"date" : Date[i], "oil" : Crude_Oil[i], "deaths" : deaths[i]}
        data[i] = dic
    return data

def MMEMean(weeks):
    n = len(weeks[0])
    sum = 0

    for i in range(0,n):
        sum = sum + int(weeks[0][i]["deaths"])
    
    print(weeks[1])
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


def integrandExp(x,lambdA,likelihoodPois):
    return (lambdA*np.exp(-lambdA*x)*likelihoodPois)

def integrandPoisson(x, prod, constAll, likeliAll, lambdA):
    return (prod*constAll*likeliAll*lambdA*np.exp((-lambdA)*x))





def baysian(weeks):
    postArray = [None]*4
    constArray = [None]*4
    likeliArray = [None]*4

    # x = np.linspace(expon.ppf(0.01), expon.ppf(0.99), 100)
    x = np.linspace(expon.ppf(.01), 5, 100)
    lambdA = MMEMean(weeks)

    #I calculate the pdf of the exp --> assuming continuous
    pdfExp = [None]*len(x)
    for i in range(0, len(x)):
        pdfExp[i] = lambdA*np.exp(-lambdA*x[i])


    #likelihood of first --> poisson
    for j in range(len(weeks[0])):
        prod = (1/(factorial(int(weeks[0][j]["deaths"]))))*(lambdA**float(weeks[0][j]["deaths"]))*(np.exp(-float(weeks[0][j]["deaths"])))
    likelihoodPois = np.exp(-lambdA)*prod
    likeliArray[0] = likelihoodPois

# expon.ppf(.01)
    # print("this is location")
    # print(expon.ppf(.01))
    # print(expon.ppf(.99))
    #I find the constant
    evalInt = integrate.quad(integrandExp, expon.ppf(.01),expon.ppf(.99), args= (lambdA, likelihoodPois))
    # print("printing eval int")
    # print(evalInt)
    
    bigConst = 1
    if(evalInt[0]!=0):
        bigConst = 1.0/evalInt[0]
    constArray[0] = bigConst
    #posterior
    post = [None]*len(x)
    for j in range(0, len(x)):
        post[j] = (likelihoodPois*pdfExp[j])*bigConst

    #plot it
    plt.plot(x, post)
    postArray[0] = post



    for i in range(0,3):
        #variables used
        constAll = 1
        for m in range(0,len(constArray)):
            if(constArray[m]!=None):
                constAll = constArray[m]*constAll
        likeliAll = 1
        for m in range(0, len(likeliArray)):
            if(likeliArray[m]!=None):
                likeliAll = likeliArray[m]*likeliAll
        #likelihood
        prod = 1
        for m in range(0,len(weeks[i+1])):
            prod = constAll*likeliAll*lambdA*np.exp((-lambdA)*float(weeks[i+1][m]["deaths"]))
        
        
        #get the constant
        evalInt = integrate.quad(integrandPoisson, expon.ppf(.01),expon.ppf(.99), args= (prod, constAll, likeliAll, lambdA))
        # , points = [1,4]
        print("printing eval int")
        print(evalInt)

    
        bigConst=1.0
        if(evalInt[0] !=0):
            bigConst = 1.0/evalInt[0]

        #store variables
        constArray[i+1] = bigConst
        likeliArray[i+1] = prod

        #post pdf
        post = bigConst*prod*constAll*likeliAll*lambdA*np.exp((-lambdA)*(x))


        plt.plot(x,post)


    
    plt.show()


weeks = readData()
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
baysian(weeks)

# def arrayLikeli():
#     arrayLikeli = []
#     arrayConst = []

#     for i in range(0,4):
#         text = input("likeli " + str(i+1) + " : ")
#         arrayLikeli[i] = float(text)
    
#     for i in range(0,4):
#         text = input("consts " + str(i+1) + " : ")
#         arrayLikeli[i] = float(text)

# def baysianGraphs(arrayLikeli, arrayConst, weeks):
#     x = np.linspace(expon.ppf(0.01), expon.ppf(0.99), 100)
#     lambdA = MMEMean(weeks)

#     d1  = arrayConst[0]*arrayLikeli[0]*(1/lambdA)*(np.exp((-1/lambdA)*(x)))
#     d2 = arrayConst[1]*arrayLikeli[1]*d1
#     d3 = arrayConst[2]*arrayLikeli[2]*d2
#     d4 = arrayConst[3]*arrayLikeli[3]*d3 

#     plt.plot(x,d1)
#     plt.plot(x,d2)
#     plt.plot(x,d3)
#     plt.plot(x,d4)  

#     plt.show() 


# def integrandPoisson(x, likelihoodPois, postArray):
#     j =0
#     tempPost = None
#     for i in range(0,4):
#         if postArray[j]!=None:
#             tempPost = postArray[j]
#     print("this si temp post")
#     print(likelihoodPois)
#     print(tempPost)
#     return (tempPost*likelihoodPois)
#     # return (mean*np.exp(-mean*x)*likelihoodPois)





#get posterior distribution for each
#plot posterior


#I get the likelihood of the prior (exp)
# temp = mean**next
# sum = 0
# for i in range(0, len(weeks[0])):
#     sum = sum + int(weeks[0][i])
# likelihoodExp = temp*math.exp(-mean*sum)

# x2 = lambda x: (mean*np.exp(-mean*x)*likelihoodPois)