from app.models.monitor import Monitor
from app.models.protocol import Protocol
from unittest.mock import patch


def test_get_monitors_endpoint_success(app, client):
    with app.app_context():
        expected_monitors = []
        protocol = Protocol.create("http")
        for i in range(5):
            expected_monitors.append(
                Monitor.create(
                    protocol.id, 30, f"Monitor{i}", f"www.monitor-{i}.com", True
                )
            )

        # Returns a list of all monitors
        response = client.get("/v1/monitors")
        assert response.status_code == 200
        assert response.json == list(
            map(lambda monitor: monitor.as_dict(), expected_monitors)
        )


def test_get_monitors_endpoint_with_ids_success(app, client):
    with app.app_context():
        expected_monitors = []
        protocol = Protocol.create("http")
        for i in range(5):
            expected_monitors.append(
                Monitor.create(
                    protocol.id, 30, f"Monitor{i}", f"www.monitor-{i}.com", True
                )
            )

        # Returns a list of all monitors
        id = expected_monitors[0].id
        response = client.get(f"/v1/monitors?ids={id}")
        assert response.status_code == 200
        assert response.json == [expected_monitors[0].as_dict()]


def test_get_monitors_endpoint_with_ids_failure(app, client):
    with app.app_context():
        response = client.get("/v1/monitors?ids=invalidId")
        assert response.status_code == 400
        assert response.json == {"message": "Unable to find monitor with id invalidId"}


def test_get_monitors_endpoint_with_active_success(app, client):
    with app.app_context():
        expected_monitors = []
        protocol = Protocol.create("http")
        for i in range(5):
            expected_monitors.append(
                Monitor.create(
                    protocol.id, 30, f"Monitor{i}", f"www.monitor-{i}.com", True
                )
            )
            # Create active false records
            Monitor.create(
                protocol.id, 30, f"Monitor-1-{i}", f"www.monitor-1-{i}.com", False
            )

        # Returns a list of all monitors
        response = client.get("/v1/monitors?active=true")
        assert response.status_code == 200
        assert response.json == list(
            map(lambda monitor: monitor.as_dict(), expected_monitors)
        )


def test_get_monitors_endpoint_with_active_failure(app, client):
    with app.app_context():
        protocol = Protocol.create("http")
        expected_monitor = Monitor.create(
            protocol.id, 30, "Monitor", "www.monitor.com", False
        )

        # Returns a list of all monitors
        id = expected_monitor.id
        response = client.get(f"/v1/monitors?ids={id}&active=true")
        assert response.status_code == 400
        assert response.json == {
            "message": f"Unable to find monitor with id {id} and active state: True"
        }


def test_update_monitor_endpoint_success(app, client, active_jwt):
    with app.app_context():
        # We need to mock this method because it handles the scheduled jobs
        with patch(
            "app.routes.common.monitors.handle_http_job", return_value=""
        ) as mock_handle_http_job:
            # Setup existing data
            protocol = Protocol.create("http")
            monitor = Monitor.create(
                protocol.id, 30, "Monitor", "www.monitor.com", True
            )

            # Post a monitor with valid changes
            response = client.post(
                "/v1/monitor",
                json={
                    "id": str(monitor.id),
                    "protocol_id": str(monitor.protocol_id),
                    # Empty name causes failure
                    "name": "New name",
                    "target": monitor.target,
                    "delay": "30",
                    "active": True,
                },
                headers={"Authorization": f"Bearer {active_jwt}"},
            )
            mock_handle_http_job.assert_called_once_with(monitor)
            assert response.status_code == 200
            # Check some of the returned details to check they are accurate
            # TODO We should be checking the full object here
            assert response.json["id"] == str(monitor.id)
            assert response.json["name"] == "New name"


def test_update_monitor_endpoint_unauthenticated(app, client):
    with app.app_context():
        # Setup existing data
        protocol = Protocol.create("http")
        monitor = Monitor.create(protocol.id, 30, "Monitor", "www.monitor.com", True)

        # Post a monitor with valid changes
        response = client.post(
            "/v1/monitor",
            json={
                "id": str(monitor.id),
                "protocol_id": str(monitor.protocol_id),
                # Empty name causes failure
                "name": "New name",
                "target": monitor.target,
                "delay": "30",
                "active": True,
            },
            # Invalid / Unauthenticated jwt
            headers={"Authorization": "Bearer invalid JWT"},
        )
        assert response.status_code == 401
        assert response.json == {
            "authenticated": False,
            "message": "Invalid token. Authentication required",
        }


def test_update_monitor_endpoint_failure(app, client, active_jwt):
    with app.app_context():
        # Setup existing data
        protocol = Protocol.create("http")
        monitor = Monitor.create(protocol.id, 30, "Monitor", "www.monitor.com", True)

        # Post a monitor with invalid changes
        response = client.post(
            "/v1/monitor",
            json={
                "id": str(monitor.id),
                "protocol_id": str(monitor.protocol_id),
                # Empty name causes failure
                "name": None,
                "target": monitor.target,
                "delay": "30",
                "active": True,
            },
            headers={"Authorization": f"Bearer {active_jwt}"},
        )
        assert response.status_code == 400
        assert response.json == {"message": "Invalid data"}


def test_create_monitor_endpoint_success(app, client, active_jwt):
    with app.app_context():
        # We need to mock this method because it handles the scheduled jobs
        with patch(
            "app.routes.common.monitors.handle_http_job", return_value=""
        ) as mock_handle_http_job:
            # Setup existing data
            protocol = Protocol.create("http")

            # Post a monitor with valid changes
            response = client.post(
                "/v1/monitor",
                json={
                    "protocol_id": str(protocol.id),
                    "name": "New monitor",
                    "target": "www.newTarget.com",
                    "delay": "30",
                    "active": True,
                },
                headers={"Authorization": f"Bearer {active_jwt}"},
            )
            mock_handle_http_job.assert_called_once()
            assert response.status_code == 200
            # Check some of the returned details to check they are accurate
            # TODO We should be checking the full object here
            assert response.json["id"] is not None
            assert response.json["name"] == "New monitor"


def test_create_monitor_endpoint_failure(app, client, active_jwt):
    with app.app_context():
        # Setup existing data
        protocol = Protocol.create("http")
        Monitor.create(protocol.id, 30, "New monitor", "www.monitor.com", True)

        # Post a monitor with valid changes
        response = client.post(
            "/v1/monitor",
            json={
                "protocol_id": str(protocol.id),
                # A monitor already exists with this name so causes a failure
                "name": "New monitor",
                "target": "www.newTarget.com",
                "delay": "30",
                "active": True,
            },
            headers={"Authorization": f"Bearer {active_jwt}"},
        )
        assert response.status_code == 400
        assert response.json == {"message": "Invalid data"}
