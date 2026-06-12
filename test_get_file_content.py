from functions.get_file_content import get_file_content


def tests() -> None:
    cases: list[list[str]] = [
        ["calculator", "main.py"],
        ["calculator", "pkg/calculator.py"],
        ["calculator", "/bin/cat"],
        ["calculator", "pkg/does_not_exist.py"],
    ]

    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    for c in cases:
        print(get_file_content(c[0], c[1]))


if __name__ == "__main__":
    tests()
