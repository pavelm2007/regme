from random import seed

from django.conf import settings
from mongoengine import connect
import pytest


@pytest.fixture(scope='module')
def django_settings():
    settings.configure(
        USE_TZ=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'mongoengine.django.mongo_auth',
            'regme',
        ),
        AUTH_USER_MODEL=('mongo_auth.MongoUser'),
        AUTHENTICATION_BACKENDS=(
            'mongoengine.django.auth.MongoEngineBackend',),
        MONGOENGINE_USER_DOCUMENT='regme.documents.User',
    )


@pytest.fixture
def User(django_settings):
    from regme.documents import User
    return User


@pytest.yield_fixture
def db(User):
    connect(db='test_regme')
    User.drop_collection()
    yield


@pytest.fixture
def user_data():
    return {
        'username': 'username',
        'password': 'password',
        'email': 'email@example.com'}


def test_create_inactive_user(db, User, user_data):
    user = User.create_user(**user_data)
    assert isinstance(user, User)
    assert not user.is_active


def test_generate_activation_key(db, User, user_data):
    seed('')
    user = User.create_user(**user_data)
    key = user.get_activation_key()
    assert key == '516bb9061d58280acd0c3900e18feaf5166f02ff'