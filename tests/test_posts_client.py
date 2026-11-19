"""Testes unitários do roteamento HTTP, sem depender de uma API externa."""

from unittest.mock import Mock

import pytest

from clients.posts_client import PostsClient


@pytest.fixture
def request_mock():
    return Mock()


@pytest.fixture
def client(request_mock):
    return PostsClient(request_mock)


@pytest.mark.parametrize(
    ("user_id", "expected_params"),
    [(None, None), (0, {"userId": 0}), (1, {"userId": 1})],
)
def test_list_posts_preserva_filtro(client, request_mock, user_id, expected_params):
    response = client.list_posts(user_id=user_id)

    request_mock.get.assert_called_once_with("/posts", params=expected_params)
    assert response is request_mock.get.return_value


@pytest.mark.parametrize("post_id", [1, 42])
def test_get_post_usa_id_na_rota(client, request_mock, post_id):
    response = client.get_post(post_id)

    request_mock.get.assert_called_once_with(f"/posts/{post_id}")
    assert response is request_mock.get.return_value


@pytest.mark.parametrize(
    ("method", "client_method", "post_id", "payload"),
    [
        ("post", "create_post", None, {"title": "Teste", "userId": 1}),
        ("put", "replace_post", 4, {"title": "Atualizado"}),
        ("patch", "update_post", 4, {"title": "Parcial"}),
    ],
)
def test_escritas_enviam_payload(
    client, request_mock, method, client_method, post_id, payload
):
    endpoint = "/posts" if post_id is None else f"/posts/{post_id}"
    call = getattr(client, client_method)
    response = call(payload) if post_id is None else call(post_id, payload)

    getattr(request_mock, method).assert_called_once_with(endpoint, data=payload)
    assert response is getattr(request_mock, method).return_value


def test_delete_post_usa_id_na_rota(client, request_mock):
    response = client.delete_post(8)

    request_mock.delete.assert_called_once_with("/posts/8")
    assert response is request_mock.delete.return_value
