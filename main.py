from parser import Parser
from validator import Validator

def main():
    parser = Parser("maps/example.txt")
    slovnik = parser.parse()
    validator = Validator(slovnik)
    validator.validate()


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)

