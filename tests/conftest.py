"""Fixtures para contexto HTTP, sem navegador."""
import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, APIRequestContext

from clients.posts_client import PostsClient

load_dotenv()


@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> APIRequestContext:
    base_url = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    timeout_ms = int(os.getenv("API_TIMEOUT_MS", "10000"))
    context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"Accept": "application/json"},
        timeout=timeout_ms,
    )
    yield context
    context.dispose()


@pytest.fixture
def posts_client(api_context: APIRequestContext) -> PostsClient:
    return PostsClient(api_context)
