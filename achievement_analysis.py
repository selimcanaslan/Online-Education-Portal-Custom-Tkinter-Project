import customtkinter
from db_connection import DbConnection

class Analysis:
    def __init__(self, lesson_name, student_number):
        conn =DbConnection().get_conn()
        crsr = conn.cursor()
        crsr.execute
