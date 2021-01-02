import csv
import matplotlib.pyplot as plt

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

def plotECDFS(a, b, year1, year2):
    a.sort()
    b.sort()


    yValuesA = []
    yValuesB = []

    maxDif = [0, 0, "left", 0]

    #I get the y values
    for i in range(1, len(a)+1):
        yValuesA.append(i/len(a))
    for i in range(1,len(b)+1):
        yValuesB.append(i/len(b))

    #I calculate the difference to the left and right of a change in data set1
    for i in range(1, len(a)):
        tempLeft = 0
        tempRight = 0

        bValL = 0
        bValR = 0
        #I check for the "b" data point that is first less than or equal to the "a" data point
        for j in range(0, len(b)):
            if ((b[j]==a[i])):
                tempLeft = yValuesB[j-1]
                tempRight = yValuesB[j]
                bValL = j-1
                bValR = j

            elif ((b[j]<a[i])):
                tempLeft = yValuesB[j] #possibly j-1
                tempRight = yValuesB[j]
                bValR = j
                bValL = j
        
        dataChangeLeft = abs(yValuesA[i-1]-tempLeft)
        dataChangeRight = abs(yValuesA[i]-tempRight)

        #I check which change is greater and see how it compares to the max change value
        if dataChangeLeft>dataChangeRight:
            if dataChangeLeft>maxDif[0]:
                maxDif[0] = dataChangeLeft
                maxDif[1] = i
                maxDif[2] = "left"
                maxDif[3] = bValL
        else:
            if dataChangeRight>maxDif[0]:
                maxDif[0] = dataChangeRight
                maxDif[1] = i
                maxDif[2] = "right"
                maxDif[3] = bValR
    
    #I plot the graphs
    plt.step(a, yValuesA, label = year1)
    plt.step(b, yValuesB, label = year2)
    plt.legend(title='Data Sets')
    #I plot an arrow representing the max change  
    temp = 0
    yValB = yValuesB[maxDif[3]]
    if(maxDif[2]=="left"):
        temp = a[maxDif[1]-1]-.1
    else:
        temp = a[maxDif[1]-1]+.1

    plt.annotate("", xy=(temp, yValuesA[maxDif[1]]), xytext=(temp, yValB), arrowprops=dict(arrowstyle="<->"))
    
    str4Graph = "Max Dif: " + str(maxDif[0])
    plt.text((temp+.1), (yValuesA[maxDif[1]]/2), str4Graph, weight = "bold")
    titleStr = year1 + " versus " + year2
    plt.title(titleStr)
    plt.show()



x1, y1 = firstSample()
x2, y2 = secondSample()

plotECDFS(x1, y1, "1999 Data", "2009 Data")
plotECDFS(x2, y2, "2009 Data", "2019 Data")