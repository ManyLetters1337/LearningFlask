"""
Product Class
"""
from database.core import db


class Product(db.Model):
    """
    Model of Product
    """
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(20), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def set_uuid(self, uuid_):
        """
        Set product uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_basket(self, id_):
        """
        Set basket for product
        :param id_:
        :return:
        """
        self.product_id.add(id_)

    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'user_id': self.user_id,
            'basket_id': self.basket_id,
            'title': self.title,
            'description': self.description
        }
