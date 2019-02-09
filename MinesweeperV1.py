
# make limiter on number of mines in field (now number of mines can exceed field cells)
# Add function flagged cleam main
# check all variable names

import random
import sys


class Game:
    def __init__(self):
        #The cell value is (0 for nothing, 1-8 for #neighboring mines count)
        self.gridplayed= Grid()
        self.game_end = False
        self.nextmove_x = 0
        self.nextmove_y = 0
        self.nextmove_action = 'f'  	# 'f' flag or 'r' reveal
        self.score = 0
        self.round_number = 0

    def set_grid_total_revealed(self):
        self.gridplayed.add_mines()

    def set_grid_played(self):
        self.gridplayed.calculate_number_neigboring_mines()

    def ask_user_input_coordinates_and_action(self):
        # user sends x,y coordinates + action reveal or action flag
        pass

    def run_game(self):
        self.set_grid_total_revealed()
        self.set_grid_played()
        self.gridplayed.show_grid()
        while not self.game_end:
            self.run_round()

    def run_round(self):
        self.round_number += 1
        self.user_input()
        self.gridplayed.unveil_cell(self.nextmove_x, self.nextmove_y)
        self.gridplayed.check_if_cells_need_to_be_revealed()
        self.check_end_of_game()
        print("Round number:", self.round_number)
        self.gridplayed.show_grid()

    def user_input(self):
        self.nextmove_x = int(input("Enter x value"))
        self.nextmove_y = int(input("Enter y value"))
        # input("Enter action value f(flag), r(reveal)")
        self.nextmove_action = 'f'

    def check_end_of_game(self):
        # check if mine is revealed if so game ends
        if(self.gridplayed.check_if_mine_is_revealed()):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Game has ended because you revealed a mine, your score is:")
            print(self.score)
            sys.exit()
        else:
            # check if all revealable cells are revealed
            self.gridplayed.calculate_number_cells_revealed()
            self.score = self.gridplayed.numberofrevealedcells
            if(self.gridplayed.numberofrevealedcells == self.gridplayed.total_revealablecells):
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("You win!!!! , your score is:")
                print(self.score)
                sys.exit()


class Grid:
    def __init__(self):
        self.gridwidth = 10
        self.gridheight = 10
        self.numberofmines = 10
        self.numberofrevealedcells = 0
        self.numberofcells = self.gridwidth * self.gridheight
        self.total_revealablecells = self.numberofcells - self.numberofmines
        # Makes a list containing number of <gridheight> lists, each of number
        # of <gridwidth> items. All items == cell instance
        self.matrix = [[Cell() for x in range(self.gridwidth)]
                       for y in range(self.gridheight)]

    def show_grid(self):
        print("  ", end="")
        for i in range(0, self.gridheight):  # add numbers to coloms
            print("|", end="")
            print(i, end="")
        print("|", end="")
        for y in range(0, self.gridheight):  # add numbers to the rows
            print("")
            print(y, end="")
            print("|", end="")
            for x in range(0, self.gridwidth):
                print("|", end="")
                self.matrix[x][y].output_cell_value()
            print("|", end="")
        print("")

    def add_mines(self):
        numberofminesadded = 0
        while (numberofminesadded < self.numberofmines):
            y = random.randint(0, self.gridheight - 1)
            x = random.randint(0, self.gridwidth - 1)
            if not self.matrix[x][y].mine:
                self.matrix[x][y].add_mine()
                numberofminesadded += 1

    def calculate_number_neigboring_mines(self):
        for y in range(self.gridheight):
            for x in range(self.gridwidth):
                if (self.matrix[x][y].check_if_cell_contains('mine')):
                    pass
                else:
                    self.matrix[x][y].add_number_neighboring_mines(
                        self.calculate_number_in_neighborhood(x, y, 'mine'))

    def check_if_cells_need_to_be_revealed(self):
        for i in range(0, 5):
            for y in range(self.gridheight):
                for x in range(self.gridwidth):
                    if (self.matrix[x][y].check_if_cell_contains('0') and self.matrix[x][y].revealed):
                        self.reveal_all_cells_around(x, y)
                    else:
                        pass

    def reveal_all_cells_around(self, x, y):
        for yi in range(y - 1, y + 2):
            for xi in range(x - 1, x + 2):

                # if outside of range (@borders of grid) don't check just
                # continue
                if(xi < 0 or yi < 0 or xi >= self.gridwidth or yi >= self.gridheight):
                    continue
                else:  # if within range then check if neighbors cells contain checkvalue and increment the number of total neighbors
                    self.matrix[xi][yi].reveal_cell()

    def unveil_cell(self, x, y):
        self.matrix[x][y].reveal_cell()

    def calculate_number_in_neighborhood(self, x, y, checkvalue):
        numberofneighbors = 0

        # take it into consideration that the start of the array is at 0, so
        # x=1,y=1 is the item in the second column and the second row.
        for yi in range(y - 1, y + 2):
            for xi in range(x - 1, x + 2):

                # if outside of range (@borders of grid) don't check just
                # continue
                if(xi < 0 or yi < 0 or xi >= self.gridwidth or yi >= self.gridheight):
                    continue
                else:  # if within range then check if neighbors cells contain checkvalue and increment the number of total neighbors
                    if (self.matrix[xi][yi].check_if_cell_contains(checkvalue)):
                        numberofneighbors += 1
        return numberofneighbors

    def check_if_mine_is_revealed(self):
        for y in range(self.gridheight):
            for x in range(self.gridwidth):
                if(self.matrix[x][y].check_if_cell_contains('mine') and self.matrix[x][y].revealed):
                    return True
        return False

    def calculate_number_cells_revealed(self):
        # is het beter om lokaal een nieuwe variabele aan te maken of gewoon
        # deze even op 0 te zetten?
        self.numberofrevealedcells = 0
        for y in range(self.gridheight):
            for x in range(self.gridwidth):
                if(self.matrix[x][y].revealed):
                    self.numberofrevealedcells += 1


class Cell:
    def __init__(self):
        self.mine = False
        self.revealed = False
        self.neighboring_mines_count = 0

    def add_mine(self):
        self.mine = True

    def reveal_cell(self):
        self.revealed = True

    def hide_cell(self):
        print("*", end="")

    def show_cell(self):
        if self.mine:
            print("x", end="")
        else:
            print(self.neighboring_mines_count, end="")

        # hier is een voorbeeld van een functie die andere functies in zelfde
        # level aanroept (nested structuur). Is dat good practice of juist
        # niet?
    def output_cell_value(self):
        if self.revealed:
            self.show_cell()
        else:
            self.hide_cell()

    def check_if_cell_contains(self, checkvalue):
        if (checkvalue == 'mine'):
            if self.mine:
                return True
            else:
                return False
        if (checkvalue == '0'):
            if self.neighboring_mines_count == 0 and not self.mine:
                return True
            else:
                return False

        # is dit de nette manier of juist de omslachtige manier om
        # numberofneigbhborsmines te updaten?
    def add_number_neighboring_mines(self, numberofneighborsmines):
        self.neighboring_mines_count = numberofneighborsmines


def main():

    print("Main starts...")

    game1 = Game()
    game1.run_game()
    print("The end...")


if __name__ == "__main__":
    main()
