# agent.py
import random


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept.get('agent_pos')
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """A simple reflex agent that acts only on current percepts using IF-THEN rules."""

    def sense_and_act(self, percept: dict) -> str:
        # Rule 1: If food is here, collect it
        if percept.get('food_here'):
            return 'Suck'   # You can treat 'Suck' as a placeholder action

        # Rule 2: If wall ahead, turn left
        elif percept.get('wall_ahead'):
            return 'Left'

        # Rule 3: If toxin here, move away (basic avoidance)
        elif percept.get('toxin_here'):
            return 'Right'

        # Rule 4: Default action: move forward
        else:
            return 'Up'



'''
class ModelBasedAgent:
    def __init__(self):
        self.visited_cells = set()
        self.last_action = None

    def sense_and_act(self, percept: dict, agent_pos: tuple) -> str:
        # Update memory: mark current cell as visited
        self.visited_cells.add(agent_pos)

        # Rule 1: If food is here, collect
        if percept.get('food_here'):
            self.last_action = 'Suck'
            return 'Suck'

        # Rule 2: If there is a wall ahead, try to turn left or right (prefer a move that doesn't head back)
        elif percept.get('wall_ahead') and (agent_pos[0]-1, agent_pos[1]) in self.visited_cells:
            self.last_action = 'Right'
            return 'Right'

        elif percept.get('wall_ahead'):
            left_cell = (agent_pos[0]-1, agent_pos[1])
            right_cell = (agent_pos[0]+1, agent_pos[1])

            # 1. If left was visited, prefer turning right to explore new ground
            if left_cell in self.visited_cells and right_cell not in self.visited_cells:
                action = 'Right'
            # 2. If right was visited, prefer turning left to explore new ground
            elif right_cell in self.visited_cells and left_cell not in self.visited_cells:
                action = 'Left'
            # Fallback: If neither are visited, default to a turn
            else: 
                action = 'Left'

            self.last_action = action
            return action

        # RUle 3: If there is a toxin ahead, move away (basic avoidance)
        elif percept.get('toxin_here'):
            self.last_action = 'Right'
            return 'Right'

        # Rule 4: If opponent here, move away
        elif percept.get('opponent_here'):
            self.last_action = 'Down'
            return 'Down'

        # Rule 5: Default move forward 
        else:
            self.last_action = 'Up'
            return 'Up'  
'''


class ModelBasedAgent:
    def __init__(self, width=12, height=12):
        self.visited_cells = set()
        self.last_action = None
        self.width = width
        self.height = height

    def sense_and_act(self, percept: dict, agent_pos: tuple) -> str:
        # 1. Update Memory State
        self.visited_cells.add(agent_pos)

        # Rule 1: If standing on food, collect it
        if percept.get('food_here'):
            self.last_action = 'Suck'
            return 'Suck'

        # 2. Compute Absolute Grid Coordinates of 4 Neighbors
        x, y = agent_pos
        up_cell    = (x, y + 1)
        down_cell  = (x, y - 1)
        left_cell  = (x - 1, y)
        right_cell = (x + 1, y)

        # Validity checks including grid boundaries and walls
        is_left_valid  = (x - 1 >= 0) and not percept.get('wall_left')
        is_right_valid = (x + 1 < self.width) and not percept.get('wall_right')
        is_up_valid    = (y + 1 < self.height) and not percept.get('wall_up')
        is_down_valid  = (y - 1 >= 0) and not percept.get('wall_down')

        # 3. Collect all valid unvisited moves
        unvisited_moves = []
        if is_left_valid and left_cell not in self.visited_cells:
            unvisited_moves.append('Left')
        if is_right_valid and right_cell not in self.visited_cells:
            unvisited_moves.append('Right')
        if is_up_valid and up_cell not in self.visited_cells:
            unvisited_moves.append('Up')
        if is_down_valid and down_cell not in self.visited_cells:
            unvisited_moves.append('Down')

        if unvisited_moves:
            action = random.choice(unvisited_moves)
        else:
            # Fallback: If all surrounding valid cells have been visited, pick randomly from any valid direction
            valid_moves = []
            if is_left_valid:  valid_moves.append('Left')
            if is_right_valid: valid_moves.append('Right')
            if is_up_valid:    valid_moves.append('Up')
            if is_down_valid:  valid_moves.append('Down')

            action = random.choice(valid_moves) if valid_moves else 'Up'

        self.last_action = action
        return action

        
