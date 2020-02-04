from factory import Factory
from database.core import db
import uuid


class ResourceFactory(Factory):
    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        instance = target_class(**kwargs)
        instance.uuid = uuid.uuid4().__str__()
        db.create_all()
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def _exclude_from_query(cls):
        return []

    @classmethod
    def _filter_query_keys(cls):
        return []
