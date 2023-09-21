import os

class InputHandler:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_input(prompt):
        return input(prompt)

    @staticmethod
    def get_integer_input(prompt, min, max):
        while True:
            user_input = InputHandler.get_input(prompt)
            try:
                value = int(user_input)
                if min <= value <= max:
                    return value
                else:
                    print(prompt)
            except ValueError:
                print("Veuillez entrer un entier valide.")
