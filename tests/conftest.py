"""Fixtures para contexto HTTP, sem navegador."""

import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright

from clients.posts_client import PostsClient

load_dotenv()

DEFAULT_BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_TIMEOUT_MS = 10_000


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Iterator[APIRequestContext]:
    context = playwright.request.new_context(
        base_url=os.getenv("BASE_URL", DEFAULT_BASE_URL),
        extra_http_headers={"Accept": "application/json"},
        timeout=int(os.getenv("API_TIMEOUT_MS", str(DEFAULT_TIMEOUT_MS))),
    )
    yield context
    context.dispose()


@pytest.fixture
def posts_client(api_context: APIRequestContext) -> PostsClient:
    return PostsClient(api_context)
