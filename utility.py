YELLOW = '\033[1;33m'
CYAN = '\033[0;36m'
END = '\033[0m'

def debug(*args):
    print(f'{CYAN}DEBUG{END}:    ', end='')
    print(*args)