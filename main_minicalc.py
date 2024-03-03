""" CALCULATOR !!! """
from colorama import Fore, Style


def main():

    operand = None
    operator = None
    result = None
    wait_for_number = True

    while 1:

        if wait_for_number:         
            
            # operand = input(f">>> Enter positive number or [q] for exit: ")

            print(Fore.BLUE + ">>> " + Fore.GREEN + "Enter positive " + Fore.WHITE + "number" + \
                Fore.GREEN + " or [q] for exit: " + Fore.YELLOW, end="")
            operand = input()

            if operand == "q":
                break
            elif operand == "=":
                if result is None:
                    print(f"There were no operand yet!")
                    print("_" * 27)
                    continue
                else:
                    print(f"Result of calculation:\t{result}")
                    break
            else:
                if result is None:
                    try:
                        operand = int(operand)
                        result = operand
                    except ValueError:
                        print(f"{operand} is not a number. Try again.")
                        print("_" * 30)
                        continue
                else:
                    try:
                        operand = float(operand)
                        if operator == "+":
                            result += float(operand)
                        elif operator == "-":
                            result -= float(operand)
                        elif operator == "*":
                            result *= float(operand)
                        elif operator == "/":
                            try:
                                result /= float(operand)
                            except ZeroDivisionError:
                                print(f"Division by zero detected!")
                                print("_" * 27)
                                continue
                    except ValueError:
                        print(f"{operand} is not a number. Try again.")
                        print("_" * 30)
                        continue
                
            wait_for_number = False

        else:
            
            # operator = input(f">>> Enter math operator or [q] for exit: ")

            print(Fore.BLUE + ">>> " + Fore.GREEN + "Enter " + Fore.WHITE + "math" + Fore.GREEN + \
                " operator or [q] for exit: " + Fore.YELLOW, end="")
            operator = input()

            if operator == "q":
                break
            elif operator == "=":
                if result is not None:
                    print(f"Result of calculation:\t{result}")
                else:
                    print(f"Result of calculation:\t{operand}")
                break
            elif operator not in ["+", "-", "/", "*"]:
                print(f"{operator} not '+' or '-' or '/' or '*'. Try again.")
                print("_" * 43)
                continue              

            wait_for_number = True
    
    print("Good by!" + Style.RESET_ALL)
    

if __name__ == "__main__":
    main()