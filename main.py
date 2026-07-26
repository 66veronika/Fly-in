from parser import Parser
from validator import Validator


def main():
    parser = Parser("maps/example.txt")
    data = parser.parse()
    validator = Validator(data)
    validator.validate()

    print("\n=== Validated data ===")
    print(data)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
