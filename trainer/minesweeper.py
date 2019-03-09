from enum import IntEnum
import collections
import random
import sys

Move = collections.namedtuple('Move', 'action x y')


class MoveResult(IntEnum):
    GAME_LOSS = -99
    INVALID_MOVE = -99
    NORMAL_MOVE = 1
    GAME_WIN = 50


class MineHitException(Exception):
    pass


class Game:
    def __init__(self, grid_size=3, mine_count=3):
        sys.setrecursionlimit(10000)
        self.grid = Grid(grid_size, mine_count)
        self.score = 0
        self.round_number = 0
        self.grid.generate_mines()
        self.grid.update_number_neigboring_mines()

    def run_game(self):
        while True:
            self.run_round()

    def run_round(self):
        self.round_number += 1
        next_move = self.user_input()
        self.run_move(next_move)

        print("Round number:", self.round_number)

    def run_move(self, move):
        cell = self.grid.matrix[move.x][move.y]
        if cell.revealed is True:
            return MoveResult.INVALID_MOVE

        try:
            self.grid.reveal_cell(move.x, move.y)
        except MineHitException:
            self.end_of_game(won=False)
            return MoveResult.GAME_LOSS

        # Update score
        revealed_cells_count = self.grid.calculate_number_cells_revealed()
        self.score = revealed_cells_count

        if revealed_cells_count >= self.grid.revealable_cell_count:
            self.end_of_game(won=True)
            return MoveResult.GAME_WIN

        return MoveResult.NORMAL_MOVE

    def user_input(self):
        x = int(input("Enter x value"))
        y = int(input("Enter y value"))
        return Move(action='flag', x=x, y=y)

    def end_of_game(self, won=False):
        return
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if won:
            print("You win!!!! , your score is:")
        else:
            print("Game has ended because you revealed a mine, your score is:")
        print(self.score)


class Grid:
    def __init__(self, size, mine_count):
        self.width = size
        self.height = size
        self.mine_count = mine_count
        self.cell_count = self.width * self.height
        self.revealed_cell_count = 0
        self.revealable_cell_count = self.cell_count - self.mine_count
        self.matrix = [[Cell() for x in range(self.width)]
                       for y in range(self.height)]

    def show_grid(self):
        print("  ", end="")
        for y in range(0, self.height):  # add numbers to the rows
            print("")
            for x in range(0, self.width):
                print("|", end="")
                self.matrix[x][y].output_cell_value()
            print("|", end="")
        print("")

    def generate_mines(self):
        mine_added_count = 0
        while (mine_added_count < self.mine_count):
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if not self.matrix[x][y].mine:
                self.matrix[x][y].mine = True
                mine_added_count += 1

    def update_number_neigboring_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if (self.matrix[x][y].mine):
                    pass
                else:
                    self.matrix[x][y].neighboring_mines_count = self.calculate_number_of_mines_in_neighborhood(x, y)

    def reveal_cell(self, x, y):
        cell = self.matrix[x][y]
        cell.revealed = True

        if cell.mine:
            raise MineHitException

        # If not empty, stop searching
        if not cell.neighboring_mines_count == 0:
            return

        for yi in range(y - 1, y + 2):
            for xi in range(x - 1, x + 2):
                # Don't search outside of grid
                if xi < 0 or yi < 0 or xi >= self.width or yi >= self.height:
                    continue
                # Recurse!
                if not self.matrix[xi][yi].revealed:
                    self.reveal_cell(xi, yi)

    def calculate_number_of_mines_in_neighborhood(self, x, y):
        numberofneighbors = 0

        # take it into consideration that the start of the array is at 0, so
        # x=1,y=1 is the item in the second column and the second row.
        for yi in range(y - 1, y + 2):
            for xi in range(x - 1, x + 2):

                # if outside of range (@borders of grid) don't check just
                # continue
                if xi < 0 or yi < 0 or xi >= self.width or yi >= self.height:
                    continue
                else:  # if within range then check if neighbors cells contain checkvalue and increment the number of total neighbors
                    if self.matrix[xi][yi].mine:
                        numberofneighbors += 1
        return numberofneighbors

    def check_if_mine_is_revealed(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[x][y].mine and self.matrix[x][y].revealed:
                    return True
        return False

    def calculate_number_cells_revealed(self):
        # is het beter om lokaal een nieuwe variabele aan te maken of gewoon
        # deze even op 0 te zetten?
        revealed_cell_count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[x][y].revealed:
                    revealed_cell_count += 1
        return revealed_cell_count


class Cell:
    def __init__(self):
        self.mine = False
        self.revealed = False
        self.neighboring_mines_count = 0

    def output_cell_value(self):
        if not self.revealed:
            print("*", end="")
            return

        if self.mine:
            print("x", end="")
        else:
            print(self.neighboring_mines_count, end="")

    def numerical_value(self):
        if not self.revealed:
            return -1
        else:
            return self.neighboring_mines_count

    def add_number_neighboring_mines(self, numberofneighborsmines):
        self.neighboring_mines_count = numberofneighborsmines


def main():

    print("Main starts...")

    game1 = Game()
    game1.run_game()
    print("The end...")


if __name__ == "__main__":
    main()
