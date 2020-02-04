from users.models import User
from tests.factories.bases import ResourceFactory
from factory.fuzzy import FuzzyText
from factory import Sequence, LazyAttribute
from werkzeug.security import generate_password_hash


class UserFactory(ResourceFactory):
    class Meta:
        model = User

    username = FuzzyText(length=20)
    email = Sequence(lambda n: f'user-{0}-{uuid_.uuid4().__str__()[0:10]}@gmail.com'.format(n))
    password_hash = LazyAttribute(lambda a: generate_password_hash('password'))
