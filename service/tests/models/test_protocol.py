from app.models.protocol import Protocol
from app.models.monitor import Monitor

def test_new_protocol():
    protocol = Protocol("testProtocol")

    assert protocol.name == "testProtocol"

def test_create_protocol(app):
    with app.app_context():
        Protocol.create("testProtocol")

        # Checks latest protocol created has same details as above
        db_protocol = Protocol.query.order_by(Protocol.id.desc()).first()
        assert db_protocol.name == "testProtocol"

def test_protocol_as_dict():
    protocol = Protocol("testProtocol").as_dict()

    assert protocol["name"] == "testProtocol"

def test_protocol_monitors(app, faker):
    with app.app_context():
        protocol = Protocol.create("testProtocol")
        another_protocol = Protocol.create("anotherProtocol")

        expected_monitors = []
        for _ in range(5):
            expected_monitors.append(Monitor.create(protocol.id, 30, faker.name(), 'www.test.com', True))
        for _ in range(5):
            # Create unrelated monitors
            Monitor.create(another_protocol.id, 30, faker.name(), 'www.test.com', True)

        assert protocol.monitors == expected_monitors
