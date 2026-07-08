import sqlite3


DB = "yuka.db"


def connect():

    return sqlite3.connect(DB)



def create():

    con = connect()

    cur = con.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory(

        user_id TEXT,
        text TEXT

    )
    """)


    con.commit()

    con.close()



def add_memory(user_id,text):

    con = connect()

    cur = con.cursor()


    cur.execute(
        "INSERT INTO memory VALUES (?,?)",
        (
            user_id,
            text
        )
    )


    con.commit()

    con.close()



def get_memory(user_id):

    con = connect()

    cur = con.cursor()


    cur.execute(
        "SELECT text FROM memory WHERE user_id=?",
        (user_id,)
    )


    data = cur.fetchall()


    con.close()


    return [
        x[0] for x in data
    ]