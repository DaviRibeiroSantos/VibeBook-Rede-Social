from fastapi import FastAPI
from fastapi import HTTPException

from database import get_connection
from database import init_database

from models import User
from models import UserCreate
from models import Post
from models import PostCreate
from models import Comment
from models import CommentCreate
from models import Config

from services import create_user
from services import create_post
from services import like_post
from services import follow_user
from services import create_comment


app = FastAPI()


init_database()


def build_user(user_id: int):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    if user is None:

        connection.close()

        return None

    followers = connection.execute(
        """
        SELECT follower_id
        FROM follows
        WHERE following_id = ?
        """,
        (user_id,)
    ).fetchall()

    following = connection.execute(
        """
        SELECT following_id
        FROM follows
        WHERE follower_id = ?
        """,
        (user_id,)
    ).fetchall()

    liked_posts = connection.execute(
        """
        SELECT post_id
        FROM likes
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return User(
        id=user["id"],
        nome=user["nome"],
        email=user["email"],

        configuracoes=Config(
            tema=user["tema"],
            notificacoes=bool(user["notificacoes"])
        ),

        seguidores=[
            follower["follower_id"]
            for follower in followers
        ],

        seguindo=[
            following_user["following_id"]
            for following_user in following
        ],

        posts_liked=[
            post["post_id"]
            for post in liked_posts
        ]
    )


def build_post(post_id: int):

    connection = get_connection()

    post = connection.execute(
        """
        SELECT *
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    ).fetchone()

    if post is None:

        connection.close()

        return None

    likes = connection.execute(
        """
        SELECT COUNT(*)
        FROM likes
        WHERE post_id = ?
        """,
        (post_id,)
    ).fetchone()[0]

    comments = connection.execute(
        """
        SELECT id
        FROM comments
        WHERE post_id = ?
        """,
        (post_id,)
    ).fetchall()

    connection.close()

    return Post(
        id=post["id"],
        autor_id=post["autor_id"],
        conteudo=post["conteudo"],
        likes=likes,
        compartilhamentos=post["compartilhamentos"],
        comentarios=[
            comment["id"]
            for comment in comments
        ]
    )


def build_comment(comment_id: int):

    connection = get_connection()

    comment = connection.execute(
        """
        SELECT *
        FROM comments
        WHERE id = ?
        """,
        (comment_id,)
    ).fetchone()

    connection.close()

    if comment is None:
        return None

    return Comment(
        id=comment["id"],
        autor_id=comment["autor_id"],
        post_id=comment["post_id"],
        conteudo=comment["conteudo"]
    )



# USERS
@app.get(
    "/users",
    response_model=list[User]
)
def get_users():

    connection = get_connection()

    users = connection.execute(
        """
        SELECT id
        FROM users
        """
    ).fetchall()

    connection.close()

    return [
        build_user(user["id"])
        for user in users
    ]


@app.get(
    "/user/{user_id}",
    response_model=User
)
def get_user(user_id: int):

    user = build_user(user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return user


@app.post(
    "/user",
    response_model=User
)
def post_user(user: UserCreate):

    try:

        user_id = create_user(
            user.nome,
            user.email,
            user.senha
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o usuário"
        )

    return build_user(user_id)



# POSTS
@app.get(
    "/posts",
    response_model=list[Post]
)
def get_posts():

    connection = get_connection()

    posts = connection.execute(
        """
        SELECT id
        FROM posts
        """
    ).fetchall()

    connection.close()

    return [
        build_post(post["id"])
        for post in posts
    ]


@app.get(
    "/post/{post_id}",
    response_model=Post
)
def get_post(post_id: int):

    post = build_post(post_id)

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post não encontrado"
        )

    return post


@app.post(
    "/post/{user_id}",
    response_model=Post
)
def post_content(
    user_id: int,
    post: PostCreate
):

    user = build_user(user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    post_id = create_post(
        user_id,
        post.conteudo
    )

    return build_post(post_id)



# LIKES
@app.post(
    "/post/{post_id}/like/{user_id}",
    response_model=Post
)
def like(
    post_id: int,
    user_id: int
):

    if build_user(user_id) is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if build_post(post_id) is None:

        raise HTTPException(
            status_code=404,
            detail="Post não encontrado"
        )

    try:

        like_post(
            user_id,
            post_id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Usuário já curtiu esse post"
        )

    return build_post(post_id)



# FOLLOWERS
@app.post(
    "/user/{user_id}/follow/{target_id}"
)
def follow(
    user_id: int,
    target_id: int
):

    if build_user(user_id) is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if build_user(target_id) is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário alvo não encontrado"
        )

    if user_id == target_id:

        raise HTTPException(
            status_code=400,
            detail="Você não pode seguir a si mesmo"
        )

    try:

        follow_user(
            user_id,
            target_id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Você já segue esse usuário"
        )

    return {
        "message": "Usuário seguido com sucesso"
    }



# COMMENTS
@app.get(
    "/comment/{comment_id}",
    response_model=Comment
)
def get_comment(comment_id: int):

    comment = build_comment(comment_id)

    if comment is None:

        raise HTTPException(
            status_code=404,
            detail="Comentário não encontrado"
        )

    return comment


@app.post(
    "/post/{post_id}/comment/{user_id}",
    response_model=Comment
)
def post_comment(
    post_id: int,
    user_id: int,
    comment: CommentCreate
):

    if build_user(user_id) is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    if build_post(post_id) is None:

        raise HTTPException(
            status_code=404,
            detail="Post não encontrado"
        )

    comment_id = create_comment(
        user_id,
        post_id,
        comment.conteudo
    )

    return build_comment(comment_id)



# CONFIGURAÇÕES
@app.get(
    "/user/{user_id}/config",
    response_model=Config
)
def get_config(user_id: int):

    user = build_user(user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return user.configuracoes


@app.put(
    "/user/{user_id}/config",
    response_model=Config
)
def update_config(
    user_id: int,
    config: Config
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET tema = ?,
            notificacoes = ?
        WHERE id = ?
        """,
        (
            config.tema,
            int(config.notificacoes),
            user_id
        )
    )

    if cursor.rowcount == 0:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    connection.commit()
    connection.close()

    return config

