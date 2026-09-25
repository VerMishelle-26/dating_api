from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Like

User = get_user_model()


class LikeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="u1", email="u1@test.com", password="pass12345",
            first_name="Иван", last_name="Иванов", age=25
        )
        self.user2 = User.objects.create_user(
            username="u2", email="u2@test.com", password="pass12345",
            first_name="Мария", last_name="Петрова", age=23
        )

    def test_create_like(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post("/api/interactions/likes/", {
            "to_user": self.user2.id, "type": "like"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_create_dislike(self):
        self.client.force_authenticate(self.user1)
        response = self.client.post("/api/interactions/likes/", {
            "to_user": self.user2.id, "type": "dislike"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.first().type, "dislike")

    def test_unique_like(self):
        self.client.force_authenticate(self.user1)


        response1 = self.client.post("/api/interactions/likes/", {
            "to_user": self.user2.id,
            "type": "like",
        })
        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post("/api/interactions/likes/", {
            "to_user": self.user2.id,
            "type": "like",
        })
        self.assertNotEqual(response2.status_code, 201)

    def test_liked_list(self):
        Like.objects.create(from_user=self.user1, to_user=self.user2, type="like")
        self.client.force_authenticate(self.user1)
        response = self.client.get("/api/interactions/likes/liked/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_like(self):
        response = self.client.post("/api/interactions/likes/", {
            "to_user": self.user2.id, "type": "like"
        })
        self.assertEqual(response.status_code, 401)