import pytest
from django.urls import reverse
from students.models import Student


@pytest.fixture
def student(db):
    return Student.objects.create(
        name="Test Student",
        email="test@example.com",
        age=22,
        course="CS",
    )


class TestStudentListView:
    def test_get(self, client, student):
        url = reverse("students:list")
        response = client.get(url)
        assert response.status_code == 200
        assert "student_list" in response.context
        assert student in response.context["student_list"]

    def test_empty_list(self, db, client):
        url = reverse("students:list")
        response = client.get(url)
        assert response.status_code == 200
        assert list(response.context["student_list"]) == []


class TestStudentCreateView:
    def test_get_form(self, client):
        url = reverse("students:create")
        response = client.get(url)
        assert response.status_code == 200

    def test_post_valid(self, db, client):
        url = reverse("students:create")
        data = {
            "name": "New Student",
            "email": "new@example.com",
            "age": 20,
            "course": "MATH",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert Student.objects.filter(email="new@example.com").exists()

    def test_post_invalid(self, client):
        url = reverse("students:create")
        response = client.post(url, {"name": "", "email": "bad", "age": -1, "course": ""})
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].errors


class TestStudentDetailView:
    def test_get(self, client, student):
        url = reverse("students:detail", args=[student.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["student"] == student

    def test_404(self, db, client):
        url = reverse("students:detail", args=[999])
        response = client.get(url)
        assert response.status_code == 404


class TestStudentUpdateView:
    def test_get_form(self, client, student):
        url = reverse("students:update", args=[student.pk])
        response = client.get(url)
        assert response.status_code == 200

    def test_post_valid(self, client, student):
        url = reverse("students:update", args=[student.pk])
        data = {
            "name": "Updated Name",
            "email": student.email,
            "age": 25,
            "course": "ENG",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        student.refresh_from_db()
        assert student.name == "Updated Name"

    def test_post_invalid(self, client, student):
        url = reverse("students:update", args=[student.pk])
        response = client.post(url, {"name": "", "email": "", "age": -1, "course": ""})
        assert response.status_code == 200


class TestStudentDeleteView:
    def test_get_confirm(self, client, student):
        url = reverse("students:delete", args=[student.pk])
        response = client.get(url)
        assert response.status_code == 200

    def test_post_delete(self, client, student):
        url = reverse("students:delete", args=[student.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse("students:list")
        assert not Student.objects.filter(pk=student.pk).exists()

    def test_delete_404(self, db, client):
        url = reverse("students:delete", args=[999])
        response = client.post(url)
        assert response.status_code == 404
