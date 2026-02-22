
import sys

def test(a, b):
    
    if a == 1 and b == 1:
        return a, b

    return a

def main():

    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]

if __name__ == '__main__':
    main()
