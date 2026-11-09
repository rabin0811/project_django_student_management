import pytest
from django.urls import reverse
from rest_framework import status
from students.models import Student


@pytest.fixture
def student(db):
    return Student.objects.create(
        name="Test Student",
        email="test@example.com",
        age=22,
        course="CS",
    )


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


class TestStudentListAPI:
    def test_list_students(self, api_client, student):
        url = reverse("student-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "Test Student"

    def test_empty_list(self, api_client, db):
        url = reverse("student-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0


class TestStudentCreateAPI:
    def test_create_student(self, api_client, db):
        url = reverse("student-list")
        data = {"name": "New", "email": "new@test.com", "age": 20, "course": "MATH"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New"

    def test_create_invalid(self, api_client, db):
        url = reverse("student-list")
        response = api_client.post(url, {"name": ""}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestStudentDetailAPI:
    def test_get_student(self, api_client, student):
        url = reverse("student-detail", args=[student.pk])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "test@example.com"

    def test_get_404(self, api_client, db):
        url = reverse("student-detail", args=[999])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestStudentUpdateAPI:
    def test_put_student(self, api_client, student):
        url = reverse("student-detail", args=[student.pk])
        data = {"name": "Updated", "email": student.email, "age": 25, "course": "ENG"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated"

    def test_patch_student(self, api_client, student):
        url = reverse("student-detail", args=[student.pk])
        response = api_client.patch(url, {"age": 30}, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["age"] == 30


class TestStudentDeleteAPI:
    def test_delete_student(self, api_client, student):
        url = reverse("student-detail", args=[student.pk])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Student.objects.filter(pk=student.pk).exists()


class TestStudentFilterAPI:
    def test_filter_by_course(self, api_client, db):
        Student.objects.create(name="A", email="a@a.com", age=20, course="CS")
        Student.objects.create(name="B", email="b@b.com", age=21, course="MATH")
        url = reverse("student-list")
        response = api_client.get(url, {"course": "CS"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == "A"

    def test_search_by_name(self, api_client, db):
        Student.objects.create(name="Alice", email="alice@a.com", age=20, course="CS")
        Student.objects.create(name="Bob", email="bob@b.com", age=22, course="MATH")
        url = reverse("student-list")
        response = api_client.get(url, {"search": "Alice"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1


class TestStudentSerializer:
    def test_course_display_field(self, api_client, db):
        student = Student.objects.create(
            name="Sam", email="sam@t.com", age=19, course="BIO"
        )
        url = reverse("student-detail", args=[student.pk])
        response = api_client.get(url)
        assert response.data["course_display"] == "Biology"
