import numpy as np
import csv

p_val_cutOff = .05

#I get 1999 and 2000 data
def firstSample():
    data_1999 = []
    data_2009 = []

    with open('1999_data.csv', newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data_1999.append(float(row[24]))

    with open('2009_data.csv', newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data_2009.append(float(row[24]))
    
    return data_1999, data_2009

#I get 2009 and 2019 data
def secondSample():
    data_2019 = []
    data_2009 = []

    with open('2019_data.csv', newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data_2019.append(float(row[24]))

    with open('2009_data.csv', newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data_2009.append(float(row[24]))
    
    return data_2009, data_2019

def average(x):
    sum = 0
    for i in range(0, len(x)):
        sum = sum + x[i]
    
    return (sum/len(x))

def factorial(n):
    answer = 1
    for i in range(1,(n+1)):
        answer = answer*i
    return answer

def permutationTest(n, x, y):
    # arrayOfDif = []
    tempList = []
    countOfGreaterThan = 0

    #original difference
    avX = average(x)
    avY = average(y)
    orgDif = abs(avX - avY)

    #combine data
    for i in range(0, len(x)):
        tempList.append(x[i])
    for i in range(0, len(y)):
        tempList.append(y[i])

    for i in range(0,n):
        #get permuted data
        st = np.random.permutation(tempList)
        
        #calculate average of data
        sumX = 0.0
        sumY = 0.0
        for j in range(0, len(x)):
            sumX = sumX + st[j]
        for j in range(len(x), len(st)):
            sumY = sumY + st[j]
        #calculate average value
        avX = sumX/len(x)
        avY = sumY/len(y)

        dif = abs(avX - avY)

        if(dif>orgDif):
            countOfGreaterThan = countOfGreaterThan +1

    p_value = countOfGreaterThan/n
    return p_value

def passFailPrint(p_value, cutOff, year1, year2, n):

    print("\nFor the years " + str(year1) + " and " + str(year2) + ", with " +  str(n) + " permutations, the p-value obtained was " + str(p_value) + ".")
    if p_value<cutOff:
        print("The null hypothesis is therefore rejected.")
    else:
        print("The null hypothesis is therefore accepted.")



x1, y1 = firstSample()
x2, y2 = secondSample()

p_value1_200 = permutationTest(200, x1,y1)
p_value2_200 = permutationTest(200,x2,y2)

print("Part A)")
passFailPrint(p_value1_200, .05, 1999, 2000, 200)
passFailPrint(p_value2_200, .05, 2009, 2019, 200)

p_value1_1000 = permutationTest(200, x1,y1)
p_value2_1000 = permutationTest(200,x2,y2)

print("\nPart B)")
passFailPrint(p_value1_1000, .05, 1999, 2000, 200)
passFailPrint(p_value2_1000, .05, 2009, 2019, 200)
