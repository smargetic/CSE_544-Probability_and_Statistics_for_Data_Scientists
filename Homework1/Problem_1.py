from random import random

n = raw_input("Please provide the number of variables: ")
n = int(n)

numberOfTimesTie = 0
numberOfFourThree = 0

# part A and C
for i in range(0, n):  # number of simulations
    torWins = 0
    phiWins = 0
    print("here1")
    for j in range(0, 4):
        print("in for")
        intReturned = random()
        if intReturned > .5:
            torWins = torWins + 1
        else:
            phiWins = phiWins + 1
        print("torWins", torWins)
        print("phiWins", phiWins)
    if torWins == phiWins:
        print("tie")
        numberOfTimesTie = numberOfTimesTie + 1
        while torWins != 4 and phiWins != 4:
            intReturned = random()
            if intReturned > .5:
                torWins = torWins + 1
            else:
                phiWins = phiWins + 1
        if torWins == 4:
            numberOfFourThree = numberOfFourThree + 1

print ("Number of ties: ", numberOfTimesTie)
print ("Number of 4-3", numberOfFourThree)

pA = float(numberOfTimesTie) / float(n)
pBA = float(numberOfFourThree) / float(numberOfTimesTie)

print("P(A): ", pA)
print("P(B|A): ", pBA)

numberOfFourThree = 0

# Part e
for i in range(0, n):
    torWins = 0
    phiWins = 0
    for j in range(0, 2):
        print (j)
        intReturned = random()
        if intReturned <= .75:
            torWins = torWins + 1
        else:
            phiWins = phiWins + 1
    for j in range(0, 2):
        print (j)
        intReturned = random()
        if intReturned > .75:
            torWins = torWins + 1
        else:
            phiWins = phiWins + 1
    intReturned = random()

    if intReturned <= .75:
        torWins = torWins + 1
    else:
        phiWins = phiWins + 1

    intReturned = random()
    if intReturned > .75:
        torWins = torWins + 1
    else:
        phiWins = phiWins + 1

    intReturned = random()
    if intReturned <= .75:
        torWins = torWins + 1
    else:
        phiWins = phiWins + 1
    if (torWins == 4) and (phiWins == 3):
        numberOfFourThree = numberOfFourThree + 1

# Need to do binomial
