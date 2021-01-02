import csv
from scipy import stats
import copy
# from scipy.stats import chisqprob


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

def jetFuelData(Date, Jet_Fuel, Deaths):
    #days, jet_fuel, deaths
    data = [None]*len(Date)
    deaths = [None]*len(Deaths)

    #get sum of deaths
    deaths[0]=Deaths[0]
    for i in range(1,len(Date)):
        deaths[i] = Deaths[i]+deaths[i-1]

    #array of dictionaries with data
    for i in range(0,len(Date)):
        dic = {"date" : Date[i], "jet_fuel" : Jet_Fuel[i], "deaths" : deaths[i]}
        data[i] = dic
    return data

def dataDay(data):
    dataNew = copy.deepcopy(data)
    print(data[0])
    for i in range(1,len(data)):
        dataNew[i]["deaths"] = int(data[i]["deaths"])-int(data[i-1]["deaths"])

    return dataNew

#calculate the total for each row and each column
def total(data, param):
    totalColumn = []
    totalRow = []
    sumOil = 0
    sumDeaths =0
    for i in range(0,len(data)):
        sum = float(data[i][param]) + float(data[i]["deaths"])
        totalColumn.append(sum)

        sumOil = sumOil + float(data[i][param])
        sumDeaths = sumDeaths + float(data[i]["deaths"])
    totalRow.append(sumOil)
    totalRow.append(sumDeaths)
    
    # print(totalColumn)
    # print("\n")
    # print(totalRow)
    return totalColumn, totalRow

def jet_fuelCumData(Date, Jet_Fuel, deaths):
    data = [None]*len(Date)
    for i in range(0,len(Date)):
        dic = {"date" : Date[i], "jet_fuel" : Jet_Fuel[i], "deaths" : deaths[i]}
        data[i] = dic
    return data

def totalOfTotalColumn(totalRow):
    sum = 0.0
    for i in range(0, len(totalRow)):
        sum = totalRow[i] + sum
    return sum

#calculate the expected value
def expected(totalColumn, totalRow, total):
    expDataArray = [None]*len(totalColumn)
    for i in range(0,len(totalRow)):
        for m in range(0,len(totalColumn)):
            expected = (totalColumn[m])*(totalRow[i]/total)
            if(expDataArray[m]==None):
                expDataArray[m] = [expected]
            else:
                expDataArray[m].append(expected)
    return expDataArray

def Qobs(expDataArray, data, param):
    tempArray = [None]*(len(expDataArray)*2)

    count = 0
    for i in range(0,len(expDataArray)):
        for j in range(0,2):
            name = param
            if(j ==1):
                name = "deaths"
            num = (expDataArray[i][j] - float(data[i][name]))**2
            value = num/expDataArray[i][j]
            tempArray[count]= value
            count = count+1

    sum =0
    for m in range(0,len(tempArray)):
        sum = sum + tempArray[m]

    # print(sum)
    return sum

def degreesFreedom(colums, rows):
    return (len(rows)-1)*(len(colums)-1)

def p_value(qobs, df):
    return (1-stats.chi2.cdf(qobs , df))

oil = [55.51, 54.09, 53.09, 53.33, 53.29, 52.19, 51.58, 50.06, 49.59, 50.87, 50.94, 50.34, 49.59, 50.0, 51.13, 51.41, 52.03, 52.1, 53.31, 53.77, 53.36, 51.36, 49.78, 48.67, 47.17, 44.83, 46.78, 47.27, 46.78, 45.9, 41.14, 31.05, 34.47, 33.13, 31.56, 31.72, 28.96, 26.96, 20.48, 25.09, 19.48, 23.33, 21.03, 20.75, 16.6, 15.48, 14.1, 20.51, 20.28, 25.18, 28.36, 26.21, 23.54, 24.97, 22.9, 22.36, 19.82, 18.31, 13.64, 15.06, 15.99, 12.17]
Date = ['1/23/2020', '1/24/2020', '1/27/2020', '1/28/2020', '1/29/2020', '1/30/2020', '1/31/2020', '2/3/2020', '2/4/2020', '2/5/2020', '2/6/2020', '2/7/2020', '2/10/2020', '2/11/2020', '2/12/2020', '2/13/2020', '2/14/2020', '2/18/2020', '2/19/2020', '2/20/2020', '2/21/2020', '2/24/2020', '2/25/2020', '2/26/2020', '2/27/2020', '2/28/2020', '3/2/2020', '3/3/2020', '3/4/2020', '3/5/2020', '3/6/2020', '3/9/2020', '3/10/2020', '3/11/2020', '3/12/2020', '3/13/2020', '3/16/2020', '3/17/2020', '3/18/2020', '3/19/2020', '3/20/2020', '3/23/2020', '3/24/2020', '3/25/2020', '3/26/2020', '3/27/2020', '3/30/2020', '3/31/2020', '4/1/2020', '4/2/2020', '4/3/2020', '4/6/2020', '4/7/2020', '4/8/2020', '4/9/2020', '4/13/2020', '4/16/2020', '4/17/2020', '4/22/2020', '4/23/2020', '4/24/2020', '4/27/2020']
Deaths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 2, 0, 3, 4, 5, 6, 6, 7, 23, 25, 41, 46, 61, 115, 181, 258, 286, 373, 581, 843, 930, 1111, 1169, 1304, 1999, 1846, 1870, 1551, 2141, 2188, 2179, 2016, 1992, 1355]
jetFuel = [1.702, 1.665, 1.598, 1.641, 1.62, 1.584, 1.504, 1.45, 1.451, 1.52, 1.553, 1.522, 1.491, 1.5, 1.56, 1.576, 1.591, 1.559, 1.584, 1.583, 1.582, 1.511, 1.466, 1.412, 1.384, 1.381, 1.438, 1.43, 1.438, 1.379, 1.275, 1.039, 1.112, 1.057, 0.945, 0.977, 0.836, 0.838, 0.724, 0.777, 0.716, 0.697, 0.687, 0.692, 0.728, 0.766, 0.725, 0.697, 0.65, 0.705, 0.808, 0.765, 0.729, 0.731, 0.69, 0.707, 0.653, 0.667, 0.507, 0.497, 0.453, 0.407]

oilData = oilData(Date, oil, Deaths)
jetFuelData = jetFuelData(Date, jetFuel, Deaths)
oilDataDay = dataDay(oilData)
jetFuelDataDay = jet_fuelCumData(Date, jetFuel, Deaths)

totalOilColumn, totalOilRow = total(oilData, "oil")
totalJetFuelColumn, totalJetFuelRow = total(jetFuelData, "jet_fuel")
totalOilDayColumn, totalOilDayRow = total(oilDataDay, "oil")
totalJetFuelDayColumn, totalJetFuelDayRow = total(jetFuelDataDay, "jet_fuel")

totalOil = totalOfTotalColumn(totalOilRow)
totalJetFuel = totalOfTotalColumn(totalJetFuelRow)
totalOilDay = totalOfTotalColumn(totalOilDayRow)
totalJetFuelDay = totalOfTotalColumn(totalJetFuelDayRow)

expectedOilArray = expected(totalOilColumn, totalOilRow, totalOil)
expectedJetFuelArray = expected(totalJetFuelColumn, totalJetFuelRow, totalJetFuel)
expectedOilDayArray = expected(totalOilDayColumn, totalOilDayRow, totalOilDay)
expectedJetFuelDayArray = expected(totalJetFuelDayColumn, totalJetFuelDayRow, totalJetFuelDay)

qobsOil = Qobs(expectedOilArray, oilData, "oil")
qobsJetFuel = Qobs(expectedJetFuelArray, jetFuelData, "jet_fuel")
qobsOilDay = Qobs(expectedOilDayArray, oilDataDay, "oil")
qobsJetFuelDay = Qobs(expectedJetFuelDayArray, jetFuelDataDay, "jet_fuel")

degreesFreedomOil = degreesFreedom(totalOilColumn, totalOilRow)
degreesFreedomJetFuel= degreesFreedom(totalJetFuelColumn, totalJetFuelRow)
degreesFreedomOilDay = degreesFreedom(totalOilDayColumn, totalOilDayRow)
degreesFreedomJetFuelDay= degreesFreedom(totalJetFuelDayColumn, totalJetFuelDayRow)

p_valueOil = p_value(qobsOil, degreesFreedomOil)
p_valueJetFuel = p_value(qobsJetFuel, degreesFreedomJetFuel)
p_valueOilDay = p_value(qobsOilDay, degreesFreedomOilDay)
p_valueJetFuelDay = p_value(qobsJetFuel, degreesFreedomJetFuelDay)

print("\n")
print("Oil Qobs: " + str(qobsOil))
print("degrees freedom: " + str(degreesFreedomOil))
print("p-value: "+ str(p_valueOil))

print("\n")
print("Jet Fuel Qobs: " + str(qobsJetFuel))
print("degrees freedom: " + str(degreesFreedomJetFuel))
print("p-value: "+ str(p_valueJetFuel))

print("\n")
print("Oil Day Qobs: " + str(qobsOilDay))
print("degrees freedom: " + str(degreesFreedomOilDay))
print("p-value: "+ str(p_valueOilDay))

print("\n")
print("Jet Fuel Day Qobs: " + str(qobsJetFuelDay))
print("degrees freedom: " + str(degreesFreedomJetFuelDay))
print("p-value: "+ str(p_valueJetFuelDay))


# p_value2 = p_value(3.4, 1)
# print(p_valueOil)
# print(p_valueJetFuel)
# temp = 3.84
# tempdf = 1
# p_valTemp = p_value(temp, tempdf)
# print(p_valTemp)

# print(chisqprob(qobsOil, degreesFreedomOil))


