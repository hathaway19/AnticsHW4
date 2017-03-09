  # -*- coding: latin-1 -*-
import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer, self).__init__(inputPlayerId, "geneticsAI")
    
    ##
    #getPlacement
    #
    #Description: The getPlacement method corresponds to the 
    #action taken on setup phase 1 and setup phase 2 of the game. 
    #In setup phase 1, the AI player will be passed a copy of the 
    #state as currentState which contains the board, accessed via 
    #currentState.board. The player will then return a list of 11 tuple 
    #coordinates (from their side of the board) that represent Locations 
    #to place the anthill and 9 grass pieces. In setup phase 2, the player 
    #will again be passed the state and needs to return a list of 2 tuple
    #coordinates (on their opponent's side of the board) which represent
    #Locations to place the food sources. This is all that is necessary to 
    #complete the setup phases.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is 
    #       requesting a placement from the player.(GameState)
    #
    #Return: If setup phase 1: list of eleven 2-tuples of ints -> [(x1,y1), (x2,y2),…,(x10,y10)]
    #       If setup phase 2: list of two 2-tuples of ints -> [(x1,y1), (x2,y2)]
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        # implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:  # stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    # Choose any x location
                    x = random.randint(0, 9)
                    # Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:  # stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    # Choose any x location
                    x = random.randint(0, 9)
                    # Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: The getMove method corresponds to the play phase of the game 
    #and requests from the player a Move object. All types are symbolic 
    #constants which can be referred to in Constants.py. The move object has a 
    #field for type (moveType) as well as field for relevant coordinate 
    #information (coordList). If for instance the player wishes to move an ant, 
    #they simply return a Move object where the type field is the MOVE_ANT constant 
    #and the coordList contains a listing of valid locations starting with an Ant 
    #and containing only unoccupied spaces thereafter. A build is similar to a move 
    #except the type is set as BUILD, a buildType is given, and a single coordinate 
    #is in the list representing the build location. For an end turn, no coordinates 
    #are necessary, just set the type as END and return.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is 
    #       requesting a move from the player.(GameState)   
    #
    #Return: Move(moveType [int], coordList [list of 2-tuples of ints], buildType [int]
    ##
    def getMove(self, currentState):
        return None
    
    ##
    #getAttack
    #Description: The getAttack method is called on the player whenever an ant completes 
    #a move and has a valid attack. It is assumed that an attack will always be made 
    #because there is no strategic advantage from withholding an attack. The AIPlayer 
    #is passed a copy of the state which again contains the board and also a clone of 
    #the attacking ant. The player is also passed a list of coordinate tuples which 
    #represent valid locations for attack. Hint: a random AI can simply return one of 
    #these coordinates for a valid attack. 
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is requesting 
    #       a move from the player. (GameState)
    #   attackingAnt - A clone of the ant currently making the attack. (Ant)
    #   enemyLocation - A list of coordinate locations for valid attacks (i.e. 
    #       enemies within range) ([list of 2-tuples of ints])
    #
    #Return: A coordinate that matches one of the entries of enemyLocations. ((int,int))
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        # Attack a random enemy.
        return enemyLocations[0]
        
    ##
    #registerWin
    #Description: The last method, registerWin, is called when the game ends and simply 
    #indicates to the AI whether it has won or lost the game. This is to help with 
    #learning algorithms to develop more successful strategies.
    #
    #Parameters:
    #   hasWon - True if the player has won the game, False if the player lost. (Boolean)
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

    ##
    # evaluate_state
    #
    # Evaluates and scores a GameState Object
    #
    # Parameters
    #   state - the GameState object to evaluate
    #
    # Return
    #   a double between 0 and 1 inclusive
    ##
    def evaluate_state(self, state):
        # The AI's player ID
        me = state.whoseTurn
        # The opponent's ID
        enemy = (state.whoseTurn + 1) % 2

        # Get a reference to the player's inventory
        my_inv = state.inventories[me]
        # Get a reference to the enemy player's inventory
        enemy_inv = state.inventories[enemy]

        # Gets both the player's queens
        my_queen = getAntList(state, me, (QUEEN,))
        enemy_queen = getAntList(state, enemy, (QUEEN,))

        # Sees if winning or loosing conditions are already met
        if (my_inv.foodCount == 11) or (enemy_queen is None):
            return 1.0
        if (enemy_inv.foodCount == 11) or (my_queen is None):
            return 0.0

        #the starting value, not winning or losing
        eval = 0.0

        #important number
        worker_count = 0
        drone_count = 0

        food_coords = []
        enemy_food_coords = []

        foods = getConstrList(state, None, (FOOD,))

        # Gets a list of all of the food coords
        for food in foods:
            if food.coords[1] < 5:
                food_coords.append(food.coords)
            else:
                enemy_food_coords.append(food.coords)

        #coordinates of this AI's tunnel
        tunnel = my_inv.getTunnels()
        t_coords = tunnel[0].coords

        #coordinates of this AI's anthill
        ah_coords = my_inv.getAnthill().coords

        #A list that stores the evaluations of each worker
        wEval = []

        #A list that stores the evaluations of each drone, if they exist
        dEval = []

        #queen evaluation
        qEval = 0

        #iterates through ants and scores positioning
        for ant in my_inv.ants:

            #scores queen
            if ant.type == QUEEN:

                qEval = 50.0

                #if queen is on anthill, tunnel, or food it's bad
                if ant.coords == ah_coords or ant.coords == t_coords or ant.coords == food_coords[0] or ant.coords == food_coords[1]:
                    qEval -= 10

                #if queen is out of rows 0 or 1 it's bad
                if ant.coords[0] > 1:
                    qEval -= 10

                # the father from enemy ants, the better
                qEval -= 2 * self.get_closest_enemy_dist(ant.coords, enemy_inv.ants)

            #scores worker to incentivize food gathering
            elif ant.type == WORKER:

                #tallies up workers
                worker_count += 1

                #if carrying, the closer to the anthill or tunnel, the better
                if ant.carrying:

                    wEval.append(100.0)

                    #distance to anthill
                    ah_dist = approxDist(ant.coords, ah_coords)

                    #distance to tunnel
                    t_dist = approxDist(ant.coords, t_coords)

                    #finds closest and scores
                    #if ant.coords == ah_coords or ant.coords == t_coords:
                        #print("PHill")
                        #eval += 100000000
                    if t_dist < ah_dist:
                        wEval[worker_count - 1] -= 5 * t_dist
                    else:
                        wEval[worker_count - 1] -= 5 * ah_dist

                #if not carrying, the closer to food, the better
                else:

                    wEval.append(80.0)

                    #distance to foods
                    f1_dist = approxDist(ant.coords, food_coords[0])
                    f2_dist = approxDist(ant.coords, food_coords[1])

                    #finds closest and scores
                    #if ant.coords == food_coords[0] or ant.coords == food_coords[1]:
                        #print("PFood")
                        #eval += 500

                    if f1_dist < f2_dist:
                        wEval[worker_count - 1] -= 5 * f1_dist
                    else:
                        wEval[worker_count - 1] -= 5 * f2_dist

                #the father from enemy ants, the better
                #eval += -5 + self.get_closest_enemy_dist(ant.coords, enemy_inv.ants)

            #scores soldiers to incentivize the disruption of the enemy economy
            else:

                #tallies up soldiers
                drone_count += 1

                dEval.append(50.0)

                nearest_enemy_worker_dist = self.get_closest_enemy_worker_dist(ant.coords, enemy_inv.ants)

                #if there is an enemy worker
                if not nearest_enemy_worker_dist == 100:
                     dEval[drone_count - 1] -= 5 * nearest_enemy_worker_dist

                #if there isn't an enemy worker, go to the food
                else:
                    dEval[drone_count - 1] -= 5 * self.get_closest_enemy_food_dist(ant.coords, enemy_food_coords)

        #scores other important things

        #state eval
        sEval = 0

        #assesses worker inventory
        if worker_count == 2:
            sEval += 50
        elif worker_count < 2:
            sEval -= 10
        elif worker_count > 2:
            eval_num = 0.00001
            return eval_num

        #assesses drone inventory
        if drone_count == 2:
            sEval += 50
        elif drone_count < 2:
            sEval -= 10
        elif drone_count > 2:
            eval_num = 0.00001
            return eval_num

        #assesses food
        if not sEval == 0:
            sEval += 20 * my_inv.foodCount

        #a temporary variable
        temp = 0

        #scores workers
        for val in wEval:
            temp += val
        if worker_count == 0:
            wEvalAv = 0
        else:
            wEvalAv = temp/worker_count

        temp = 0

        #scores drones
        for val in dEval:
            temp += val

        if not drone_count == 0:
            dEvalAv = temp/drone_count
        else:
            dEvalAv = 0

        #total possible score
        total_possible = 100.0 + 50.0 + 50.0 + 300.0

        #scores total evaluation and returns
        eval = (qEval + wEvalAv + dEvalAv + sEval)/ total_possible
        if eval <= 0:
            eval = 0.00002

        return eval