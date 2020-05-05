# -*- coding: utf-8 -*-
import random

fg = 11  # Feldgröße(fg*fg Felder)
bombenzahl = 20

a = []  # Bombenfeld
for i in range(fg):
    atemp = []
    for j in range(fg):
        atemp.append(0)
    a.append(atemp)

b = []  # sichtbares Spielfeld
for i2 in range(fg):
    btemp = []
    for j2 in range(fg):
        btemp.append(" ")
    b.append(btemp)


def showminfield(x):
    line2 = "  "
    for i in range(fg):
        line2 += " ___"
    spaltennummer = "    "
    for i in range(fg):
        if i < 9:
            spaltennummer += str(i + 1) + "   "
        else:
            spaltennummer += str(i + 1) + "  "
    print(spaltennummer)
    print(line2)
    for i in range(fg):
        if i < 9:
            l1 = " " + str(i + 1) + "|"
        else:
            l1 = str(i + 1) + "|"
        l2 = "  |"
        for j in range(fg):
            l1 += " " + str(x[i][j]) + " |"
            l2 += "___|"
        print(l1)
        print(l2)
    print(spaltennummer)


def plantbombs():
    for x in range(bombenzahl):
        while True:
            xkoord = random.randrange(0, fg, 1)
            ykoord = random.randrange(0, fg, 1)
            if a[ykoord][xkoord] == 0:
                a[ykoord][xkoord] = 1
                break


def checkbomb(x, y):
    if a[x][y] == 1:
        return True
    else:
        return False


def surroundbombnumber(x, y):  # zählt die anzahl der bomben um das feld an der koord(x|y)
    bcnt = 0  # und markiert die Summe auf dem sichbaren spielfeld auf der koord(x|y)
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if i == 0 and j == 0:
                pass
            else:
                if fg > x + i >= 0 and fg > y + j >= 0:
                    if checkbomb(x + i, y + j) == True:
                        bcnt += 1
    if a[x][y] != 1 and bcnt != 0:
        b[x][y] = str(bcnt)
    return bcnt


def checksurroundfieldsforsurroundbomb(x, y):
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if fg > x + i >= 0 and fg > y + j >= 0:
                if surroundbombnumber(x + i, y + j) == 0 and b[x + i][y + j] != "0" and a[x + i][y + j] != 1:
                    b[x + i][y + j] = "0"
                    checksurroundfieldsforsurroundbomb(x + i, y + j)


def checkwin():
    for i in range(fg):
        for j in range(fg):
            if b[i][j] == " ":
                if a[i][j] != 1:
                    return False
    return True


def showend():
    for i in range(fg):
        for j in range(fg):
            if a[i][j] == 1:
                b[i][j] = "X"


plantbombs()
showminfield(b)
while True:
    while True:
        x = int(input("Zeile: "))
        y = int(input("Spalte: "))
        x = x - 1
        y = y - 1
        if b[x][y] != " ":
            print("falsche eingabe")
        else:
            break
    print
    if checkbomb(x, y) == True:
        showend()
        showminfield(b)
        print("you lose\n")
        break
    else:
        surroundbombnumber(x, y)
        checksurroundfieldsforsurroundbomb(x, y)
        # showminfield(a)
        print
        if checkwin() == True:
            showend()
            showminfield(b)
            print("you win\n")
            break
        showminfield(b)
