import customtkinter
import sys
import json
from info_message import InfoMessage
from db_connection import DbConnection
from datetime import datetime

class Quiz:
    def __init__(self, quiz_name, lesson_name):
        self.school_number = int
        self.get_student_info()
        self.quiz_name = quiz_name
        self.lesson_name = lesson_name
        with open(f"assets\quiz/{self.quiz_name}.json", encoding='utf-8') as f:
            self.quiz_data = json.load(f) 
        self.questions = self.quiz_data['questions']
        self.options = self.quiz_data['options']
        self.answers = self.quiz_data['answers']
        self.question_count = len(self.questions)
        self.current_question_number = 0
        self.timer_running = True
        self.quiz_suresi = 1800
        self.current_selected_answer = 0
        self.correct_answer_count = 0
        self.wrong_answer_count = 0
        self.passed_answer_count = 0
        self.timer_running = True
        self.root = customtkinter.CTkToplevel()
        self.root.title(f"Quiz")
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        self.root.geometry(f"{ws}, {hs}")
        self.root.minsize(ws, hs)
        self.root.maxsize(ws, hs)
        self.root.attributes("-fullscreen", "True")
        self.root.focus()
        self.root.grab_set()
        self.center_frame = customtkinter.CTkFrame(master=self.root)
        self.center_frame.pack(padx=20, pady=20, fil='both', expand=True)

        self.question_frame = customtkinter.CTkFrame(master=self.center_frame)
        self.question_frame.pack(side='top', expand=False, fill='both')
        self.question_frame_content(self.current_question_number)

        self.option_frame = customtkinter.CTkFrame(master=self.center_frame)
        self.option_frame.pack(side='left', expand=True, fill='both', padx=10, pady=10)
        self.option_frame_content(self.current_question_number)

        self.next_question_button = customtkinter.CTkButton(master=self.option_frame,
                                                            width=300,
                                                            height=150, 
                                                            text='Sonraki Soru',
                                                            command=self.get_next_question)
        self.next_question_button.pack(side='right', expand=False, fill='x')

        self.info_frame = customtkinter.CTkFrame(master=self.center_frame)
        self.info_frame.pack(side='bottom', expand=True, fill='both', padx=10, pady=10)
        self.info_frame_content()
        self.update_timer()

    def question_frame_content(self, question_number):
        self.question_label = customtkinter.CTkLabel(master=self.question_frame,
                                                font=('Roboto', 24, 'bold'),
                                                text=f"Soru {question_number + 1}: {self.questions[question_number]}")
        self.question_label.pack(side='top', fill='both', expand=False, padx=10, pady=10)

    def option_frame_content(self, question_number):
        self.option1 = customtkinter.CTkCheckBox(master=self.option_frame,command=self.option1_clicked, text=f"{self.options[question_number][0]}")
        self.option1.pack(side='left', expand=True)

        self.option2 = customtkinter.CTkCheckBox(master=self.option_frame,command=self.option2_clicked, text=f"{self.options[question_number][1]}")
        self.option2.pack(side='left', expand=True)

        self.option3 = customtkinter.CTkCheckBox(master=self.option_frame,command=self.option3_clicked, text=f"{self.options[question_number][2]}")
        self.option3.pack(side='left', expand=True)

        self.option4 = customtkinter.CTkCheckBox(master=self.option_frame,command=self.option4_clicked, text=f"{self.options[question_number][3]}")
        self.option4.pack(side='left', expand=True)

        self.option5 = customtkinter.CTkCheckBox(master=self.option_frame,command=self.option5_clicked, text=f"{self.options[question_number][4]}")
        self.option5.pack(side='left', expand=True)

    def info_frame_content(self):
        self.timer_text = customtkinter.CTkLabel(master=self.info_frame, text='', font=('Roboto', 20, 'bold'))
        self.timer_text.pack(side='top', padx=10, pady=10)

        self.question_count_text = customtkinter.CTkLabel(master=self.info_frame, font=('Roboto', 20, 'bold'), text=f"Toplam Soru: {self.question_count}")
        self.question_count_text.pack(side='top', padx=10, pady=10)

        self.remaining_question_count = customtkinter.CTkLabel(master=self.info_frame, font=('Roboto', 20, 'bold'), text=f"Kalan Soru: {self.question_count - self.current_question_number}")
        self.remaining_question_count.pack(side='top', padx=10, pady=10)

        self.exit_button = customtkinter.CTkButton(master=self.info_frame, text="Exit", command=self.close).pack(side='bottom', expand=False, fill='x')


    def option1_clicked(self):
        self.option2.deselect()
        self.option3.deselect()
        self.option4.deselect()
        self.option5.deselect()
        self.current_selected_answer = 1

    def option2_clicked(self):
        self.option1.deselect()
        self.option3.deselect()
        self.option4.deselect()
        self.option5.deselect()
        self.current_selected_answer = 2

    def option3_clicked(self):
        self.option1.deselect()
        self.option2.deselect()
        self.option4.deselect()
        self.option5.deselect()
        self.current_selected_answer = 3

    def option4_clicked(self):
        self.option1.deselect()
        self.option2.deselect()
        self.option3.deselect()
        self.option5.deselect()
        self.current_selected_answer = 4

    def option5_clicked(self):
        self.option1.deselect()
        self.option2.deselect()
        self.option3.deselect()
        self.option4.deselect()
        self.current_selected_answer = 5

    def get_next_question(self):
        self.check_the_answer()
        self.current_question_number += 1
        if self.current_question_number < self.question_count:
            self.clear_question_and_options()
            self.question_frame_content(self.current_question_number)
            self.option_frame_content(self.current_question_number)
            self.next_question_button = customtkinter.CTkButton(master=self.option_frame,
                                                                width=300,
                                                                height=150,
                                                                text='Sonraki Soru',
                                                                command=self.get_next_question)
            self.next_question_button.pack(side='right', expand=False, fill='x')
            self.update_remaining_question_count()
        else:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conn = DbConnection().get_conn()
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO son_quizler VALUES ({int(self.school_number)}, '{self.lesson_name}', '{str(self.quiz_name)}', {self.correct_answer_count}, {self.wrong_answer_count}, {self.passed_answer_count}, {self.correct_answer_count - (self.wrong_answer_count / 4)}, '{now}')")
            conn.commit()
            conn.close()
            print(f"Dogru Sayisi = {self.correct_answer_count} \n Yanlis Sayisi = {self.wrong_answer_count} \n Bos Sayisi = {self.passed_answer_count}")
            self.clear_question_and_options()
            self.quiz_suresi = -1
            self.timer_text.configure(text="Sınavı Bitirdiniz")
            self.finish_quiz_button = customtkinter.CTkButton(master=self.option_frame,
                                                               text="Quizi Bitir",
                                                                font=('Roboto', 30, 'bold'),
                                                                 command=self.close)
            self.finish_quiz_button.pack(side='left', fill='both', expand=True)
            self.remaining_question_count.configure(text=f"Kalan Soru: 0")
            
    def check_the_answer(self):
        if self.current_selected_answer == 1:
            if self.answers[self.current_question_number] == self.option1.cget('text'):
                self.correct_answer_count += 1
                self.current_selected_answer = 0
            else:
                self.wrong_answer_count += 1
                self.current_selected_answer = 0

        elif self.current_selected_answer == 2:
            if self.answers[self.current_question_number] == self.option2.cget('text'):
                self.correct_answer_count += 1
                self.current_selected_answer = 0
            else:
                self.wrong_answer_count += 1
                self.current_selected_answer = 0

        elif self.current_selected_answer == 3:
            if self.answers[self.current_question_number] == self.option3.cget('text'):
                self.correct_answer_count += 1
                self.current_selected_answer = 0
            else:
                self.wrong_answer_count += 1
                self.current_selected_answer = 0

        elif self.current_selected_answer == 4:
            if self.answers[self.current_question_number] == self.option4.cget('text'):
                self.correct_answer_count += 1
                self.current_selected_answer = 0
            else:
                self.wrong_answer_count += 1
                self.current_selected_answer = 0

        elif self.current_selected_answer == 5:
            if self.answers[self.current_question_number] == self.option5.cget('text'):
                self.correct_answer_count += 1
                self.current_selected_answer = 0
            else:
                self.wrong_answer_count += 1
                self.current_selected_answer = 0

        elif self.current_selected_answer == 0:
            self.passed_answer_count += 1

    def clear_question_and_options(self):
        for widgets in self.question_frame.winfo_children():
            widgets.destroy()
        for widgets in self.option_frame.winfo_children():
            widgets.destroy()

    def update_remaining_question_count(self):
        self.remaining_question_count.configure(text=f"Kalan Soru: {self.question_count - self.current_question_number}")

    def update_timer(self):
        if self.timer_running:
            if self.quiz_suresi > 0:
                self.quiz_suresi = self.quiz_suresi - 1
                dakika = self.quiz_suresi // 60
                saniye = self.quiz_suresi % 60
                self.timer_text.configure(text=f"{dakika}dk. {saniye}.sn")
                self.root.after(1000, self.update_timer)
            elif self.quiz_suresi == 0:
                self.timer_running = False
                self.timer_text.configure(text="Süreniz Doldu.")

    def close(self):
        if self.quiz_suresi > 1200:
            InfoMessage("ilk 10 Dakika Sınavı Sonlandıramazsınız.").show_info()
        else:
            conn = DbConnection().get_conn()
            crsr = conn.cursor()
            crsr.execute(f"SELECT basarim_puani from ogrenci WHERE ogr_no={self.school_number}")
            old_point = crsr.fetchone()[0]
            conn.commit()
            print(old_point)
            new_point = old_point + (self.correct_answer_count - (self.wrong_answer_count / 4))
            print(new_point)
            crsr.execute(f"UPDATE ogrenci SET basarim_puani={new_point} WHERE ogr_no={self.school_number}")
            conn.commit()
            conn.close()
            self.root.withdraw()
            sys.exit() # if you want to exit the entire thing

    def get_student_info(self):
        with open("user_info.txt") as file:
            temp = ""
            counter = 0
            text = file.read()
            for digit in text:
                if digit != ",":
                    temp += digit
                else:
                    if counter == 0:
                        counter += 1
                    elif counter == 1:
                        self.school_number = int(temp[1:5])
                        counter += 1
            file.close()
if __name__ == "__main__":
    app = Quiz('Logaritma1')
    app.root.mainloop()
