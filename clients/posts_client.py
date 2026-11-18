"""Cliente de endpoints REST para posts."""
from playwright.sync_api import APIRequestContext, APIResponse


class PostsClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    def list_posts(self, user_id: int | None = None) -> APIResponse:
        params = {"userId": user_id} if user_id is not None else None
        return self.request.get("/posts", params=params)

    def get_post(self, post_id: int) -> APIResponse:
        return self.request.get(f"/posts/{post_id}")

    def create_post(self, payload: dict) -> APIResponse:
        return self.request.post("/posts", data=payload)

    def replace_post(self, post_id: int, payload: dict) -> APIResponse:
        return self.request.put(f"/posts/{post_id}", data=payload)

    def update_post(self, post_id: int, payload: dict) -> APIResponse:
        return self.request.patch(f"/posts/{post_id}", data=payload)

    def delete_post(self, post_id: int) -> APIResponse:
        return self.request.delete(f"/posts/{post_id}")
