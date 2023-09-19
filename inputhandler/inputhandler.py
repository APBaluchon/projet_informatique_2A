import os

class InputHandler:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_input(prompt):
        return input(prompt)