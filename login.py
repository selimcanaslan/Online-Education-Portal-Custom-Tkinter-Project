import customtkinter
from db_connection import DbConnection
from register import RegisterWindow
from main_window import MainWindow
from info_message import InfoMessage

LOGIN_RES = [300, 350]
MAIN_RES = [1600, 900]
IMAGE_RES = [100, 100]


class LoginWindow:
    def __init__(self):
        # ui start
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.root = customtkinter.CTk()
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        x = (self.ws / 2) - (LOGIN_RES[0] / 2)
        y = (self.hs / 2) - (LOGIN_RES[1] / 2)
        self.root.geometry('%dx%d+%d+%d' % (LOGIN_RES[0], LOGIN_RES[1], x, y))
        self.root.minsize(width=300, height=350)
        self.root.maxsize(width=300, height=350)
        self.root.title("Online Education Portal")
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text="ONLİNE EDUCATION PORTAL",
                                            text_color="white", font=("Roboto", 18))
        self.label.pack(pady=12, padx=10)

        self.school_number_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="School Number")
        self.school_number_entry.pack(pady=12, padx=10)

        self.password_entry = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = customtkinter.CTkButton(master=self.frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        with open("user_info.txt") as f:
            if len(f.read()) > 0:
                self.checkbox = customtkinter.CTkCheckBox(master=self.frame, text="Remember Me",
                                                          border_width=1, border_color="green")
                self.checkbox.pack(pady=12, padx=10)
                self.checkbox.select()
                f.close()
            else:
                self.checkbox = customtkinter.CTkCheckBox(master=self.frame, text="Remember Me",
                                                          border_width=1, border_color="green")
                self.checkbox.pack(pady=12, padx=10)
                f.close()

        self.register_text = customtkinter.CTkLabel(master=self.frame, text="You can register via 'REGISTER' Button.")
        self.register_text.pack()

        self.register_button = customtkinter.CTkButton(master=self.frame, text="REGISTER",
                                                       command=self.open_register_window)
        self.register_button.pack()
        self.remember()
        # ui end

    def login(self):
        if len(self.school_number_entry.get()) >= 1 and len(self.password_entry.get()) >= 1:
            school_number = self.school_number_entry.get()
            password = self.password_entry.get()
            conn = DbConnection().get_conn()
            cursor = conn.cursor()

            cursor.execute(f" SELECT ogr_sifre FROM ogr_login WHERE ogr_no = '{school_number}' ")
            ogr_password = cursor.fetchall()

            ogr_name_rec = cursor.execute(f"SELECT ogr_ad + ' ' + ogr_soyad FROM ogrenci where ogr_no={school_number}")
            ogr_name = ogr_name_rec.fetchall()

            grade_rec = cursor.execute(f"SELECT ogr_sinif FROM ogrenci WHERE ogr_no ={school_number}")
            grade = grade_rec.fetchall()
            if len(grade) > 0:
                grade = grade[0][0][6:]

            point_rec = cursor.execute(f"SELECT basarim_puani FROM ogrenci WHERE ogr_no={school_number}")
            point = point_rec.fetchall()
            if len(point) > 0:
                point = point[0][0]
            conn.commit()
            conn.close()
            if len(ogr_password) > 0:
                if password == ogr_password[0][0]:
                    if self.checkbox.get() == 1:
                        file = open("user_info.txt", "w")
                        file.write(str(self.checkbox.get()) + ",")
                        file.write(school_number + ",")
                        file.write(password + ",")
                        file.close()
                        self.open_main_window(ogr_name[0][0], school_number, grade, point)
                    else:
                        file = open("user_info.txt", "w")
                        file.truncate()
                        file.close()
                else:
                    y = InfoMessage("You have entered wrong password")
                    y.show_error()
            else:
                InfoMessage("Bu bilgilere sahip bir kullanıcı bulunamadı !").show_error()
        else:
            msg = "Please fill the school number and password"
            m = InfoMessage(msg)
            m.show_error()

    def remember(self):
        with open("user_info.txt") as file:
            temp = ""
            counter = 0
            text = file.read()
            for digit in text:
                if digit != ",":
                    temp += digit
                else:
                    if counter == 0:
                        # print(temp)
                        counter += 1
                    elif counter == 1:
                        # print(temp[1:5])
                        self.school_number_entry.insert(0, temp[1:5])
                        counter += 1
                    elif counter == 2:
                        # print(temp[5:10])
                        self.password_entry.insert(0, temp[5:10])
                        counter += 1
            file.close()

    def open_main_window(self, name, school_number, grade, point):
        MainWindow(name, school_number, grade, point)
        

    def open_register_window(self):
        RegisterWindow()


if __name__ == "__main__":
    ui = LoginWindow()
    ui.root.mainloop()
