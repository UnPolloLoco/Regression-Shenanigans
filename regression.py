# Preparation

CODE = """
let state = Calc.getState();
state.expressions.list = [];

state.expressions.list.push(
    {"type":"folder", "id":"10000", "title":"Scary Stuff", collapsed:true}
);
"""

def createPush(x):
    return f'state.expressions.list.push({x});\n'

def adjustSubscripts(loopIter, x):
    startingNumber = 1
    if loopIter > len(letters):
        startingNumber = (loopIter - 1) // len(letters)
        startingNumber *= 10

    x = x.replace('A', str(startingNumber))
    x = x.replace('B', str(startingNumber + 1))
    x = x.replace('C', str(startingNumber + 2))
    return x



# Colors

CODE += createPush('{folderId: "10000", id:"7", latex:"c_{lightgray}=\\\\operatorname{rgb}\\\\left(210,210,210\\\\right)", type:"expression"}')
CODE += createPush('{folderId: "10000", id:"8", latex:"c_{darkgray}=\\\\operatorname{rgb}\\\\left(100,100,100\\\\right)", type:"expression"}')



# Scary function

latex = r"f\left(x\right)=\arctan\left(x^{\sin\left(x^{\arctan\left(x^{\sin\left(x^{\arctan x}\right)}\right)}\right)}\right)".replace('\\', '\\\\')

equationObject = '{folderId: "10000", id: "1", latex: "{latex}", type: "expression", colorLatex:"c_{lightgray}", lineStyle:"DASHED", lineWidth:"1.5" }'
equationObject = equationObject.replace('{latex}', latex)

CODE += createPush(equationObject)



# The table: function x value

c1values = ''
for bigN in range(0, 100):
    n = bigN / 10
    c1values += f'"{n}",'
column1 = '{hidden: true, id: "3", latex: "x_{1}", values: [{c1values}]}'
column1 = column1.replace('{c1values}', c1values)



# The table: function output

c2latex = r'f\\left(x_{1}\\right)'
column2 = '{colorLatex: "c_{darkgray}", id: "4", latex: "{c2latex}", values: ["{c2latex}"], lineWidth: "2.5", lines: true, pointSize: "5", pointStyle: "OPEN"}'
column2 = column2.replace('{c2latex}', c2latex)

tableObject = '{folderId: "10000", id: "2", type: "table", columns: [{column1}, {column2}]}'
tableObject = tableObject.replace('{column1}', column1).replace('{column2}', column2)

CODE += createPush(tableObject)



# Create y1

CODE += createPush('{folderId: "10000", id:"6", type:"expression", latex:"y_{1}=f\\\\left(x_{1}\\\\right)"}')



# Regression creation

regression = 'y_{1} \sim '

letters = 'abcdefghijklmnopqrstuvwz'
regressionMode = 'sine'
depth = 25

for n in range(1, depth+1):
    if regressionMode == 'sine': 
        term = adjustSubscripts(n, 'a_{A}\\sin\\left(a_{B}x_{1}-a_{C}\\right) +')
    
    if regressionMode == 'poly':
        term = adjustSubscripts(n, 'a_{A}\\left(a_{B}x_{1}-a_{C}\\right)^{__EXPONENT__} + ')
        term = term.replace('__EXPONENT__', str(n))
    
    letterIndex = (n-1) % len(letters)
    term = term.replace('a', letters[letterIndex])

    regression += term

    print(n, letters[letterIndex], term)

regression += 'k'
regressionObject = '{folderId: "10000", id: "5", hidden: false, latex: "{regression}", type: "expression", colorLatex:"c_{regcolor}"}'
regressionObject = regressionObject.replace('{regression}', regression.replace('\\', '\\\\'))



# Final code

CODE += createPush(regressionObject)
CODE += "Calc.setState(state);"



# Printing

color = '\033[0;93m'
reset = '\033[0m'

print(f'Mode:  {regressionMode}')
print(f'Depth: {depth}')
print()
print(f'{color}/* START */{reset}')
print()
print(CODE)
print()
print(f'{color}/* END */{reset}')
print()
