import pytest
from students.models import Student


class TestStudentModel:
    def test_create_student(self, db):
        student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            age=20,
            course="CS",
        )
        assert student.pk is not None
        assert str(student) == "John Doe"
        assert student.get_course_display() == "Computer Science"

    def test_email_unique(self, db):
        Student.objects.create(name="Alice", email="a@b.com", age=21, course="ENG")
        with pytest.raises(Exception):
            Student.objects.create(name="Bob", email="a@b.com", age=22, course="MATH")

    def test_get_absolute_url(self, db):
        student = Student.objects.create(
            name="Jane", email="jane@test.com", age=19, course="BIO"
        )
        url = student.get_absolute_url()
        assert url == f"/students/{student.pk}/"

    def test_default_enrollment_date(self, db):
        from datetime import date
        student = Student.objects.create(
            name="Sam", email="sam@test.com", age=23, course="PHY"
        )
        assert student.enrollment_date == date.today()
