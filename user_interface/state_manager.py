from time import time
import pygame
import sys


class GameStateManager:
    def __init__(self, state_function: callable, state_number = time()):
        self._states = {state_number: state_function}
        self._current_state = state_number

    def add_state(self, state_number: float, state_function: callable):
        """Registers a new state and its update function."""
        if state_number in self._states:
            raise ValueError(f"State '{state_number}' already exists!")
        self._states[state_number] = state_function

    def set_state(self, new_state: float):
        """Changes to a new state (if it exists)."""
        if new_state not in self._states:
            raise ValueError(f"State '{new_state}' not registered!")
        self._current_state = new_state

    def set_timed_state(self, state_function: callable):
        """Adds a new state using a timestamp as its key and sets it as the current state."""
        state_id = time()
        self.add_state(state_id, state_function)
        self.set_state(state_id)

    def update(self):
        """Executes the logic of the current state."""
        if self._states:
            self._states[self._current_state]()
        else:
            print("No current state to update!")
            pygame.quit()
            sys.exit()

    def return_to_previous_state(self):
        """
        Remove the highest key from the game_classes states dictionary and
        set the current state to the highest key
        """
        self._states.pop(max(self._states.keys()))
        if self._states:
            self._current_state = max(self._states.keys())

    def return_to_initial_state(self):
        """
        Keeps only the first (oldest) added state in the state dictionary,
        removing all others. Sets the current state to that main (initial) state.
        """
        if self._states:
            min_key = min(self._states.keys())
            self._states = {min_key: self._states[min_key]}
            self._current_state = min_key
