from urllib.parse import quote
from flask import url_for, request
from app.models import Login, ProfessorsNames, SubjectsNames


class TestViews():

    def login(self, client, email, password):
        return client.post(
            url_for("bp.login"),
            data=dict(
                Email_Address=email,
                Password=password),
            follow_redirects=True)

    def test_home(self, client):
        response = client.get(url_for("bp.home"))
        assert response.status_code == 200

    def test_signup(self, client):
        response = client.get(url_for("bp.signup"))
        assert response.status_code == 200
        response = client.post(
            url_for("bp.signup"),
            data=dict(
                Roll_Number=9999999998,
                Email_Address1="itest@test.com",
                Email_Address2="itest@test.com",
                Password1="password",
                Password2="password"),
            follow_redirects=True)
        assert response.status_code == 200
        assert request.path == url_for("bp.login")

        response = client.post(
            url_for("bp.signup"),
            data=dict(
                Roll_Number=0000000000,
                Email_Address1="admin@admin.com",
                Email_Address2="admin@admin.com",
                Password1="password",
                Password2="password"),
            follow_redirects=True)
        assert response.status_code == 200
        assert request.path == url_for("bp.signup")

    def test_login(self, client):
        response = client.get(url_for("bp.login"))
        assert response.status_code == 200
        response = self.login(client=client, email="admin@admin.com", password="password")
        assert response.status_code == 200
        response = self.login(client=client, email="adlkfashdkfl@fake.com", password="password")
        assert response.status_code == 200
        assert "Invalid credentials" in str(response.data)

    def test_logout(self, client):
        self.login(client=client, email="admin@admin.com", password="password")
        response = client.get(url_for("bp.logout"))
        assert response.status_code == 302

    def test_semester(self, client):
        for i in range(1, 9):
            response = client.get(url_for("bp.semester", sem=i))
            assert response.status_code == 200

        response = client.get(url_for("bp.semester", sem=9))
        assert response.status_code == 200

    def test_professor(self, client):
        prof = ProfessorsNames.query.first().name
        response = client.get(url_for("bp.professor", profid=quote(prof)))
        assert response.status_code == 200
        assert request.path != url_for("bp.home")

        prof = "Blah Blah"
        response = client.get(url_for("bp.professor", profid=quote(prof)))
        assert response.status_code == 302

    def test_subject(self, client):
        sub = SubjectsNames.query.first().name
        response = client.get(url_for("bp.subject", subid=quote(sub)))
        assert response.status_code == 200

        sub = "Somereallyrandomsubthatexistsonlyintests"
        response = client.get(url_for("bp.subject", subid=quote(sub)), follow_redirects=True)
        assert response.status_code == 200
        assert "Invalid subject" in str(response.data)

    def test_404(self, client):
        response = client.get('/asdfasdfasdflkjlkjlkjadsfasdf')
        assert response.status_code == 404
