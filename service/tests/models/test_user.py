from app.models.user import User
from werkzeug.security import check_password_hash


def test_new_user():
    user = User("testUsername", "testPassword")

    assert user.username == "testUsername"
    assert check_password_hash(user.password, "testPassword") is True


def test_create_user(app):
    with app.app_context():
        User.create("testUsername", "testPassword")

        # Checks latest user created has same details as above
        db_user = User.query.order_by(User.id.desc()).first()
        assert db_user.username == "testUsername"
        assert check_password_hash(db_user.password, "testPassword") is True


def test_user_as_dict():
    user = User("testUsername", "testPassword").as_dict()

    assert user["username"] == "testUsername"
