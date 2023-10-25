import os
from InquirerPy import prompt


class View:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_input(self, message, type_message = "input"):
        questions = [
            {"type" : type_message,
             "message" : message,
             "name" : "resultat"}
        ]

        result = prompt(questions)
        return result["resultat"]

    def get_list_input(self, message, list_values):
        questions = [{
            "type" : "list",
            "message" : message,
            "choices" : list_values,
            "name" : "resultat"
        }]

        result = prompt(questions)["resultat"]
        return result
