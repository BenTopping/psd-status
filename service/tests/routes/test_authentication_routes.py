from app.models.user import User


def test_post_login_endpoint_success(app, client):
    with app.app_context():
        User.create("username", "password")

        # When we have a valid username and password there should be a successful response with a token
        response = client.post(
            "/v1/login", json={"username": "username", "password": "password"}
        )
        assert response.status_code == 200
        assert response.json["token"] is not None


def test_post_login_endpoint_failure(app, client):
    with app.app_context():
        User.create("username", "password")

        # When we have a bad password there should be a unsuccessful response with an error
        response = client.post(
            "/v1/login", json={"username": "username", "password": "badpassword"}
        )
        assert response.status_code == 401
        assert response.json == {
            "authenticated": False,
            "message": "Invalid credentials",
        }
