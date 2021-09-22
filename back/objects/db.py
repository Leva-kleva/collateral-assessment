import sqlite3

conn = sqlite3.connect("objects/objects.db", check_same_thread=False)
cursor = conn.cursor()

# cursor.execute("""CREATE TABLE cars
#                   (mark text, Model text, Generation text)
#                   ;
#                """)


def do_list(obj):
    ans = []
    for el in obj:
        ans.append(el[0])
    return ans


def get_mark():
    a = cursor.execute("""SELECT mark FROM cars GROUP BY mark;""")
    return do_list(a.fetchall())


def get_model(mark):
    a = cursor.execute("""SELECT model FROM cars WHERE mark='{0}' GROUP BY model;""".format(mark))
    return do_list(a.fetchall())


def get_generation(mark, model):
    a = cursor.execute(
        """SELECT generation FROM cars WHERE mark='{0}' and model='{1}' GROUP BY generation;""".format(mark, model))
    return do_list(a.fetchall())
