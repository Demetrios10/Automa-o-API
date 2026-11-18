"""Cobertura REST de contrato, CRUD simulado e cenários negativos."""
import pytest

from clients.posts_client import PostsClient


def assert_post_contract(post: dict) -> None:
    assert isinstance(post, dict)
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str) and post["title"]
    assert isinstance(post["body"], str) and post["body"]


@pytest.mark.smoke
@pytest.mark.contract
def test_listar_posts(posts_client: PostsClient):
    response = posts_client.list_posts()
    assert response.status == 200
    posts = response.json()
    assert isinstance(posts, list) and posts
    assert_post_contract(posts[0])


@pytest.mark.smoke
@pytest.mark.contract
@pytest.mark.parametrize("post_id", [1, 2, 3, 10])
def test_consultar_posts_por_id(posts_client: PostsClient, post_id: int):
    response = posts_client.get_post(post_id)
    assert response.status == 200
    post = response.json()
    assert_post_contract(post)
    assert post["id"] == post_id


@pytest.mark.regression
def test_filtrar_posts_por_usuario(posts_client: PostsClient):
    response = posts_client.list_posts(user_id=1)
    assert response.status == 200
    posts = response.json()
    assert posts and all(post["userId"] == 1 for post in posts)


@pytest.mark.negative
@pytest.mark.parametrize("post_id", [0, 999999])
def test_post_inexistente(posts_client: PostsClient, post_id: int):
    response = posts_client.get_post(post_id)
    assert response.status == 404
    assert response.json() == {}


@pytest.mark.smoke
@pytest.mark.regression
def test_criar_post_simulado(posts_client: PostsClient):
    payload = {"title": "Teste QA", "body": "Automacao com Playwright", "userId": 1}
    response = posts_client.create_post(payload)
    assert response.status == 201
    body = response.json()
    assert isinstance(body["id"], int)
    for field, expected in payload.items():
        assert body[field] == expected


@pytest.mark.regression
def test_substituir_post_simulado(posts_client: PostsClient):
    payload = {"id": 1, "title": "Titulo substituido", "body": "Novo corpo", "userId": 1}
    response = posts_client.replace_post(1, payload)
    assert response.status == 200
    body = response.json()
    for field, expected in payload.items():
        assert body[field] == expected


@pytest.mark.regression
def test_atualizar_post_parcialmente(posts_client: PostsClient):
    response = posts_client.update_post(1, {"title": "Novo titulo de QA"})
    assert response.status == 200
    assert response.json()["title"] == "Novo titulo de QA"
    assert response.json()["id"] == 1


@pytest.mark.regression
def test_excluir_post_simulado(posts_client: PostsClient):
    response = posts_client.delete_post(1)
    assert response.status == 200
    # DELETE não persiste na JSONPlaceholder.
