from tkinter import *
from functools import partial #Solution from internet to allow passing custom commands from tkinter button in loop.
import tokenize
import math


def isfloat(string):  ##Checks if number is float.
    try:
        float(string)
        return True
    except ValueError:
        return False

def sinFunction(argument):
    return math.sin(argument)

def cosFunction(argument):
    return math.cos(argument)

def arcSinFunction(argument):
    try:
        return math.asin(argument)
    except ValueError:
        return 0

def arcCosFunction(argument):
    try:
        return math.acos(argument)
    except ValueError:
        return 0
def minusSign(argument):
    return argument*-1
def radianConvert(argument):
    try:
        return math.radians(argument)
    except ValueError:
        return 0

functionDictionary = {"sin":sinFunction ##A collection of different functions with key pairs
                      ,"cos":cosFunction
                    ,"arcsin":arcSinFunction
                      ,"arccos":arcCosFunction
                        ,"minus":minusSign
                      ,"radian":radianConvert
                      } 

def buttonPressed(buttonText):
    cursorPosition = inputLabel.index(INSERT)#index(INSERT) returns the value of the position of cursor
    expressionString = inputText.get()
    inputText.set(expressionString[0:cursorPosition] + "%s" %buttonText + expressionString[cursorPosition:len(inputText.get())])
    inputLabel.icursor(cursorPosition + len(str(buttonText))) ##icursor sets the position of the cursor in the entry widget.


def backSpace(): #Removes a character
    cursorPosition = inputLabel.index(INSERT)
    expressionString = inputText.get()
    inputText.set(expressionString[0:cursorPosition - 1] + expressionString[cursorPosition:len(inputText.get())])
    inputLabel.icursor(cursorPosition - 1)
6565
def clearAll():
    inputText.set("")
    outputText.set("")

def executeFunction(functionName,argument): ##Executes Named functions like Sin() Cos()
    for f in functionDictionary:
        if functionName.lower() in functionDictionary:
           return functionDictionary[functionName.lower()](argument)
    return argument
    
def evaluateExpression(expressionString):
    ##First the expression is converted into an postfix expression
    postFix = [',']  ##Commas are inserted as filler characters in stack
    postFixStack = ['(']
    expressionString = expressionString + ')' ##The brackets are added so that all the operands are evaluated in the end.
    functionFlag = 0 ##A Variable that keeps track of whether a function bracket is closed or not
    for x in expressionString:
        if x == '(':
            if postFix[len(postFix)-1].isalpha():
                postFix.append('[')
                functionFlag += 1
            postFixStack.append('(')
            postFix.append(',')
        if x == '^':
            postFixStack.append('^')
            postFix.append(',')
        if x in '/*':
            while postFixStack[len(postFixStack)-1] == '^':
                postFix.append(postFixStack.pop())
            postFixStack.append(x)
            postFix.append(',')
        if x in '+-':
            while postFixStack[len(postFixStack)-1] in '^*/':
                postFix.append(postFixStack.pop())
            postFixStack.append(x)
            postFix.append(',')

        if x == ')':
            while postFixStack[len(postFixStack)-1] != '(':
                postFix.append(postFixStack.pop())
            if functionFlag > 0:
                postFix.append(']')
                functionFlag -= 1
            postFixStack.pop()
            
        if isfloat(x) or x =='.':
            if isfloat(postFix[len(postFix)-1]):
                postFix[len(postFix)-1] += x
            else:
                postFix.append(x)
                
        if x.isalpha():
            if postFix[len(postFix)-1].isalpha():
                postFix[len(postFix)-1] += x
            else:
                postFix.append(x)
##        print(postFix)        
##        print(postFixStack)           
##        if x not in '^*/-+() ' and isfloat(x) == False and x.isalpha() == False:
##            outputText.set("Invalid Expression. Please Check Expression")    
##            return
##    if len(postFixStack) != 0:
##        outputText.set("Invalid Expression. Please Check Expression")
##        return
##    print(postFixStack)
##    input('Freeze')
    print(postFix)
    outputText.set(evaluatePostFix(postFix))

def evaluatePostFix(postFix):
    ##Evaluation of postfix Expression
    postFix.reverse()
    postFixStack = [] #Clearing postFixStack
##    print(postFix)
##    print("arg")
    x = len(postFix)-1
    currentToken = postFix[len(postFix)-1]
    while len(postFix) != 0:
        ##input('Freeze')
        print(postFix)
        currentToken = postFix[len(postFix)-1]
##        print(currentToken)
##        print('arg2')
        if currentToken.isalpha():
            postFix.pop()
            postFix.pop()
            tempStack = []
            functionFlag = 1
            while functionFlag > 0:
                if postFix[len(postFix)-1] == '[':
                    tempStack.append(postFix.pop())
                    functionFlag += 1
                    print("Beta")
                if postFix[len(postFix)-1] == ']':
                    functionFlag -= 1
                    if functionFlag == 0:
                        postFix.pop()
                        break
                    else:
                        tempStack.append(postFix.pop())
                ##input('Help')
                print("Alpha"+"%d"%functionFlag)
                if postFix[len(postFix)-1] not in "[]":
                    tempStack.append(postFix.pop())
            postFix.append(str(executeFunction(currentToken,evaluatePostFix(tempStack))))           
        if currentToken == ',':
            postFix.pop()
        if isfloat(currentToken):
            postFixStack.append(postFix.pop())
        if currentToken in '^*/-+':                
            operator = postFix.pop()
            if operator == '^':
                operator = '**'
            secondOperand = postFixStack.pop()
            firstOperand = postFixStack.pop()
            firstOperand = eval("%s%s%s" %(firstOperand,operator,secondOperand)) ##eval function in python evalulates a string as an expression.
            postFixStack.append(firstOperand)
    return float(postFixStack.pop())


    
def placeHolder():##Function to be used as a placeholder during development.
    pass

homeScreen = Tk(className=" Scientific Calculator")
homeScreen.resizable(0, 0)
##menuBar = Menu(homeScreen) ##Create a new object of class Menu
##homeScreen.config(menu=menuBar) ##Config is a function of the window used to add menu bar to it.
##
##fileSubMenu = Menu(menuBar)
##menuBar.add_cascade(label="FILE",menu=fileSubMenu)
####fileSubMenu.add_command(label = "New File",command = placeHolder)##Adding a command is optional
####fileSubMenu.add_command(label = "New Project",command = placeHolder)
####fileSubMenu.add_command(label = "Save",command = placeHolder)
####fileSubMenu.add_command(label = "Print",command = placeHolder)
####fileSubMenu.add_separator()
##fileSubMenu.add_command(label = "Quit",command="")

guiFrame = Frame(homeScreen)
inputText = StringVar()
outputText = StringVar()
inputLabel = Entry(guiFrame,bg="#00FF05",textvariable=inputText,width=55)
outputLabel = Label(guiFrame,bg="#00FF05",textvariable=outputText,anchor="se")
minusButton = Button(guiFrame,text="Minus",command = lambda: buttonPressed("minus("),width=7) ##Lambda Creates a one line function object
radianButton = Button(guiFrame,text="Radian",command = lambda: buttonPressed("radian("),width=7)

inputLabel.grid(row=0,column=0,sticky=N+S+E+W,ipady=9) ##TODO Fix the problem of entry not being able to strech.
outputLabel.grid(row=1,column=0,stick=N+S+E+W,ipady=9)
minusButton.grid(row=0,column=1,padx=(10,0),pady=5)
radianButton.grid(row=1,column=1,padx=(10,0),pady=5)
inputText.set("Sin(2+1)+Sin(3+1)")

keyPadFrame = Frame(homeScreen)
keyPadButton  = []
keyPadText = []
for i in range(0,10):
    keyPadText.insert(i,StringVar())
    keyPadText[i].set(i)
    keyPadButton.insert(i,Button(keyPadFrame,textvariable=keyPadText[i],command= partial(buttonPressed, i),width=7)) #partial allows passing fixed values to a function
    keyPadButton[i].grid(row=int(i/3),column = int(i%3),padx=5,pady=5)
keyPadButton[9].grid(row=3,column=1)
clearButton = Button(keyPadFrame,text="Clear",command=clearAll,width=7)
clearButton.grid(row=3,column=0)
backSpaceButton = Button(keyPadFrame,text="<-",command=backSpace,width=7)
backSpaceButton.grid(row=3,column=2)

operatorFrame1 = Frame(homeScreen)
operatorList1 = ["(",")","^","/","*","+","-","="]
operatorButton = []
for i in range(len(operatorList1)):
    operatorButton.append(Button(operatorFrame1,text=operatorList1[i],command= partial(buttonPressed,operatorList1[i]),width=7))
    operatorButton[i].grid(row=int(i/2),column = int(i%2),padx=5,pady=5)
operatorButton[len(operatorList1) - 1]["command"] = lambda: evaluateExpression(inputLabel.get())     

operatorFrame2 = Frame(homeScreen)
operatorList2 = ["Sin","Cos","arcSin","arcCos"]
operatorButton2 = []
for i in range(len(operatorList2)):
    operatorButton2.append(Button(operatorFrame2,text=operatorList2[i],command= partial(buttonPressed,operatorList2[i]+"("),width=7))
    operatorButton2[i].grid(row=int(i),column = int(0),padx=5,pady=5)


keyPadFrame.grid(row=1,column=0)
guiFrame.grid(row=0,column=0,columnspan=3,sticky=N+S+E+W,padx=5)
operatorFrame1.grid(row=1,column=1)
operatorFrame2.grid(row=1,column=2)
