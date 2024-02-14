from info_message import InfoMessage
import datetime
import tkinter as tk
from tkVideoPlayer import TkinterVideo
import customtkinter
from PIL import Image
import sys
from konular import Konu
from quiz import Quiz
import os

RES = [1600, 900]
playet_text_font = ("Tahoma", 14, "bold")

f = open('video_info.txt', 'r')
video_name = f.read()
video_path = Konu().konu_yolla(video_name)
f.close()

f = open('lesson_info.txt', 'r')
lesson_name = f.read()
f.close()

def update_duration(event):
    duration = vid_player.video_info()["duration"]
    end_time.configure(text=str(datetime.timedelta(seconds=duration)))
    progress_slider["to"] = duration

def update_scale(event):
    duration = vid_player.video_info()["duration"]
    progress_value.set(vid_player.current_duration())
    start_time.configure(text=str(datetime.timedelta(seconds=vid_player.current_duration() + 1))[:7])
    end_time.configure(text=str(datetime.timedelta(seconds= duration - vid_player.current_duration()))[:7])

def load_video(video_path):
    vid_player.load(video_path)

    progress_slider.configure(to=0, from_=0)
    play_pause_btn.configure(text="Play")
    progress_value.set(0)

def seek(value):
    vid_player.seek(int(value))

def skip(value: int):
    vid_player.seek(int(progress_slider.get()) + value)
    progress_value.set(progress_slider.get() + value)

def play_pause():
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn.configure(text="Pause")
        play_pause_btn.configure(image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\pause.png"),
                                                    dark_image=Image.open(r"assets\video_player\pause.png")))
    else:
        vid_player.pause()
        play_pause_btn.configure(text="Play")
        play_pause_btn.configure(image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\play.png"),
                                                    dark_image=Image.open(r"assets\video_player\play.png")))

def exit_window():
    vid_player.pause()
    play_pause_btn.configure(text="Play")
    play_pause_btn.configure(image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\play.png"),
                                            dark_image=Image.open(r"assets\video_player\play.png")))
    response = InfoMessage("Videoyu kapatmak istediğine emin misin ?").ask_question()
    if response:
        root.destroy()
    else:
        vid_player.play()
        play_pause_btn.configure(text="Pause")
        play_pause_btn.configure(image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\pause.png"),
                                                    dark_image=Image.open(r"assets\video_player\pause.png")))

def video_end_exit():
        root.destroy()

def open_quiz_window():
    if os.path.exists(f"assets/quiz/{video_name}.json"):
        Quiz(video_name, lesson_name)
    else:
        InfoMessage("Bu videonun Quiz'i henüz eklenmemiş.").show_error()
        
def video_ended(event):
    progress_slider.set(progress_slider["to"])
    play_pause_btn.configure(text="Play")
    progress_slider.set(0)
    end_time.configure(text=str(datetime.timedelta(seconds=0)))
    for widgets in root.winfo_children():
            widgets.destroy()

    video_end_text = customtkinter.CTkLabel(master=root, text="VIDEO SONA ERDİ", font=("Tahoma", 50, "bold"))
    video_end_text.pack(fill='both')

    quiz_button = customtkinter.CTkButton(master=root, text="Video Quizini Çöz", font=("Tahoma", 50, "bold"), command=open_quiz_window)
    quiz_button.pack(fill='both', expand=True)

    exit_button = customtkinter.CTkButton(master=root, text="Çıkış Yap", command=video_end_exit, font=("Tahoma", 50, "bold"))
    exit_button.pack(fill='both', expand=True)

def truncate_video_info():
    f = open("video_info.txt", "w")
    f.close()



root = customtkinter.CTk()
root.title(" ")
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
RES[0] = int(ws * 3 / 4)
RES[1] = int(hs * 3 / 4)
root.attributes("-fullscreen", "True")
x = (ws / 2) - (RES[0] / 2)
y = (hs / 2) - (RES[1] / 2)
root.geometry('%dx%d+%d+%d' % (RES[0], RES[1], x, y))
root.minsize(RES[0], RES[1])
root.maxsize(RES[0], RES[1])

vid_player = TkinterVideo(scaled=True, master=root)
vid_player.pack(expand=True, fill="both")

play_pause_btn = customtkinter.CTkButton(master=root,
                                          text="Play",
                                            fg_color= "#212121",
                                                width=80,
                                                font= playet_text_font,
                                                    command=play_pause,
                                                        image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\play.png"),
                                                            dark_image=Image.open(r"assets\video_player\play.png")))
play_pause_btn.pack(side='left', padx=2)

exit_button = customtkinter.CTkButton(master=root, font= playet_text_font, fg_color= "#212121", text="Exit", width=50, command=exit_window)
exit_button.pack(side='left', padx=2)

skip_minus_5sec = customtkinter.CTkButton(master=root, font= playet_text_font, text="", fg_color= "#212121", width=50, image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\backward.png"),
                                                    dark_image=Image.open(r"assets\video_player\backward.png")), command=lambda: skip(-5))
skip_minus_5sec.pack(side="left", padx=2)

skip_plus_5sec = customtkinter.CTkButton(master=root, font= playet_text_font, text="", width=50, fg_color= "#212121", image=customtkinter.CTkImage(light_image=Image.open(r"assets\video_player\forward.png"),
                                                    dark_image=Image.open(r"assets\video_player\forward.png")), command=lambda: skip(5))
skip_plus_5sec.pack(side="left", padx=2)

start_time = customtkinter.CTkLabel(root, font= playet_text_font, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left", padx=2)

progress_value = tk.IntVar(master=root)

progress_slider = tk.Scale(master=root,
                           variable=progress_value,
                           showvalue=False,
                           from_=0, to=0,
                           orient="horizontal",
                           background="green",
                           troughcolor="#212121", borderwidth=0,
                           command=seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = customtkinter.CTkLabel(master=root, font= playet_text_font, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended )

def close(event):
    root.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing

root.bind('<Escape>', close)

load_video(video_path)
play_pause()
root.mainloop()
