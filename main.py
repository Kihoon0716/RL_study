from backend import Tetris
from front import Front
import time
import random
from backend import Move

def run():
    front = Front()
    tetris = Tetris()
    t = time.time()
    count = 0
    while True:
        # command = front.get_command()
        command = random.choice(list(Move))
        score, map = tetris.tick(command = command)
        # front.show(map=map)
        # time.sleep(0.1)
        count += 1
        if count == 100:
            fps = 100 / (time.time() - t)
            count = 0
            t = time.time()
            print(fps)
if __name__ == "__main__":
    run()