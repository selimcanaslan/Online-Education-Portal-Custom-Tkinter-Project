import customtkinter
import random
from db_connection import DbConnection
from info_message import InfoMessage

REGISTER_RES = [250, 350]


class RegisterWindow:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ui
        self.register_win = customtkinter.CTkToplevel()
        self.register_win.title("Register")
        self.ws = self.register_win.winfo_screenwidth()
        self.hs = self.register_win.winfo_screenheight()
        x = (self.ws / 2) - (REGISTER_RES[0] / 2)
        y = (self.hs / 2) - (REGISTER_RES[1] / 2)
        self.register_win.geometry('%dx%d+%d+%d' % (REGISTER_RES[0], REGISTER_RES[1], x, y))
        self.register_win.minsize(REGISTER_RES[0], REGISTER_RES[1])
        self.register_win.maxsize(REGISTER_RES[0], REGISTER_RES[1])
        self.register_win.focus()
        self.register_win.grab_set()

        self.frame = customtkinter.CTkFrame(master=self.register_win)
        self.frame.pack(fill="both", expand=True)

        self.register_text = customtkinter.CTkLabel(master=self.frame, text="REGISTER", font=("Roboto", 18))
        self.register_text.pack(pady=12, padx=10)

        self.student_name = customtkinter.CTkEntry(master=self.frame, placeholder_text="Your Name", )
        self.student_name.pack(pady=3)

        self.student_surname = customtkinter.CTkEntry(master=self.frame, placeholder_text="Surname")
        self.student_surname.pack(pady=3)

        self.student_phone_number = customtkinter.CTkEntry(master=self.frame, placeholder_text="Phone Number", )
        self.student_phone_number.pack(pady=3)

        self.student_mail = customtkinter.CTkEntry(master=self.frame, placeholder_text="Mail Address", )
        self.student_mail.pack(pady=3)

        self.major = DbConnection().fetch_major()
        self.student_major_combobox = customtkinter.CTkComboBox(master=self.frame, values=self.major)
        self.student_major_combobox.pack(pady=3)
        self.student_major_combobox.set("Your Major")

        self.grade = DbConnection().fetch_class()
        self.student_grade_combobox = customtkinter.CTkComboBox(master=self.frame, values=self.grade)
        self.student_grade_combobox.pack(pady=3)
        self.student_grade_combobox.set("Your Grade")

        self.register_button = customtkinter.CTkButton(master=self.frame, text="Register", command=self.validate_fields)
        self.register_button.pack(pady=10)
        # ui end

        self.mail_types = ["@hotmail.com", "@gmail.com", "@outlook.com"]
        self.err_dict = {
            "blank_name_err": "You have to fill the name section\n",
            "blank_surname_err": "You have to fill the surname section\n",
            "blank_phone_err": "You have to fill the phone number section\n",
            "blank_mail_err": "You have to fill the mail section\n",
            "major_not_selected": "Please choose your major\n",
            "grade_not_selected": "Please choose your grade\n",
            "name_numeric_err": "Please do not enter number in your name\n",
            "surname_numeric_err": "Please do not enter number in your surname\n",
            "invalid_phone_number": "Please enter a valid phone number\n",
            "invalid_mail_address": "Please enter a valid mail address\n"
        }

    def validate_fields(self):
        name = self.student_name.get()
        surname = self.student_surname.get()
        phone_number = self.student_phone_number.get()
        mail = self.student_mail.get()
        student_major = self.student_major_combobox.get()
        student_grade = self.student_grade_combobox.get()
        info_text = ""
        err_list = []

        if len(name) < 1:
            err_list.append(self.err_dict["blank_name_err"])
        if name.isnumeric():
            err_list.append(self.err_dict["name_numeric_err"])
        if len(surname) == 0:
            err_list.append(self.err_dict["blank_surname_err"])
        if surname.isnumeric():
            err_list.append(self.err_dict["surname_numeric_err"])
        if len(phone_number) < 1:
            err_list.append(self.err_dict["blank_phone_err"])
        if not phone_number.isdigit() and len(phone_number) != 0:
            err_list.append(self.err_dict["invalid_phone_number"])
        if len(mail) == 0:
            err_list.append(self.err_dict["blank_mail_err"])
        if len(mail) > 0:
            counter = 0
            for x in self.mail_types:
                if mail.endswith(x):
                    counter += 1
            if counter == 0:
                err_list.append(self.err_dict["invalid_mail_address"])
        if student_major == "Your Major":
            err_list.append(self.err_dict["major_not_selected"])
        if student_grade == "Your Grade":
            err_list.append(self.err_dict["grade_not_selected"])
        if len(err_list) == 0:
            for i in range(1, 9999):
                student_number = random.randint(1, 9999)
                if self.fetch_student_numbers(student_number):
                    self.send_to_database(student_number, name, surname, phone_number, mail,
                                          student_major, student_grade)
                    break
        else:
            i = 1
            for err in err_list:
                info_text += f"{str(i)} - {err}"
                i += 1
            InfoMessage(info_text).show_info()

    def fetch_student_numbers(self, number):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT ogr_no FROM ogrenci WHERE ogr_no={number}")
        records = cursor.fetchall()
        if len(records) > 0:
            return False
        else:
            return True

    def send_to_database(self, student_number, name, surname, phone_number, mail_address, student_major, student_grade):
        student_number = student_number
        name = name
        surname = surname
        phone_number = phone_number
        mail_address = mail_address
        student_major = student_major
        student_grade = student_grade
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO ogrenci (ogr_no,ogr_ad,ogr_soyad,ogr_telefon,ogr_mail,ogr_alan,ogr_sinif,basarim_puani) VALUES \
            ({student_number},'{name}','{surname}','{phone_number}','{mail_address}',"
            f"'{student_major}','{student_grade}', {0})")
        conn.commit()
        conn.close()
        InfoMessage(f"Tebrikler Başarıyla Kayıt Oldunuz. Numaranız ve Şifreniz : {student_number}").show_info()
