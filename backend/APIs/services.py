from database import get_connection


def create_user(nome: str, email: str, senha: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (
            nome,
            email,
            senha
        )
        VALUES (?, ?, ?)
        """, (nome, email, senha))

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def create_post(autor_id: int, conteudo: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO posts (
            autor_id,
            conteudo
        )
        VALUES (?, ?)
        """,(autor_id, conteudo))

    connection.commit()

    post_id = cursor.lastrowid

    connection.close()

    return post_id


def like_post(user_id: int, post_id: int):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO likes (
            user_id,
            post_id
        )
        VALUES (?, ?)
        """,
        (user_id, post_id))

    connection.commit()

    connection.close()


def follow_user(follower_id: int,following_id: int):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO follows (
            follower_id,
            following_id
        )
        VALUES (?, ?)
        """,
        (follower_id,following_id))

    connection.commit()

    connection.close()


def create_comment(autor_id: int, post_id: int, conteudo: str):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO comments (
            autor_id,
            post_id,
            conteudo
        )
        VALUES (?, ?, ?)
        """,
        (autor_id, post_id, conteudo))

    connection.commit()

    comment_id = cursor.lastrowid

    connection.close()

    return comment_id

