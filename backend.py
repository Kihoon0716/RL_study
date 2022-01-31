from typing import List, Set, Dict, Tuple
from enum import Enum
import random
import time
from front import Front
import copy


class Pos:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Color(Enum):
    BLUE = 1
    RED = 2
    ORANGE = 3
    GREEN = 4
    PURPLE = 5
    YELLO = 6


class Move(Enum):
    TURN = 0
    LEFT = 1
    RIGHT = 2
    DROP = 3
    DOWN = 4


class MoveFeedback(Enum):
    SUCCESS = 0
    IMPOSSIBLE = 1
    STACKED = 2


class BlockType(Enum):
    BAR = 0
    RECT = 1
    Z = 2
    Z_R = 3
    MOUNTAIN = 4
    SEVEN = 5
    SEVEN_R = 6


class Block:
    def __init__(self) -> None:
        self.center = Pos(4, 2)
        self.turn_count = random.randint(0, 3)
        self.color = random.choice(list(Color)).value

    @property
    def cubes(self) -> List[List[int]]:
        pass

    def IsPositionable(self, map) -> bool:
        if not all(0 <= cube[0] < 10 and 0 <= cube[1] < 25 for cube in self.cubes):
            return False
        if not all(map[cube[1]][cube[0]] == 0 for cube in self.cubes):
            return False
        return True

    def move(self, direction: Move, map):
        if direction.value == Move.TURN.value:
            self.turn_count += 1
            if not self.IsPositionable(map=map):
                self.turn_count -= 1
                return MoveFeedback.IMPOSSIBLE

        elif direction.value == Move.LEFT.value:
            self.center.x -= 1
            if not self.IsPositionable(map=map):
                self.center.x += 1
                return MoveFeedback.IMPOSSIBLE

        elif direction.value == Move.RIGHT.value:
            self.center.x += 1
            if not self.IsPositionable(map=map):
                self.center.x -= 1
                return MoveFeedback.IMPOSSIBLE

        elif direction.value == Move.DOWN.value:
            self.center.y += 1
            if not self.IsPositionable(map=map):
                self.center.y -= 1
                return MoveFeedback.STACKED

        elif direction.value == Move.DROP.value:
            self.center.y += 1
            if not self.IsPositionable(map=map):
                self.center.y -= 1
                return MoveFeedback.STACKED
            else:
                self.move(direction=Move.DROP, map=map)
                return MoveFeedback.STACKED

        return MoveFeedback.SUCCESS


class BlockBar(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        if self.turn_count % 2 == 0:
            return [[self.center.x, self.center.y - 1, self.color], [self.center.x, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x, self.center.y + 2, self.color]]
        else:
            return [[self.center.x - 1, self.center.y, self.color], [self.center.x, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x + 2, self.center.y, self.color]]


class BlockRect(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        return [[self.center.x, self.center.y, self.color], [self.center.x + 1, self.center.y + 1, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color]]

class BlockZ(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        if self.turn_count % 2 == 0:
            return [[self.center.x, self.center.y, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x + 1, self.center.y + 1, self.color]]
        elif self.turn_count % 2 == 1:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x + 1, self.center.y - 1, self.color]]
class BlockZR(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        if self.turn_count % 2 == 0:
            return [[self.center.x, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x - 1, self.center.y + 1, self.color]]
        elif self.turn_count % 2 == 1:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x + 1, self.center.y + 1, self.color]]

class BlockMountain(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        if self.turn_count % 4 == 0:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color]]
        elif self.turn_count % 4 == 1:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x - 1, self.center.y, self.color]]
        elif self.turn_count % 4 == 2:
            return [[self.center.x, self.center.y, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color]]
        elif self.turn_count % 4 == 3:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x + 1, self.center.y, self.color]]

class BlockSeven(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        if self.turn_count % 4 == 0:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x - 1, self.center.y - 1, self.color], [self.center.x, self.center.y + 1, self.color]]
        elif self.turn_count % 4 == 1:
            return [[self.center.x, self.center.y, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x - 1, self.center.y + 1, self.color]]
        elif self.turn_count % 4 == 2:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x + 1, self.center.y + 1, self.color], [self.center.x, self.center.y - 1, self.color]]
        elif self.turn_count % 4 == 3:
            return [[self.center.x, self.center.y, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x + 1, self.center.y - 1, self.color]]

class BlockSevenR(Block):
    def __init__(self) -> None:
        super().__init__()

    @property
    def cubes(self) -> List[List[int]]:
        if self.turn_count % 4 == 0:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x + 1, self.center.y - 1, self.color]]
        elif self.turn_count % 4 == 1:
            return [[self.center.x, self.center.y, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x - 1, self.center.y - 1, self.color]]
        elif self.turn_count % 4 == 2:
            return [[self.center.x, self.center.y, self.color], [self.center.x, self.center.y + 1, self.color], [self.center.x, self.center.y - 1, self.color], [self.center.x - 1, self.center.y + 1, self.color]]
        elif self.turn_count % 4 == 3:
            return [[self.center.x, self.center.y, self.color], [self.center.x - 1, self.center.y, self.color], [self.center.x + 1, self.center.y, self.color], [self.center.x + 1, self.center.y + 1, self.color]]


block_list = [BlockBar, BlockRect, BlockZ, BlockZR, BlockMountain, BlockSeven, BlockSevenR]


class Tetris:
    def __init__(self) -> None:
        self.map: List[List[int]] = []
        self.total_score: int = 0
        self.blockQueue: List[Block] = []
        self.currentBlock: Block = random.choice(block_list)()

        for i in range(25):
            self.map.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def tick(self, command) -> int:
        feedback = None
        if command is not -1:
            feedback = self.currentBlock.move(command, self.map)
        score = 0
        _map = copy.deepcopy(self.map)
        for cube in self.currentBlock.cubes:
            _map[cube[1]][cube[0]] = cube[2]

        if feedback is not None and feedback.value == MoveFeedback.STACKED.value:
            for cube in self.currentBlock.cubes:
                self.map[cube[1]][cube[0]] = cube[2]
                self.currentBlock = random.choice(block_list)()

            for i in range(25):
                while all(cube > 0 for cube in self.map[i]):
                    self.map.pop(i)
                    self.map.insert(0, [0] * 10)
                    score += 1
            
            if not all(self.map[3][i] == 0 for i in range(0, 10)):
                self.map.clear()
                for i in range(25):
                    self.map.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                score = -100
        return score, _map