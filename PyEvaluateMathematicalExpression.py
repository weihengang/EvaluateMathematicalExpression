#ORDER OF PRECEDENCE - ^, (), /*, +-  "4 + 18 / (9 - 3)"
import math as m
str_equation = input("Enter expression to evaluate: ").replace(" ", "")
def solve_equation(equation):
    dict_precedence = {
    "^": (lambda A, B: pow(A, B), 3),
    "*": (lambda A, B: A * B, 2),
    "/": (lambda A, B: A / B, 2),
    "+": (lambda A, B: A + B, 1),
    "-": (lambda A, B: A - B, 1),
    "sin": lambda x: m.sin(x * m.pi / 180),
    "cos": lambda x: m.cos(x * m.pi / 180),
    "tan": lambda x: m.tan(x * m.pi / 180),
    "csc": lambda x: 1 / m.sin(x * m.pi / 180),
    "sec": lambda x: 1 / m.cos(x * m.pi / 180),
    "cot": lambda x: 1 / m.tan(x * m.pi / 180),
    "asin": lambda x: m.asin(x) / m.pi * 180,
    "acos": lambda x: m.acos(x) / m.pi * 180,
    "atan": lambda x: m.atan(x) / m.pi * 180,
    "sinh": lambda x: m.sinh(x),
    "cosh": lambda x: m.cosh(x),
    "tanh": lambda x: m.tanh(x),
    "fact": lambda x: m.factorial(int(x)),
    "loge": lambda x: m.log(x),
    "log": lambda x: m.log10(x),
    }
    class Operator:
        def __init__(self, operator, number_A, number_B):
            self.operator = operator
            self.number_A = number_A
            self.number_B = number_B
        def __repr__(self):
            return f"{self.number_A}{self.operator}{self.number_B}"
    assert type(equation) == str
    for i in list(dict_precedence.keys()):
        if (i == "-" and equation.count(i) == 1 and equation.index(i) == 0):
            continue
        if (i in equation):
            break
    else:
        return equation
    #find the most important operator and split equation in two
    while ("(" in equation):
        start_index = equation.index("(")
        term_bracket = ""
        bracket_count = 1
        for i in range(start_index + 1, len(equation)):
            char = equation[i]
            if (char == "("):
                bracket_count += 1
            if (char == ")"):
                bracket_count -= 1
            if (bracket_count == 0):
                break
            term_bracket += char
        partial_solution = solve_equation(term_bracket)
        if (start_index > 2 and equation[start_index - 1].isalpha()): #function instead of bracket
            index = 0
            for i in range(1, start_index + 1):
                index = start_index - i
                if (equation[index] in dict_precedence): #operator found
                    break
            else:
                index = -1
            function_name = equation[index + 1:start_index]
            equation = equation.replace(f"{function_name}({term_bracket})", str(dict_precedence[function_name](float(partial_solution))))
        else:
            equation = equation.replace(f"({term_bracket})", str(partial_solution)) 
    list_Operator = []
    for i in range(1, len(equation)): #find and isolate the operator with the most precedence
        char = equation[i]
        if ((not char.isnumeric()) and char != "."):
            str_A = ""
            for j in range(1, i + 1):
                char_A = equation[i - j]
                if ((char_A == "-" and j == i) or (char_A == "-" and not equation[i - j - 1].isnumeric())): # 12 + -12 / 11, evaluating /
                    str_A += char_A
                    continue
                if (char_A.isnumeric() or char_A == "."):
                    str_A += char_A
                else:
                    break
            str_A = str_A[::-1]
            str_B = ""
            for j in range(i + 1, len(equation)):
                char_B = equation[j]
                if (char_B == "-" and j == i + 1):
                    str_B += char_B
                    continue
                if (char_B.isnumeric() or char_B == "."): # 12 + -11
                    str_B += char_B
                else:
                    break
            list_Operator.append(Operator(char, str_A, str_B))
    if (len(list_Operator) == 0):
        return equation
    current_value = 0
    current_operator = None
    for Operator in list_Operator:
        precedence = dict_precedence[Operator.operator][1]
        if (current_value < precedence):
            current_value = precedence
            current_operator = Operator
    print(list_Operator)
    value = dict_precedence[current_operator.operator][0](float(current_operator.number_A), float(current_operator.number_B))
    if ("e" in str(value)): #smaller than 10^-4
        value = 0
    equation = equation.replace(f"{current_operator.number_A}{current_operator.operator}{current_operator.number_B}", str(value))
    return solve_equation(equation)
print(solve_equation(str_equation))