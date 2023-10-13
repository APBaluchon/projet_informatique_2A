from view.view import View


class UserView(View):
    actions_dict = {
        "1" : "Analyser un poste",
        "2" : "Quitter l'application"
    }

    positions_dict = {
        "1" : "Top",
        "2" : "Jungler",
        "3" : "Mid",
        "4" : "ADC",
        "5" : "Support"
    }

    def ask_action(self):
        return super().get_list_input("Entrez l'action à réaliser : ", UserView.actions_dict.values())

    def ask_pseudo_for_analyse(self):
        return super().get_input("Entrez le pseudo du joueur à analyser : ")

    def ask_for_position(self):
        return super().get_list_input("Entrez la position à analyser : ", UserView.positions_dict.values())