from interpreter import Interpreter
from part5_examples import examples


if __name__ == "__main__":
    # run the examples and print the titles and outputs for each one
    for title, statements, expected in examples():
        print(title + ":")
        Interpreter().run(statements)
        print()
