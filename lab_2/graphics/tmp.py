def main():
    size: int = int(input())
    a: list = list(map(int, input().split()))

    b: list = a[size - 1:size] + a[0:size - 1]

    print(*b)


if __name__ == '__main__':
    main()
