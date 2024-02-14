import pyodbc

class DbConnection:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        driver = "SQL SERVER"
        server = "SCA\SQLEXPRESS"
        db = "online_dershane"
        self.connection_string = f"""
                DRIVER={{{driver}}};
                SERVER={server};
                DATABASE={db};
                Trust_Connection=yes;
                """

    def get_conn(self):
        conn = pyodbc.connect(self.connection_string)
        return conn

    def fetch_major(self):
        major_list = []
        conn = self.get_conn()
        cursor = conn.cursor()
        query = cursor.execute(""" SELECT * FROM alan """)
        majors = query.fetchall()
        for i in majors:
            major_list.append(i[1])
        return major_list

    def fetch_class(self):
        class_list = []
        conn = self.get_conn()
        cursor = conn.cursor()
        query = cursor.execute(""" SELECT * FROM sinif """)
        classes = query.fetchall()
        for i in classes:
            class_list.append(i[1])
        return class_list

    def get_student_name(self, number):
        school_number = number
        conn = self.get_conn()
        cursor = conn.cursor()
        query = cursor.execute(f" SELECT ogr_ad + ' ' + ogr_soyad FROM ogrenci WHERE ogr_no = {school_number} ")
        name = query.fetchall()
        return name[0][0]

    def fetch_one_user(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        query = cursor.execute(" SELECT * FROM ogr_login")
        print(query.fetchone())
        
