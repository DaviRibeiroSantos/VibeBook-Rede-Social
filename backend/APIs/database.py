import sqlite3


DATABASE = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tema TEXT NOT NULL DEFAULT 'dark',
            notificacoes INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor_id INTEGER NOT NULL,
            conteudo TEXT NOT NULL,
            compartilhamentos INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (autor_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,

            PRIMARY KEY (user_id, post_id),

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (post_id)
                REFERENCES posts(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS follows (
            follower_id INTEGER NOT NULL,
            following_id INTEGER NOT NULL,

            PRIMARY KEY (follower_id, following_id),

            FOREIGN KEY (follower_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (following_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            conteudo TEXT NOT NULL,

            FOREIGN KEY (autor_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (post_id)
                REFERENCES posts(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


def get_user_by_id(user_id: int):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user


def get_post_by_id(post_id: int):

    connection = get_connection()

    post = connection.execute(
        """
        SELECT *
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    ).fetchone()

    connection.close()

    return post

