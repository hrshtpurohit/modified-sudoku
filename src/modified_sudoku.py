"""
MODIFIED SUDOKU -

    It is a modification of the old sudoku, where, a block is formed of a unique color.
    Example - red color forms a block and the red color block should have all non repeating numbers in the range 1 to 9
    The Code has been developed using PyQt ver - 5.7 for python ver - 3.5

    DEVELOPED BY : HARSHIT PUROHIT
"""

# Importing header files for Python development

import sys
import random
import copy
from datetime import datetime
random.seed()

# Importing header files for PyQt development

from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QTextBrowser,
    QInputDialog, QApplication, QGridLayout, QLabel, QMessageBox)
from PyQt5.QtGui import (QPalette, QFont, QIntValidator)

# Declaring global scope variables

n = 9
grid = [[0 for x in range(n)] for y in range(n)]
space = []
text_edit = []
text_browser = []

# Main class for application widget display

class Example(QWidget):

    # Constructor
    
    def __init__(self):
        super().__init__()
        
        self.initUI()    
        
    # PyQt application widget development
     
    def initUI(self):

        # Initial level selector message box implementation

        box0 = QMessageBox()
        box0.setWindowTitle("Setup")
        box0.setText("Yo! Bored of the old Sudoku. Try this one. Remember, unlike the old version, here every color forms a unique block. All the best! Choose your level - ")
        box0.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
        buttonX = box0.button(QMessageBox.Yes)
        buttonX.setText('Amatuer')
        buttonY = box0.button(QMessageBox.No)
        buttonY.setText('Professional')
        buttonZ = box0.button(QMessageBox.Cancel)
        buttonZ.setText('WorldClass')
        
        box0.exec_()

        # Variable storing value of level selected
        
        global tool

        if box0.clickedButton() == buttonX:
            tool = 4
        
        elif box0.clickedButton() == buttonY:
            tool = 5
            
        elif box0.clickedButton() == buttonZ:
            tool = 6

        # Time tracking - start time

        global start_time, end_time
        start_time = datetime.now()

        # Base font setup for complete layout

        font = QFont()
        font.setPointSize(30)
        self.setFont(font)
        global gr
        gr = QGridLayout()
        self.setLayout(gr)
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Modified Sudoku')
        self.setFixedSize(720,600)

        # Creating a Modified-Sudoku board with empty box initialized to '-'
 
        self.prepare_game()

        # Variables used for indexing text_edits and text_browsers respectively
        
        x = 0
        y = 0

        positions = [(i,j) for i in range(9) for j in range(9)]

        # Colour list

        color = ['red','green','yellow','blue','magenta','cyan','grey','pink','brown']

        # Displaying the created Modified Sudoku using text_edits to be edited by user and text_browsers for hint numbers
        
        for pos in positions:
            if grid[pos[0]][pos[1]][0] == '-':
                text_edit.append(QTextEdit(self))
                gr.addWidget(text_edit[x], *pos)
                text_edit[x].setFixedSize(60, 60)
                text_edit[x].setStyleSheet('background-color:'+color[grid[pos[0]][pos[1]][1]-1]+';')


                fone = QFont()
                fone.setBold(True)
                fone.setPointSize(30)
                text_edit[x].setFont(fone)
                x = x+1
            else:
                text_browser.append(QTextBrowser(self))
                temp = str(grid[pos[0]][pos[1]][0])
                text_browser[y].setText(temp)
                gr.addWidget(text_browser[y], *pos)
                text_browser[y].setFixedSize(60, 60)
                text_browser[y].setStyleSheet('background-color:'+color[grid[pos[0]][pos[1]][1]-1]+';')
                y = y+1

        # Response Buttons - Button 1 - Submit, Button 2 - Solve
        
        global button1, button2
        button1 = QPushButton('Submit')
        fon1 = QFont()
        fon1.setPointSize(12)
        button1.setFont(fon1)
        posi1 = [3,10]
        gr.addWidget(button1, *posi1)
        button1.clicked.connect(lambda: self.checkin())

        button2 = QPushButton('Solve')
        fon2 = QFont()
        fon2.setPointSize(12)
        button2.setFont(fon2)
        posi2 = [4,10]
        gr.addWidget(button2, *posi2)
        button2.clicked.connect(lambda: self.solving())
        
        self.move(200, 10)
        self.show()

    # Method for checking responses of the input from user - Win/Lose  
        
    def checkin(self):
        
        try:

            # Extracting indexes of the empty boxes in lexographic order and filling them up with user inputs
            
            for i in range(n*tool):
                temp = text_edit[i].toPlainText()    
                t = (ord(temp)-48)
                [a,b] = space.pop(0)
                y = grid[a-1][b-1][1]
                grid[a-1][b-1]=[t,y]

            answer = list(range(1,n+1))
            flag = 1
        
            # Comparing the every row/column of grid with correct answer by sorting every row/column
            
            for i in range(n):
                check = []
                for j in range(n):
                    x = grid[i][j][0]
                    check.append(x)
                check.sort()
                if answer != check:
                    flag=0

            for i in range(n):
                check = []
                for j in range(n):
                    x = grid[j][i][0]
                    check.append(x)
                check.sort()
                if answer != check:
                    flag=0

        # If input missing
        
        except Exception:
            flag=0

        # Display result - Won/Lost. If won, display time taken. Also disabling submit button so that user submits only once.
        
        if flag==0:
            box1 = QMessageBox.information(self, 'Game Over',"Sorry! You Lost", QMessageBox.Ok, QMessageBox.Ok)
            button1.setEnabled(False)
        else:

            # Time tracking - end time
            
            end_time = datetime.now()
            diff = end_time - start_time
            minu = str(int(diff.seconds/60))
            seco = str(diff.seconds%60)
            box1 = QMessageBox.information(self, 'Game Over',"Congrats! You Won. Time Taken - " + minu + " minutes and " + seco + " seconds", QMessageBox.Ok, QMessageBox.Ok)
            button1.setEnabled(False)
            button2.setEnabled(False)

    # Solve it for user. It simply displays the initially created Modified Sudoku board overriding the layout.

    def solving(self):
        positions = [(i,j) for i in range(9) for j in range(9)]
        text_edit.clear();
        text_browser.clear();
        color = ['red','green','yellow','blue','magenta','cyan','grey','pink','brown']
        y=0
        for pos in positions:          
            text_browser.append(QTextBrowser(self))
            temp = str(result[pos[0]][pos[1]][0])
            text_browser[y].setText(temp)
            gr.addWidget(text_browser[y], *pos)
            text_browser[y].setFixedSize(60, 60)
            text_browser[y].setStyleSheet('background-color:'+color[result[pos[0]][pos[1]][1]-1]+';')
            y = y+1
        button1.setEnabled(False)


    # Method for preparing game

    def prepare_game(self):

        # Try generating a Modified Sudoku board until not generated
        
        do_ = 1
        while(do_):
            try:
                loop = list(range(1,n+1))
                main = []
                for i in loop:
                        for j in loop:
                                main.append([i,j])
                for i in loop:
                        aux = []
                        for j in loop:
                            [x,y] = random.choice(main)
                            grid[x-1][y-1] = [i,j]
                            main.remove([x,y])
                            for l in loop:
                                    if [l,y] in main:
                                            z = main.index([l,y])
                                            aux.append(main.pop(z))
                            for l in loop:
                                    if [x,l] in main:
                                            z = main.index([x,l])
                                            aux.append(main.pop(z))
                        main.extend(aux)
                do_ = 0
            except Exception:
                pass

        # Copy the grid into result for desplaying solution
         
        global result
        result = copy.deepcopy(grid)

        # Creating empty box based on level selected
        
        for i in loop:
            rem = list(range(1,n+1))
            for j in range(tool):
                z = random.choice(rem)
                x = grid[i-1][z-1][1]
                grid[i-1][z-1]=['-',x]
                space.append([i,z])
                rem.remove(z)
        space.sort()
                
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

"""
    Thank You
"""
