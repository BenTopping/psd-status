from app.models.protocol import Protocol


def test_get_login_endpoint_success(app, client):
    with app.app_context():
        expected_protocols = []
        for i in range(5):
            expected_protocols.append(Protocol.create(f"Name-{1}"))

        # Returns a list of all protocols
        response = client.get("/v1/protocols")
        assert response.status_code == 200
        assert response.json == list(
            map(lambda protocol: protocol.as_dict(), expected_protocols)
        )
