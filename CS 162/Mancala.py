# Author: Sterling Violette
# GitHub username: Sterlinghv
# Date: 11/26/2022
# Description: A program that allows 2 players to play the game of mancala.
#              Player class stores the player object, and the mancala
#              class stores the mancala object, or the game if you will.
#              The mancala class has various method for playing the game,
#              and determining the winner.

class Player:
    """
    Class that defines the player object.
    """
    instances = []

    def __init__(self, name):
        """
        Prepares the player object.
        """
        self._name = name
        self.__class__.instances.append(self)

    def get_name(self):
        """
        Returns the players name based on the passed in num
        """
        return self._name

class Mancala:
    """
    The mancala game class object. Represents the game of mancala
    in its entirety as an object.
    """

    def __init__(self):
        """
        Prepares the mancala object
        """
        self._game_set = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self._winner_flag = 0

    def create_player(self, name):
        """
        Method that creates a player object
        based upon a passed in player name.
        """
        return Player(name)

    def play_game(self, player, pit_index):
        """
        The method to actually play the game, takes a player index 1 or 2,
        and a pit index, 1-6. Houses the logic of the game, returns the
        state of the array holding the pits and stores.
        """
        if self._winner_flag != 0:
            return "Game is ended"

        #if they input an invalid index
        if player == 1:
            if pit_index < 1 or pit_index > 6:
                return "Invalid number for pit index"

            #configure index matches for player 1
            if pit_index:
                real_pit_index = pit_index - 1

        if player == 2:
            if pit_index < 1 or pit_index > 6:
                return "Invalid number for pit index"

            #configure index matches for player 2
            if pit_index:
                real_pit_index = pit_index + 6

        #if they choose an empty pit
        if self._game_set[real_pit_index] == 0:
            print("This pit is empty, current player, take another turn!")
            return self._game_set

        #else we start the game
        else:
            seed_count = self._game_set[real_pit_index] #the count of seeds in the indexed pit
            seed_count_copy = seed_count #used for tracking the amount of seeds to disperse in pits
            next_pit_index = (real_pit_index + 1) #the next pit index to start adding seeds
            self._game_set[real_pit_index] = 0 #turn the selected pit into 0 (seeds have been picked up)

            if player == 1:
                #start adding seeds to pits
                for seed in range(seed_count):

                    #if the next pit to add seeds is player 2's store, reset to first player 1 index
                    if next_pit_index == 13:
                        next_pit_index = 0

                    if next_pit_index >= len(self._game_set):
                        next_pit_index = 0

                    #correspond opposite side pits
                    other_player_index = 12 - next_pit_index

                    steal_flag = 0
                    #if the player can steal seeds
                    if seed_count_copy == 1 and self._game_set[next_pit_index] == 0 and next_pit_index != 6 and self._game_set[other_player_index] > 0:
                        seeds_to_steal = self._game_set[other_player_index] + 1
                        self._game_set[6] += seeds_to_steal
                        self._game_set[other_player_index] = 0
                        steal_flag = 1

                    #if the last seed lands in player 1's store, they take a bonus turn
                    if seed_count_copy == 1 and next_pit_index == 6:
                        self._game_set[next_pit_index] += 1
                        print("player 1 take another turn")
                        return self._game_set

                    #add a seed to the pit, up the next pit index to next pit
                    if steal_flag == 0:
                        self._game_set[next_pit_index] += 1

                    seed_count_copy -= 1
                    next_pit_index += 1

            if player == 2:
                # start adding seeds to pits
                for seed in range(seed_count):

                    # if the next pit to add seeds is player 1's store, reset to first player 2 index
                    if next_pit_index == 6:
                        next_pit_index = 7

                    if next_pit_index >= len(self._game_set):
                        next_pit_index = 0

                    # correspond opposite side pits
                    other_player_index = 12 - next_pit_index

                    steal_flag = 0
                    # if the player can steal seeds
                    if seed_count_copy == 1 and self._game_set[next_pit_index] == 0 and next_pit_index != 13 and self._game_set[other_player_index] > 0:
                        seeds_to_steal = self._game_set[other_player_index] + 1
                        self._game_set[13] += seeds_to_steal
                        self._game_set[other_player_index] = 0
                        steal_flag = 1

                    #if the last seed lands in player 2's store, they take a bonus turn
                    if seed_count_copy == 1 and next_pit_index == 13:
                        self._game_set[next_pit_index] += 1
                        print("player 2 take another turn")
                        return self._game_set

                    # add a seed to the pit, up the next pit index to next pit
                    if steal_flag == 0:
                        self._game_set[next_pit_index] += 1
                    seed_count_copy -= 1
                    next_pit_index += 1

            pit_sum_1 = 0
            pit_sum_2 = 0
            for i in range(0, 6):
                pit_sum_1 += self._game_set[i]
            for i in range(7, 13):
                pit_sum_2 += self._game_set[i]
            if pit_sum_1 == 0 or pit_sum_2 == 0:
                self._game_set[6] += pit_sum_1
                self._game_set[13] += pit_sum_2
                for i in range(0, 6):
                    self._game_set[i] = 0
                for i in range(7, 13):
                    self._game_set[i] = 0
                if self._game_set[6] > self._game_set[13]:
                    self._winner_flag = 1
                if self._game_set[6] < self._game_set[13]:
                    self._winner_flag = 2
                if self._game_set[6] == self._game_set[13]:
                    self._winner_flag = 3
                self.return_winner()
        return self._game_set

    def print_board(self):
        """
        method to return the current state of the board. Returns
        number of seeds in both players store, and seeds in pit
        1 - 6.
        """
        player_1_store = self._game_set[6]
        player_2_store = self._game_set[13]

        indexes = [0, 1, 2, 3, 4, 5]
        player_1_set = [self._game_set[x] for x in indexes]
        indexes = [7, 8, 9, 10, 11, 12]
        player_2_set = [self._game_set[x] for x in indexes]

        print("player1:", "\nstore:", player_1_store, "\nPits:", player_1_set,)
        print("player2:", "\nstore:", player_2_store, "\nPits:", player_2_set,)

    def return_winner(self):
        """
        Method that will be called to determine the output of a winner
        """
        if self._winner_flag == 0:
            return "Game has not ended"
        if self._winner_flag == 1:
            return "Winner is player 1: " + Player.get_name(Player.instances[0])
        if self._winner_flag == 2:
            return "Winner is player 2: " + Player.get_name(Player.instances[1])
        if self._winner_flag == 3:
            return "It's a tie"


"""
Sample game usage

game = Mancala()
player1 = game.create_player("Lily")
player2 = game.create_player("Lucy")
print(game.play_game(1, 3))
game.play_game(1, 1)
game.play_game(2, 3)
game.play_game(2, 4)
game.play_game(1, 2)
game.play_game(2, 2)
game.play_game(1, 1)
game.print_board()
print(game.return_winner())
"""