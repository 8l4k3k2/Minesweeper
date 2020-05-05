#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Jonathan Grimm"
__date__ = "initially done: 28.04.17 updated to Python3.8 and PyQt5: 05/2020"

import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


def asd(x=10):
    a = []
    for i in range(x):
        a.append([0] * x)
    return a


# d= asd(3,4)


class field(QtWidgets.QWidget):
    def __init__(self):
        super(field, self).__init__()
        self.size = 10
        self.array = [[None for i in range(self.size)] for j in range(self.size)]

        self.mines = 20
        self.x = 850
        self.y = 950
        self.win = False

        self.optionmod = 0

        self.createBombArray()
        self.initGUI()

    def createBombArray(self):
        self.bombarray = [[0 for i in range(self.size)] for j in range(self.size)]
        for x in range(self.mines):
            while True:
                xkoord = random.randrange(0, self.size, 1)
                ykoord = random.randrange(0, self.size, 1)
                if self.bombarray[ykoord][xkoord] == 0:
                    self.bombarray[ykoord][xkoord] = 1
                    break

    def checkbomb(self, x, y):
        return self.bombarray[int(x)][int(y)] == 1

    def surroundbombnumber(self,x, y):
        bcnt=0
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if i == 0 and j == 0:
                    pass
                else:
                    if self.size > x + i >=0 and self.size > y + j >= 0:
                        if self.checkbomb(x+i,y+j):
                            bcnt +=1
        if self.bombarray[x][y] != 1 and bcnt !=0:
            self.array[x][y] = bcnt
        return bcnt

    def checksurroundfieldsforsurroundbomb(self,x, y):
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if self.size > x + i >= 0 and self.size > y + j >= 0:
                    if self.surroundbombnumber(x + i, y + j) == 0 and self.array[x + i][y + j] != 0 and self.bombarray[x + i][y + j] != 1:
                        self.array[x + i][y + j] = 0
                        self.checksurroundfieldsforsurroundbomb(x + i, y + j)

    def showend(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.bombarray[i][j] == 1:
                    self.array[i][j] = "X"

    def mod_update(self):
        self.update()
        self.cellwidth = (self.x - 2 * self.border) // self.size

    def asdfg(self):
        print("asdfg")
        pass

    def initGUI(self):

        self.button_options = QtWidgets.QPushButton("Options", self)
        self.button_options.clicked.connect(self.gooptions)
        self.button_options.move(10, 10)

        self.button_saveoptions = QtWidgets.QPushButton("Save and reload", self)
        self.button_saveoptions.clicked.connect(self.saveoptions)
        self.button_saveoptions.move(10, 50)
        self.button_saveoptions.setEnabled(False)

        self.button_backoptions = QtWidgets.QPushButton("Back", self)
        self.button_backoptions.clicked.connect(self.backoptions)
        self.button_backoptions.move(200, 50)
        self.button_backoptions.setEnabled(False)

        self.label_size = QtWidgets.QLabel("Size: ", self)
        self.label_size.setStyleSheet('color: black')
        self.label_size.move(300, 13)

        self.entry_size = QtWidgets.QLineEdit(self)
        self.entry_size.setGeometry(450, 10, 60, 35)
        self.entry_size.setText("10")
        self.entry_size.setEnabled(False)

        self.label_mines = QtWidgets.QLabel("Mine count: ", self)
        self.label_mines.move(300, 53)

        self.entry_mines = QtWidgets.QLineEdit(self)
        self.entry_mines.setGeometry(450, 50, 60, 35)
        self.entry_mines.setEnabled(False)
        self.entry_mines.setText("20")

        self.setGeometry(300, 300, self.x, self.y)
        self.setWindowTitle("Minesweeper")
        self.show()

    def gooptions(self):
        if self.optionmod == 0:
            self.optionmod = 1
            self.button_saveoptions.setEnabled(True)
            self.button_backoptions.setEnabled(True)
            self.button_options.setEnabled(False)
            self.entry_size.setEnabled(True)
            self.entry_mines.setEnabled(True)

    def backoptions(self):
        if self.optionmod == 1:
            self.optionmod = 0
            self.button_saveoptions.setEnabled(False)
            self.button_backoptions.setEnabled(False)
            self.button_options.setEnabled(True)
            self.entry_size.setEnabled(False)
            self.entry_size.setText(str(self.size))
            self.entry_mines.setEnabled(False)
            self.entry_mines.setText(str(self.mines))

    def saveoptions(self):
        if self.optionmod == 1:
            try:
                self.size = int(self.entry_size.text())
                self.mines = int(self.entry_mines.text())
                if self.mines <= 0 or self.size <= 1:
                    self.entryerror2()
                elif self.mines >= self.size * self.size:
                    self.bomberror()
                else:
                    self.win = False
                    self.optionmod = 0
                    self.button_saveoptions.setEnabled(False)
                    self.button_backoptions.setEnabled(False)
                    self.button_options.setEnabled(True)
                    self.entry_size.setEnabled(False)

                    self.entry_size.setText(str(self.size))
                    self.entry_mines.setEnabled(False)

                    self.entry_mines.setText(str(self.mines))
                    self.array = [[None for i in range(self.size)] for j in range(self.size)]
                    self.createBombArray()
                    self.mod_update()
            except ValueError:
                self.entryerror()


    def mousePressEvent(self, QMouseEvent):
        if self.optionmod == 0:
            pos = QMouseEvent.pos()
            x = pos.x()
            y = pos.y()
            if self.border < x < self.x - self.border2 and self.y - self.x + self.border < y < self.y - self.border2:
                x -= self.border
                y = y - self.border - (self.y - self.x)
                i = x // self.cellwidth
                j = y // self.cellwidth

                # lose Bedingung
                if self.checkbomb(j,i):
                    # du hast verkackt
                    self.showend()

                    self.gooptions()
                    self.button_backoptions.setEnabled(False)
                    self.lose_window()

                else:
                    self.surroundbombnumber(j,i)
                    self.checksurroundfieldsforsurroundbomb(j,i)

                """
                if self.array[j][i] == 0:
                    self.array[j][i] = 1
                else:
                    self.array[j][i] = 0
                """
                if self.checkwin():
                    self.win = True
                    self.showend()
                    self.gooptions()
                    self.button_backoptions.setEnabled(False)
                    self.win_window()
                self.update()

    def entryerror(self):
        w = QtWidgets.QMessageBox()
        w.setText("No integer found!")
        w.setInformativeText("Please enter integer values")
        w.setIcon(QtWidgets.QMessageBox.Critical)
        w.setStandardButtons(QtWidgets.QMessageBox.Ok)
        w.setWindowTitle("ValueError")
        w.exec_()

    def entryerror2(self):
        w = QtWidgets.QMessageBox()
        w.setText("Please enter a size value greater than 1 and a bomb value greater than 0")
        w.setIcon(QtWidgets.QMessageBox.Critical)
        w.setStandardButtons(QtWidgets.QMessageBox.Ok)
        w.setWindowTitle("ValueError")
        w.exec_()

    def bomberror(self):
        w = QtWidgets.QMessageBox()
        w.setText("Too many bombs for the size of the minefield")
        w.setInformativeText("Increase the size of the minefield or reduce the number of bombs")
        w.setIcon(QtWidgets.QMessageBox.Critical)
        w.setStandardButtons(QtWidgets.QMessageBox.Ok)
        w.setWindowTitle("Error")
        w.exec_()

    def lose_window(self):
        w=QtWidgets.QMessageBox()
        w.setText("Du hast eine Bombe ausgewählt")
        w.setInformativeText("Du hast verloren!")
        w.setIcon(QtWidgets.QMessageBox.Critical)
        w.setStandardButtons(QtWidgets.QMessageBox.Ok)
        w.setWindowTitle("Du hast verloren!")
        w.exec_()

    def win_window(self):
        w=QtWidgets.QMessageBox()
        w.setText("Wow ich bin beeindruckt")
        w.setInformativeText("Bist ja doch nicht komplett unfaehig")
        w.setStandardButtons(QtWidgets.QMessageBox.Ok)
        w.setWindowTitle("GZ")
        w.exec_()


    def checkwin(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.array[i][j] is None:
                    if self.bombarray[i][j] != 1:
                        return False
        return True


    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.qp = qp
        self.drawGrid()
        qp.end()

    def drawGrid(self):
        self.qp.setBrush(QtGui.QColor(220, 220, 220))
        self.border = 10
        y1 = self.y - self.x + self.border
        x2 = self.x - 2 * self.border
        # m=self.size
        self.cellwidth = x2 // self.size
        x2 = self.cellwidth * self.size
        y2 = x2

        self.qp.drawRect(self.border, y1, int(x2), int(y2))

        self.border2 = self.x - (x2 + self.border)
        ygrid2 = self.y - self.border2
        xgrid2 = self.x - self.border2
        for i in range(self.size):
            self.qp.drawLine(int(self.border + self.cellwidth * i), y1, int(self.border + self.cellwidth * i), int(ygrid2))
            self.qp.drawLine(self.border, int(y1 + self.cellwidth * i), int(xgrid2), int(y1 + self.cellwidth * i))

        # self.drawcircles()
        self.drawrects()

    def drawrects(self):
        array = self.array
        self.qp.setBrush(QtGui.QColor(170, 170, 170))
        for i in range(self.size):
            for j in range(self.size):
                if array[j][i] is not None:
                    x = self.border + self.cellwidth * i
                    y = self.y - self.x + self.border + self.cellwidth * j

                    if array[j][i] == 'X':
                        if self.win is False:
                            self.qp.setBrush(QtGui.QColor(255, 0,0))
                        if self.win is True:
                            self.qp.setBrush(QtGui.QColor(0, 255,0))

                    self.qp.drawRect(x, y, self.cellwidth, self.cellwidth)
                    if array[j][i] == 'X':
                        self.qp.setBrush(QtGui.QColor(170, 170, 170))

                    # self.qp.setPen(QtGui.QColor(0, 255, 0))
                    if array[j][i] != 0:
                        self.qp.drawText(x, y, self.cellwidth, self.cellwidth, QtCore.Qt.AlignCenter, str(array[j][i]))
                    # self.qp.setPen(QtGui.QColor(0, 0, 0))


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = field()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


