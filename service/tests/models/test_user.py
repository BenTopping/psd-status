from app.models.user import User

def test_new_user():
    user = User("testUsername", "testPassword")

    assert user.username == "testUsername"
    assert user.password == "testPassword"

def test_create_user(app):
    with app.app_context():
        User.create("testUsername", "testPassword")

        # Checks latest user created has same details as above
        db_user = User.query.order_by(User.id.desc()).first()
        assert db_user.username == "testUsername"
        assert db_user.password == "testPassword"

def test_user_as_dict():
    user = User("testUsername", "testPassword").as_dict()

    assert user["username"] == "testUsername"
    assert user["password"] == "testPassword"