from CTkMessagebox import CTkMessagebox

WIDTH = 350
HEIGHT = 150


class InfoMessage:
    def __init__(self, msg):
        self.msg = msg

    def show_info(self):
        CTkMessagebox(title="Info", message=self.msg, width=WIDTH, height=HEIGHT)

    def show_checkmark(self):
        CTkMessagebox(message=self.msg,
                      icon="check", option_1="Thanks", width=WIDTH, height=HEIGHT)

    def show_error(self):
        CTkMessagebox(title="Error", message=self.msg, icon="cancel", width=WIDTH, height=HEIGHT)

    def ask_question(self):
        shown_message = CTkMessagebox(title="Uygulama Kapatılacak", message=self.msg,
                            icon="question", option_1="Vazgeç", option_2="Hayır", option_3="Evet")
        response = shown_message.get()

        if response == "Evet":
            return True
        else:
            return False
        
