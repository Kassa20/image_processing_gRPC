
import sys

def test(a, b):
    
    if a == 1 and b == 1:
        return a, b

    return a

def main():

    a = 1
    b = 1

    print(test(a, b))


if __name__ == '__main__':
    main()
