from view.view import View


class AdminView(View):
    actions_dict = {
            "1": "Consulter la base de données",
            "2": "Modifier les informations d'un utilisateur de la base de données",
            "3": "Supprimer un utilisateur de la base de données",
            "4": "Ajouter des informations à la base de données des parties",
            "5": "Quitter l'application"
    }
    choix_dict = {
        "1" : "Ajouter un joueur en particulier",
        "2" : "Ajouter les joueurs d'un rang"
    }
    tier_dict = {
        "1" : "Fer",
        "2" : "Bronze",
        "3" : "Argent",
        "4" : "Or",
        "5" : "Platinium",
        "6" : "Emeraude",
        "7" : "Diamant"
    }

    def ask_action(self):
        return super().get_list_input("Choissiez l'action : ", AdminView().choix_dict.values())

    def ask_pseudo_to_add(self):
        return super().get_input("Entrez le pseudo du joueur à ajouter : ")
    
    def ask_tier_to_add(self):
        return super().get_list_input("Choisissez le rang : ", AdminView().tier_dict.values())
    
    def ask_choice(self):
        return super().get_list_input("Selectionnez l'action : ", AdminView().actions_dict.values())
