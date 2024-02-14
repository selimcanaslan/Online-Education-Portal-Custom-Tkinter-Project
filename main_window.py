import customtkinter
from customtkinter import *
from PIL import Image
import os
from tkinter import ttk
from db_connection import DbConnection
from info_message import InfoMessage
from quiz import Quiz
from konular import Konu
import subprocess
from CTkListbox import *
from PIL import Image
from datetime import datetime

MAIN_RES = [1600, 900]
IMAGE_RES = [150, 150]
ICON_RES = [25, 25]

class MainWindow:
    def __init__(self, name, school_number, grade, point):
        # Needed Variables
        self.version = 'Version 0.01 \n by SCA'
        self.font = ("Roboto", 14, "bold")
        self.video_duration = 0
        self.lessons12 = ['Matematik', 'Türkçe', 'Biyoloji', 'Coğrafya', 'Felsefe', 'Fizik', 'Yabancı Dil', 'Sosyoloji']
        self.lesson_select_state = False
        self.is_video_playing = False
        self.is_music_paused = False
        self.name = name
        self.school_number = school_number
        self.grade = grade
        self.point = point
        self.last_clicked_video_button_text = ''
        self.color_mode = 'dark'

        # Creating Main Window
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.main_window = customtkinter.CTkToplevel()
        self.main_window.title(f"Online Education Portal - {self.name} - {self.school_number}")
        self.ws = self.main_window.winfo_screenwidth()
        self.hs = self.main_window.winfo_screenheight()
        MAIN_RES[0] = self.ws * 3 / 4
        MAIN_RES[1] = self.hs * 3 / 4
        self.main_window.attributes("-fullscreen", "True")
        x = (self.ws / 2) - (MAIN_RES[0] / 2)
        y = (self.hs / 2) - (MAIN_RES[1] / 2)
        self.main_window.geometry('%dx%d+%d+%d' % (MAIN_RES[0], MAIN_RES[1], x, y))
        self.main_window.minsize(MAIN_RES[0], MAIN_RES[1])
        self.main_window.maxsize(MAIN_RES[0], MAIN_RES[1])
        self.main_window.focus()
        self.main_window.grab_set()
        # Creating Main Window Ends

        # window components
        self.left_side_frame = customtkinter.CTkScrollableFrame(master=self.main_window, scrollbar_button_color='#323232', width=280)
        self.left_side_frame.pack(padx=5, pady=5, side='left', expand=False, fill='both')

        self.student_information_frame()
        self.build_achievement_frame()
        self.last_views_frame()
        self.completed_quizzes_frame()
        self.all_rights_deserved_frame()
        self.center_frame_default()
        self.global_ranking_frame()
        self.bottom_frame_default()

        # window components ends

    def student_information_frame(self):
        self.student_info_frame = customtkinter.CTkFrame(master=self.left_side_frame)
        self.student_info_frame.pack(padx=5, pady=5, side='top', expand=False, fill='both')
        if os.path.exists(f"assets/pictures/profile_pictures/{self.school_number}.jpg"): 
            self.student_profile_photo = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(f"assets/pictures/profile_pictures/{self.school_number}.jpg")),
                size=(IMAGE_RES[0], IMAGE_RES[1]))
            self.label = customtkinter.CTkLabel(master=self.student_info_frame, image=self.student_profile_photo, text='')
            self.label.pack(pady=20)
        else:
            self.student_profile_photo = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(f"assets/pictures/profile_holder.jpg")),
                size=(IMAGE_RES[0], IMAGE_RES[1]))
            self.label = customtkinter.CTkLabel(master=self.student_info_frame, image=self.student_profile_photo, text='')
            self.label.pack(pady=20)
        self.student_name_text = customtkinter.CTkLabel(master=self.student_info_frame,
                                                        text=DbConnection().get_student_name(self.school_number),
                                                        width=220, pady=5,
                                                        font=("Roboto", 21, 'bold'))
        self.student_name_text.pack(side='top')
        self.student_number = customtkinter.CTkLabel(master=self.student_info_frame,
                                                     text=f"Okul No: {self.school_number}",
                                                     pady=5,
                                                     font=("Roboto", 21, 'bold'))
        self.student_number.pack(side='top')
        self.student_grade = customtkinter.CTkLabel(master=self.student_info_frame,
                                                    text=f"Sınıf: {self.grade}",
                                                    pady=5,
                                                    font=("Roboto", 21, 'bold'))
        self.student_grade.pack(side='top')
        self.achievement_point_text = customtkinter.CTkLabel(master=self.student_info_frame,
                                                             text=f"Puan: {self.point}",
                                                             pady=5,
                                                             font=("Roboto", 21, 'bold'))
        self.achievement_point_text.pack(side='top')

        self.general_ranking_text = customtkinter.CTkLabel(master=self.student_info_frame,
                                                           text=f"Genel Sıralama: {self.get_student_ranking()} ",
                                                           pady=5,
                                                           font=("Roboto", 21, 'bold'))
        self.general_ranking_text.pack(side='top')

    def build_achievement_frame(self):
        self.achievement_frame = customtkinter.CTkFrame(master=self.left_side_frame)
        self.achievement_frame.pack(padx=5, pady=5, side='top', expand=False, fill='both')

        self.lesson_achievement_text = customtkinter.CTkLabel(master=self.achievement_frame,
                                                              text="BAŞARIMLAR",
                                                              font=self.font,
                                                              text_color="#f5c842")
        self.lesson_achievement_text.pack(side='top', pady=10)
        listbox = CTkListbox(self.achievement_frame, height=250, justify='center', font=("Roboto", 20), command=self.list_box_clicked)
        listbox.pack(side='top', expand=False, fill='both')
        x = 0
        for lesson in self.lessons12:
            listbox.insert(x, f"~ {lesson} ~")
            x += 1

    def last_views_frame(self):
        self.last_viewed_frame = customtkinter.CTkFrame(master=self.left_side_frame)
        self.last_viewed_frame.pack(padx=5, pady=5, side='top', expand=False, fill='both')

        self.last_viewed = customtkinter.CTkLabel(master=self.last_viewed_frame,
                                                   text="Son İzlenenler",
                                                   font=self.font,
                                                   text_color="#f5c842")
        self.last_viewed.pack(side='top', expand=False, fill='both', padx=10, pady=10)

        conn_for_last_viewed = DbConnection().get_conn()
        cursor_viewed = conn_for_last_viewed.cursor()
        cursor_viewed.execute(f"SELECT * FROM son_izlenenler WHERE ogr_no={self.school_number} ORDER BY izlenme_tarihi DESC")
        last_viewed = cursor_viewed.fetchall()
        viewed_counter = 0
        if len(last_viewed) > 0:
            for last_ones in last_viewed:
                if viewed_counter < 5:
                    customtkinter.CTkLabel(master=self.last_viewed_frame, font=("Roboto", 15), text=str(last_ones[1]) + ' - ' + str(last_ones[2])[:16]).pack(side='top', expand=False, fill='both', padx=5, pady=5)
                    viewed_counter += 1
        else:
            customtkinter.CTkLabel(master=self.last_viewed_frame, font=("Roboto", 15), text="Henüz Video İzlemediniz.").pack(side='top', expand=False, fill='both')
        
    def last_views_frame_refresh(self):
        for widgets in self.last_viewed_frame.winfo_children():
            widgets.destroy()
        self.last_viewed = customtkinter.CTkLabel(master=self.last_viewed_frame,
                                                   text="Son İzlenenler",
                                                   font=self.font,
                                                   text_color="#f5c842")
        self.last_viewed.pack(side='top', expand=False, fill='both', padx=10, pady=10)

        conn_for_last_viewed = DbConnection().get_conn()
        cursor_viewed = conn_for_last_viewed.cursor()
        cursor_viewed.execute(f"SELECT * FROM son_izlenenler WHERE ogr_no={self.school_number} ORDER BY izlenme_tarihi DESC")
        last_viewed = cursor_viewed.fetchall()
        viewed_counter = 0
        if len(last_viewed) > 0:
            for last_ones in last_viewed:
                if viewed_counter < 5:
                    customtkinter.CTkLabel(master=self.last_viewed_frame, font=("Roboto", 15), text=str(last_ones[1]) + ' - ' + str(last_ones[2])[:16]).pack(side='top', expand=False, fill='both', padx=5, pady=5)
                    viewed_counter += 1
        else:
            customtkinter.CTkLabel(master=self.last_viewed_frame, font=("Roboto", 15), text="Henüz Video İzlemediniz.").pack(side='top', expand=False, fill='both')

    def completed_quizzes_frame(self):
        self.completed_quizzes = customtkinter.CTkFrame(master=self.left_side_frame)
        self.completed_quizzes.pack(padx=5, pady=5, side='top', expand=False, fill='both')
        conn = DbConnection().get_conn()
        quiz_records = conn.cursor()
        quiz_records.execute(f"SELECT * FROM son_quizler WHERE ogr_no={self.school_number} ORDER BY quiz_tarihi DESC")
        quizzes = quiz_records.fetchall()
        conn.commit()
        conn.close()
        customtkinter.CTkLabel(master=self.completed_quizzes, text="Son Tamamlanan Quizler",
                                                   font=self.font,
                                                   text_color="#f5c842").pack(side='top', expand=False, fill='both', padx=5, pady=5)
        x = 0
        for quiz in quizzes:
            print(quiz)
            if x < 5 and x < len(quizzes):
                customtkinter.CTkLabel(master=self.completed_quizzes, text=f"{quiz[2]} : {quiz[3]}D-{quiz[4]}Y-{quiz[5]}B",
                                                    font=("Roboto", 15)).pack(side='top', padx=10, pady=5)
            x += 1
                
    def completed_quizzes_refresh(self):
        for widgets in self.completed_quizzes.winfo_children():
            widgets.destroy()
        conn = DbConnection().get_conn()
        quiz_records = conn.cursor()
        quiz_records.execute(f"SELECT * FROM son_quizler WHERE ogr_no={self.school_number} ORDER BY quiz_tarihi DESC")
        quizzes = quiz_records.fetchall()
        conn.commit()
        conn.close()
        customtkinter.CTkLabel(master=self.completed_quizzes, text="Son Tamamlanan Quizler",
                                                   font=self.font,
                                                   text_color="#f5c842").pack(side='top', expand=False, fill='both', padx=5, pady=5)
        x = 0
        for quiz in quizzes:
            if x < 5 and x < len(quizzes):
                customtkinter.CTkLabel(master=self.completed_quizzes, text=f"{quiz[2]} : {quiz[3]}D-{quiz[4]}Y-{quiz[5]}B",
                                                    font=("Roboto", 15)).pack(side='top', padx=10, pady=5)
                x += 1



    def all_rights_deserved_frame(self):
        self.all_rights_reserved = customtkinter.CTkLabel(master=self.left_side_frame,
                                                          text=f"{self.version}",
                                                          font=self.font,
                                                          text_color="#868a7d")
        self.all_rights_reserved.pack(side='bottom')

    def center_frame_default(self):
        self.center_frame = customtkinter.CTkFrame(master=self.main_window)
        self.center_frame.pack(padx=5, pady=5, side='left', expand=True, fill='both')

        self.hi_text = customtkinter.CTkLabel(master=self.center_frame, 
                                              text=f"Merhaba {self.name}\n Bugün Hangi Dersi Çalışmak İstersin ?",
                                              font=("Roboto", 25, "bold"))
        self.hi_text.pack(side='top', padx=15, pady=15)
        self.matematik = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Matematik',
                                                 font=self.font,
                                                 fg_color="#13D9FC",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\math.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\math.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.turkce = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Türkçe',
                                                 font=self.font,
                                                 fg_color="#FF3B3B",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\turkce.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\turkce.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.biyoloji = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Biyoloji',
                                                 font=self.font,
                                                 fg_color="#B5FF3B",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\biology.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\biology.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.cografya = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Coğrafya',
                                                 font=self.font,
                                                 fg_color="#FFC13B",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\geography.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\geography.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.felsefe = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Felsefe',
                                                 font=self.font,
                                                 fg_color="#B4B4B4",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\philosophy.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\philosophy.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.fizik = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Fizik',
                                                 font=self.font,
                                                 fg_color="#3F5FFF",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\physics.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\physics.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.yabanci_dil = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Yabancı Dil',
                                                 font=self.font,
                                                 fg_color="#FFF93F",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\foreign_language.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\foreign_language.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.kimya = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Kimya',
                                                 font=self.font,
                                                 fg_color="#D03FFF",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\chemistry.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\chemistry.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        
    def back_to_center_frame_default(self):
        self.clear_center_frame()
        self.bottom_frame_default()
        self.hi_text = customtkinter.CTkLabel(master=self.center_frame, 
                                              text=f"Merhaba {self.name}\n Bugün Hangi Dersi Çalışmak İstersin ?",
                                              font=("Roboto", 25, "bold"))
        self.hi_text.pack(side='top', padx=15, pady=15)
        self.matematik = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Matematik',
                                                 font=self.font,
                                                 fg_color="#13D9FC",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\math.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\math.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.turkce = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Türkçe',
                                                 font=self.font,
                                                 fg_color="#FF3B3B",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\turkce.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\turkce.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.biyoloji = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Biyoloji',
                                                 font=self.font,
                                                 fg_color="#B5FF3B",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\biology.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\biology.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.cografya = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Coğrafya',
                                                 font=self.font,
                                                 fg_color="#FFC13B",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\geography.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\geography.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.felsefe = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Felsefe',
                                                 font=self.font,
                                                 fg_color="#B4B4B4",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\philosophy.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\philosophy.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.fizik = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Fizik',
                                                 font=self.font,
                                                 fg_color="#3F5FFF",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\physics.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\physics.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.yabanci_dil = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Yabancı Dil',
                                                 font=self.font,
                                                 fg_color="#FFF93F",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\foreign_language.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\foreign_language.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)
        self.kimya = customtkinter.CTkButton(master=self.center_frame,
                                                 text='Kimya',
                                                 font=self.font,
                                                 fg_color="#D03FFF",
                                                 hover_color="#000000",
                                                 image=customtkinter.CTkImage(light_image=Image.open(r"assets\pictures\lesson_pictures\chemistry.png"),
                                                    dark_image=Image.open(r"assets\pictures\lesson_pictures\chemistry.png"),
                                                    size=(60, 60)),
                                                 command=self.center_frame_matematik).pack(side='top', fill='both', expand=True, pady=5, padx=10)

    def global_ranking_frame(self):
        self.ranking_frame = customtkinter.CTkFrame(master=self.main_window)
        self.ranking_frame.pack(padx=5, pady=5, side='right', expand=False, fill='both')

        self.ranking_title = customtkinter.CTkLabel(master=self.ranking_frame,
                                                text='Global Başarımlar',
                                                  font=("Roboto", 20, "bold"),
                                                  text_color="#f5c842").pack(side='top', pady=20, padx=20, fill='both')
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT ogr_ad + ' ' + ogr_soyad, basarim_puani from ogrenci ORDER BY basarim_puani DESC")
        best_students = cursor.fetchall()
        rank = 1
        for student in best_students:
            if rank <11:
                customtkinter.CTkLabel(master=self.ranking_frame,font=("Roboto", 20), text= str(rank) + '-' + str(student[0]) + ' / ' + str(student[1]) + ' Puan').pack(side='top', fill='both', padx=5, pady=5)
                rank += 1
            else:
                pass

    def global_ranking_refresh(self):
        for widgets in self.ranking_frame.winfo_children():
            widgets.destroy()
        self.ranking_title = customtkinter.CTkLabel(master=self.ranking_frame,
                                                text='Global Başarımlar',
                                                  font=("Roboto", 20, "bold"),
                                                  text_color="#f5c842").pack(side='top', pady=20, padx=20, fill='both')
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT ogr_ad + ' ' + ogr_soyad, basarim_puani from ogrenci ORDER BY basarim_puani DESC")
        best_students = cursor.fetchall()
        rank = 1
        for student in best_students:
            if rank <11:
                customtkinter.CTkLabel(master=self.ranking_frame,font=("Roboto", 20), text= str(rank) + '-' + str(student[0]) + ' / ' + str(student[1]) + ' Puan').pack(side='top', fill='both', padx=5, pady=5)
                rank += 1
            else:
                pass

    def bottom_frame_default(self):
        self.bottom_frame = customtkinter.CTkFrame(master=self.center_frame, height=10)
        self.bottom_frame.pack(padx=5, pady=5, side='bottom', expand=False, fill='both')
        self.quiz_button = customtkinter.CTkButton(master=self.bottom_frame,
                                                   text="Quiz",
                                                   text_color="#FFFFFF",
                                                   fg_color="#4F4F4F",
                                                   hover_color="#323232")
        self.quiz_button.pack(padx=3, pady=3, expand=False, side='left', fill='both')
        self.exit_button = customtkinter.CTkButton(master=self.bottom_frame,
                                                   text="Exit",
                                                   text_color="#FFFFFF",
                                                   fg_color="#4F4F4F",
                                                   hover_color="#323232",
                                                   command=self.exit_window)
        self.exit_button.pack(padx=3, pady=3, expand=False, side='left', fill='both')

        self.appearance_mode = customtkinter.CTkButton(master=self.bottom_frame,
                                                   text="Light Mode",
                                                   text_color="#FFFFFF",
                                                   fg_color="#4F4F4F",
                                                   hover_color="#323232",
                                                   command=self.mode_change)
        self.appearance_mode.pack(padx=3, pady=3, expand=False, side='left', fill='both')
    
    def mode_change(self):
        if self.color_mode == "dark":
            customtkinter.set_appearance_mode("light")
            self.color_mode = "light"
            self.appearance_mode.configure(text="Dark Mode")
        else:
            customtkinter.set_appearance_mode("dark")
            self.color_mode = "dark"
            self.appearance_mode.configure(text="Light Mode")


    def bottom_frame_back(self):
        self.bottom_frame_destroy()
        self.quiz_button = customtkinter.CTkButton(master=self.bottom_frame,
                                                   text="Quiz",
                                                   text_color="#FFFFFF",
                                                   fg_color="#4F4F4F",
                                                   hover_color="#323232")
        self.quiz_button.pack(padx=3, pady=3, expand=False, side='left', fill='both')
        self.exit_button = customtkinter.CTkButton(master=self.bottom_frame,
                                                   text="Exit",
                                                   text_color="#FFFFFF",
                                                   fg_color="#4F4F4F",
                                                   hover_color="#323232",
                                                   command=self.exit_window)
        self.exit_button.pack(padx=3, pady=3, expand=False, side='left', fill='both')


    def get_seperator_for_left_side_frame(self, padx, pady):
        self.separator = ttk.Separator(self.left_side_frame, orient='horizontal')
        self.separator.pack(fill='x', padx=padx, pady=pady)

    def get_seperator_for_ranking_frame(self, padx, pady):
        self.separator = ttk.Separator(self.ranking_frame, orient='horizontal')
        self.separator.pack(fill='x', padx=padx, pady=pady)

    def exit_window(self):
        response = InfoMessage("Uygulamadan çıkmak için onaylayın.!").ask_question()
        if response:
            self.main_window.destroy()
        else:
            pass

    def list_box_clicked(self, selected_option):
        InfoMessage(f"{selected_option} kadarını tamamladınız.").show_info()

    def clear_center_frame(self):
        for widgets in self.center_frame.winfo_children():
            widgets.destroy()
        
    def bottom_frame_destroy(self):
        for widgets in self.bottom_frame.winfo_children():
            widgets.destroy()
    
    def center_frame_matematik(self):
        self.clear_center_frame()
        self.bottom_frame_default()
        self.hi_text = customtkinter.CTkLabel(master=self.center_frame, 
                                              text=f"Bugün Matematik Çalışmak İçin Muhteşem Bir Gün!\n Hangi konuda videolar izlemek istersin ?",
                                              font=("Roboto", 25, "bold"))
        self.hi_text.pack(side='top', padx=15, pady=15)
        self.back_to_lessons = customtkinter.CTkButton(master=self.center_frame,
                                                       text='Derslere Dön',
                                                       font= self.font,
                                                       command=self.back_to_center_frame_default)
        self.back_to_lessons.pack(side='top', pady=10, expand=False, fill='x')

        self.first_topic_frame = customtkinter.CTkFrame(master=self.center_frame)
        self.first_topic_frame.pack(side='left', expand=True, fill='both')
        logaritma = customtkinter.CTkLabel(master=self.first_topic_frame,
                                           text='Logaritma',
                                           font=self.font)
        logaritma.pack(side='top')

        konu1 = customtkinter.CTkButton(master=self.first_topic_frame,
                                        text='Logaritma 1', font=self.font, fg_color='#FFB900', hover_color='#516867', command=self.logaritma_konu_1)
        konu1.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        konu2 = customtkinter.CTkButton(master=self.first_topic_frame,
                                        text='Logaritma 2', font=self.font, fg_color='#FFB900', hover_color='#516867', command=self.logaritma_konu_2)
        konu2.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        konu3 = customtkinter.CTkButton(master=self.first_topic_frame,
                                        text='Logaritma 3', font=self.font, fg_color='#FFB900', hover_color='#516867', command=self.logaritma_konu_3)
        konu3.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        konu4 = customtkinter.CTkButton(master=self.first_topic_frame,
                                        text='Logaritma 4', font=self.font, fg_color='#FFB900', hover_color='#516867', command=self.logaritma_konu_4)
        konu4.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        konu5 = customtkinter.CTkButton(master=self.first_topic_frame,
                                        text='Logaritma 5', font=self.font, fg_color='#FFB900',  hover_color='#516867', command=self.logaritma_konu_5)
        konu5.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        konu6 = customtkinter.CTkButton(master=self.first_topic_frame,
                                        text='Logaritma 6', font=self.font, fg_color='#FFB900',  hover_color='#516867', command=self.logaritma_konu_6)
        konu6.pack(side='top', padx=5, pady=5, fill='both', expand=True)

        self.second_topic_frame = customtkinter.CTkFrame(master=self.center_frame)
        self.second_topic_frame.pack(side='left', expand=True, fill='both')
        Cebir = customtkinter.CTkLabel(master=self.second_topic_frame,
                                           text='Cebir',
                                           font=self.font)
        Cebir.pack(side='top')
        cbr_konu1 = customtkinter.CTkButton(master=self.second_topic_frame,
                                        text='Cebir 1', font=self.font, fg_color='#00B2FF',  hover_color='#516867', command=self.cebir_konu_1)
        cbr_konu1.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        cbr_konu2 = customtkinter.CTkButton(master=self.second_topic_frame,
                                        text='Cebir 2', font=self.font, fg_color='#00B2FF',  hover_color='#516867', command=self.cebir_konu_2)
        cbr_konu2.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        cbr_konu3 = customtkinter.CTkButton(master=self.second_topic_frame, fg_color='#00B2FF', hover_color='#516867',
                                        text='Cebir 3', font=self.font)
        cbr_konu3.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        cbr_konu4 = customtkinter.CTkButton(master=self.second_topic_frame, fg_color='#00B2FF', hover_color='#516867',
                                        text='Cebir 4', font=self.font)
        cbr_konu4.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        cbr_konu5 = customtkinter.CTkButton(master=self.second_topic_frame, fg_color='#00B2FF', hover_color='#516867',
                                        text='Cebir 5', font=self.font)
        cbr_konu5.pack(side='top', padx=5, pady=5, fill='both', expand=True)

        self.third_topic_frame = customtkinter.CTkFrame(master=self.center_frame)
        self.third_topic_frame.pack(side='left', expand=True, fill='both')
        trigonometri = customtkinter.CTkLabel(master=self.third_topic_frame,
                                           text='Trigonometri',
                                           font=self.font)
        trigonometri.pack(side='top')
        trigonometri_konu1 = customtkinter.CTkButton(master=self.third_topic_frame,
                                        text='Trigonometri 1', font=self.font, fg_color='#FF004D', hover_color='#516867', command=self.trigonometri_konu_1)
        trigonometri_konu1.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        trigonometri_konu2 = customtkinter.CTkButton(master=self.third_topic_frame,
                                        text='Trigonometri 2', font=self.font, fg_color='#FF004D', hover_color='#516867', command=self.trigonometri_konu_2)
        trigonometri_konu2.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        trigonometri_konu3 = customtkinter.CTkButton(master=self.third_topic_frame, fg_color='#FF004D', hover_color='#516867',
                                        text='Trigonometri 3', font=self.font)
        trigonometri_konu3.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        trigonometri_konu4 = customtkinter.CTkButton(master=self.third_topic_frame, fg_color='#FF004D', hover_color='#516867',
                                        text='Trigonometri 4', font=self.font)
        trigonometri_konu4.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        trigonometri_konu5 = customtkinter.CTkButton(master=self.third_topic_frame, fg_color='#FF004D', hover_color='#516867',
                                        text='Trigonometri 5', font=self.font)
        trigonometri_konu5.pack(side='top', padx=5, pady=5, fill='both', expand=True)

    def logaritma_konu_1(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Logaritma1"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Logaritma 1', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def logaritma_konu_2(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Logaritma2"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Logaritma 2', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def logaritma_konu_3(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Logaritma3"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Logaritma 3', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def logaritma_konu_4(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Logaritma4"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Logaritma 4', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def logaritma_konu_5(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Logaritma5"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Logaritma 5', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def logaritma_konu_6(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Logaritma6"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Logaritma 6', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def cebir_konu_1(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Cebir1"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Cebir 1', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def cebir_konu_2(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Cebir2"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Cebir 2', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def trigonometri_konu_1(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Trigonometri1"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Trigonometri 1', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()

    def trigonometri_konu_2(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ders = 'Matematik'
        konu = "Trigonometri2"
        f = open('video_info.txt', 'w')
        f.write(konu)
        f.close()
        f = open('lesson_info.txt', 'w')
        f.write(ders)
        f.close()
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO son_izlenenler VALUES ({self.school_number}, 'Trigonometri 2', '{now}')")
        conn.commit()
        conn.close()
        subprocess.run(['python', 'video_player.py'])
        self.last_views_frame_refresh()
        self.completed_quizzes_refresh()
        self.global_ranking_refresh()


    def get_student_ranking(self):
        conn = DbConnection().get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT ogr_no, basarim_puani from ogrenci ORDER BY basarim_puani DESC")
        records = cursor.fetchall()
        school_number_sort = []
        for record in records:
            school_number_sort.append(record[0])
        print(school_number_sort)
        rank = 1
        for student in school_number_sort:
            if int(student) != int(self.school_number):
                rank += 1
            else:
                break
        return rank
            


if __name__ == "__main__":
    ui = MainWindow("Selim Can ASLAN", 9929, 12, 500)
    ui.main_window.mainloop()