from src.helpers import is_in_list
from src.server import run_server
import sys
import time

def main():
    run_server()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
