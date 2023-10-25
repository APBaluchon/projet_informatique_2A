from business_layer.controler.view import View


class GuestView(View):
    
    def ask_pseudo(self):
        return super().get_input("Pseudo : ")

    def ask_password(self):
        return super().get_input("Password : ", "password")

    def wrong_password(self):
        print("Mot de passe incorrect. Veuillez réessayer.")