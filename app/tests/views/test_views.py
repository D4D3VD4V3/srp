from flask import url_for, request
from app.models import Login


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

    def test_login(self, client):
        response = client.get(url_for("bp.login"))
        assert response.status_code == 200
        response = self.login(client=client, email="admin@admin.com", password="password")
        assert response.status_code == 200
        # assert "successfully" in str(response.data)
        response = self.login(client=client, email="adlkfashdkfl@fake.com", password="password")
        assert response.status_code == 200
        assert "Invalid credentials" in str(response.data)

    def test_logout(self, client):
        response = client.get(url_for("bp.logout"))
        assert response.status_code == 302

    def test_semester(self, client):
        for i in range(1, 9):
            response = client.get(url_for("bp.semester", sem=i))
            assert response.status_code == 200

        response = client.get(url_for("bp.semester", sem=9))
        assert response.status_code == 200

    def test_404(self, client):
        response = client.get('/asdfasdfasdflkjlkjlkjadsfasdf')
        assert response.status_code == 404
