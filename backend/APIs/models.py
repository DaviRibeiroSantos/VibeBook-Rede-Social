from pydantic import BaseModel


class Config(BaseModel):

    tema: str = "dark"
    notificacoes: bool = True


class UserCreate(BaseModel):

    nome: str
    email: str
    senha: str


class User(BaseModel):

    id: int
    nome: str
    email: str

    configuracoes: Config

    seguidores: list[int]
    seguindo: list[int]

    posts_liked: list[int]


class PostCreate(BaseModel):

    conteudo: str


class Post(BaseModel):

    id: int
    autor_id: int
    conteudo: str

    likes: int
    compartilhamentos: int

    comentarios: list[int]


class CommentCreate(BaseModel):

    conteudo: str


class Comment(BaseModel):

    id: int
    autor_id: int
    post_id: int
    conteudo: str

