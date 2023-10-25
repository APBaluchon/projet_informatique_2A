from business_layer.controler.view import View


class DBView(View):
    def press_enter(self):
        return super().get_input("Appuyez sur la touche entréee pour revenir au menu")

    def ask_pseudo(self):
        return super().get_input("Pseudo : ")

    def ask_modality(self):
        possibilities_dict = {
            "1" : "Password",
            "2" : "Rôle"
        }
        return super().get_list_input("Choisissez le type de modification : ", possibilities_dict.values())

    def ask_new_password(self):
        return super().get_input("Entrez le nouveau mot de passe : ", "password")

    def wrong_password(self):
        return print("Le pseudo n'est pas dans la base de données.")

    def ask_password_new_account(self):
        return super().get_input("Entrez un mot de passe pour créer un compte : ", "password")