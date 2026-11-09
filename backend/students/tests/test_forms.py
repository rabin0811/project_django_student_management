from students.forms import StudentForm


class TestStudentForm:
    def test_valid_data(self, db):
        form = StudentForm(data={
            "name": "Alice",
            "email": "alice@example.com",
            "age": 21,
            "course": "CS",
        })
        assert form.is_valid()

    def test_blank_name(self, db):
        form = StudentForm(data={
            "name": "",
            "email": "a@b.com",
            "age": 20,
            "course": "ENG",
        })
        assert not form.is_valid()
        assert "name" in form.errors

    def test_invalid_email(self):
        form = StudentForm(data={
            "name": "Bob",
            "email": "not-an-email",
            "age": 20,
            "course": "MATH",
        })
        assert not form.is_valid()
        assert "email" in form.errors

    def test_negative_age(self, db):
        form = StudentForm(data={
            "name": "Charlie",
            "email": "c@d.com",
            "age": -5,
            "course": "BIO",
        })
        assert not form.is_valid()
        assert "age" in form.errors

    def test_missing_course(self, db):
        form = StudentForm(data={
            "name": "Diana",
            "email": "d@e.com",
            "age": 22,
            "course": "",
        })
        assert not form.is_valid()
        assert "course" in form.errors

    def test_form_widgets(self):
        form = StudentForm()
        assert "form-control" in str(form.fields["name"].widget.attrs.get("class", ""))
        assert "form-select" in str(form.fields["course"].widget.attrs.get("class", ""))
