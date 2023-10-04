import os
from InquirerPy import prompt
from InquirerPy.validator import NumberValidator


class InputHandler:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_input(message, type_message = "input"):
        questions = [
            {"type" : type_message,
             "message" : message,
             "name" : "resultat"}
        ]

        result = prompt(questions)
        return result["resultat"]

    @staticmethod
    def get_list_input(message, list_values):
        questions = [{
            "type" : "list",
            "message" : message,
            "choices" : list_values,
            "name" : "resultat"
        }]

        result = prompt(questions)["resultat"]
        return result

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
