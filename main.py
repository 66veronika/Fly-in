from parser import Parser


def main():
    parser = Parser("maps/example.txt")
    slovnik = parser.parse()
    for v in slovnik.values():
        print(v)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print("cvbhlcgxhfvvzh", e)

