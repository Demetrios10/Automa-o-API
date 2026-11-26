"""Cliente de endpoints REST para o recurso ``/posts``."""

from playwright.sync_api import APIRequestContext, APIResponse

POSTS_ENDPOINT = "/posts"

Payload = dict[str, object]


class PostsClient:
    """Encapsula as chamadas HTTP do recurso de posts."""

    def __init__(self, request: APIRequestContext) -> None:
        self.request = request

    @staticmethod
    def _post_url(post_id: int) -> str:
        return f"{POSTS_ENDPOINT}/{post_id}"

    def list_posts(self, user_id: int | None = None) -> APIResponse:
        params = {"userId": user_id} if user_id is not None else None
        return self.request.get(POSTS_ENDPOINT, params=params)

    def get_post(self, post_id: int) -> APIResponse:
        return self.request.get(self._post_url(post_id))

    def create_post(self, payload: Payload) -> APIResponse:
        return self.request.post(POSTS_ENDPOINT, data=payload)

    def replace_post(self, post_id: int, payload: Payload) -> APIResponse:
        return self.request.put(self._post_url(post_id), data=payload)

    def update_post(self, post_id: int, payload: Payload) -> APIResponse:
        return self.request.patch(self._post_url(post_id), data=payload)

    def delete_post(self, post_id: int) -> APIResponse:
        return self.request.delete(self._post_url(post_id))
