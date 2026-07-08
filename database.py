import sqlite3


DB = "yuka.db"



def connect():

    return sqlite3.connect(DB)



def setup():

    con = connect()

    cur = con.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory(
        user_id TEXT,
        text TEXT
    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id TEXT PRIMARY KEY,
        money INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    )
    """)



    con.commit()

    con.close()



def add_memory(uid,text):

    con = connect()

    cur = con.cursor()


    cur.execute(
        "INSERT INTO memory VALUES (?,?)",
        (
            uid,
            text
        )
    )


    con.commit()

    con.close()



def get_memory(uid):

    con = connect()

    cur = con.cursor()


    cur.execute(
        "SELECT text FROM memory WHERE user_id=?",
        (uid,)
    )


    data = cur.fetchall()


    con.close()


    return [
        x[0]
        for x in data
    ]



def create_user(uid):

    con = connect()

    cur = con.cursor()


    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id)
        VALUES (?)
        """,
        (uid,)
    )


    con.commit()

    con.close()



def get_user(uid):

    create_user(uid)


    con = connect()

    cur = con.cursor()


    cur.execute(
        """
        SELECT money,xp,level
        FROM users
        WHERE user_id=?
        """,
        (uid,)
    )


    data = cur.fetchone()


    con.close()


    return data



def add_xp(uid,amount):

    money,xp,level = get_user(uid)


    xp += amount


    if xp >= level*100:

        xp = 0
        level += 1


    con = connect()

    cur = con.cursor()


    cur.execute(
        """
        UPDATE users
        SET xp=?, level=?
        WHERE user_id=?
        """,
        (
            xp,
            level,
            uid
        )
    )


    con.commit()

    con.close()