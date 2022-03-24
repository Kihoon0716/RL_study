

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