"""Cobertura REST de contrato, CRUD simulado e cenários negativos."""

from http import HTTPStatus

import pytest

from clients.posts_client import PostsClient

EXISTING_POST_ID = 1
USER_ID = 1


def assert_post_contract(post: dict) -> None:
    assert isinstance(post, dict)
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str) and post["title"]
    assert isinstance(post["body"], str) and post["body"]


def assert_payload_echoed(body: dict, payload: dict) -> None:
    """Confere que a API devolveu cada campo enviado sem alteração."""
    for field, expected in payload.items():
        assert body[field] == expected, f"campo '{field}' divergente"


@pytest.mark.smoke
@pytest.mark.contract
def test_listar_posts(posts_client: PostsClient):
    response = posts_client.list_posts()

    assert response.status == HTTPStatus.OK
    posts = response.json()
    assert isinstance(posts, list) and posts
    assert_post_contract(posts[0])


@pytest.mark.smoke
@pytest.mark.contract
@pytest.mark.parametrize("post_id", [1, 2, 3, 10])
def test_consultar_posts_por_id(posts_client: PostsClient, post_id: int):
    response = posts_client.get_post(post_id)

    assert response.status == HTTPStatus.OK
    post = response.json()
    assert_post_contract(post)
    assert post["id"] == post_id


@pytest.mark.regression
def test_filtrar_posts_por_usuario(posts_client: PostsClient):
    response = posts_client.list_posts(user_id=USER_ID)

    assert response.status == HTTPStatus.OK
    posts = response.json()
    assert posts and all(post["userId"] == USER_ID for post in posts)


@pytest.mark.negative
@pytest.mark.parametrize("post_id", [0, 999_999])
def test_post_inexistente(posts_client: PostsClient, post_id: int):
    response = posts_client.get_post(post_id)

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.json() == {}


@pytest.mark.smoke
@pytest.mark.regression
def test_criar_post_simulado(posts_client: PostsClient):
    payload = {"title": "Teste QA", "body": "Automacao com Playwright", "userId": USER_ID}

    response = posts_client.create_post(payload)

    assert response.status == HTTPStatus.CREATED
    body = response.json()
    assert isinstance(body["id"], int)
    assert_payload_echoed(body, payload)


@pytest.mark.regression
def test_substituir_post_simulado(posts_client: PostsClient):
    payload = {
        "id": EXISTING_POST_ID,
        "title": "Titulo substituido",
        "body": "Novo corpo",
        "userId": USER_ID,
    }

    response = posts_client.replace_post(EXISTING_POST_ID, payload)

    assert response.status == HTTPStatus.OK
    assert_payload_echoed(response.json(), payload)


@pytest.mark.regression
def test_atualizar_post_parcialmente(posts_client: PostsClient):
    payload = {"title": "Novo titulo de QA"}

    response = posts_client.update_post(EXISTING_POST_ID, payload)

    assert response.status == HTTPStatus.OK
    body = response.json()
    assert_payload_echoed(body, payload)
    assert body["id"] == EXISTING_POST_ID


@pytest.mark.regression
def test_excluir_post_simulado(posts_client: PostsClient):
    response = posts_client.delete_post(EXISTING_POST_ID)

    # A JSONPlaceholder responde 200, mas não persiste a exclusão.
    assert response.status == HTTPStatus.OK
