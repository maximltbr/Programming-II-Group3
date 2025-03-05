import random
import operator
import sympy as sp
def generate_math():
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }
    
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    op = random.choice(list(operators.keys()))

    # Ensure division results in an integer
    if operator == "/":
        num1 = num2 * random.randint(1, 10)  # Make num1 a multiple of num2

    problem = f"{num1} {op} {num2}"
    answer = operators[op](num1, num2)

    return problem, answer

def simplemexecute():
    while True:
        problem, answer = generate_math()
        print(f"Solve: {problem} = ?")
        try:
            user_answer = float(input("Your answer: "))
            if user_answer == answer:
                print("Correct!")
            elif user_answer == "q":
                break
            else:
                print(f"Wrong! The correct answer is {answer}")
        except ValueError:
            print("Please enter a number or 'q' to quit.")
        except TypeError:
            print("Please enter a number or 'q' to quit.")
            
def generatedifint():
    x = sp.Symbol('x')
    
    # Generate random polynomial coefficients and exponents
    coefficient = random.randint(1, 10)
    exponent = random.randint(1, 5)  # Keeps things simple
    
    # Create the function ax^n
    func = coefficient * x**exponent

    # Randomly decide if it's differentiation or integration
    if random.choice(["differentiate", "integrate"]) == "differentiate":
        problem = f"Differentiate: d/dx ({sp.latex(func)})"
        solution = sp.diff(func, x)  # Differentiate
    else:
        problem = f"Integrate: ∫ ({sp.latex(func)}) dx"
        solution = sp.integrate(func, x)  # Integrate
    return problem, solution
    
def difintexecute():
    while True:
        problem, solution = generatedifint()
        print(problem)
        try:
            user_answer = input("Your answer: ")
            if user_answer == str(solution):
                print("Correct!")
            elif user_answer == "q":
                break
            else:
                print(f"Wrong! The correct answer is {solution}")
        except ValueError:
            print("Please enter a number or 'q' to quit.")
        except TypeError:
            print("Please enter a number or 'q' to quit.")

def mexecute():
    choice = input("Would you like to 1. Solve math problems or 2. Differentiate/Integrate or 3. Quit? ")
    while True:    
        if choice == "1":
            simplemexecute()
        elif choice == "2":
            difintexecute()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")