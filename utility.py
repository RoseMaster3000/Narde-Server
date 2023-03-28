YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
RED = '\033[0;31m'
END = '\033[0m'

def debug(*args):
    print(f'{CYAN}DEBUG{END}:    ', end='')
    for a in args:
        print(a, end=" ")
    print()
