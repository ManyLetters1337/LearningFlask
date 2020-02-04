"""
Database interaction methods for a Product class
"""
from database.core import db
from database.base_services import BaseDBService
from .models import Product
from flask import session
import uuid
import mysql.connector

class ProductDBService(BaseDBService):
    model = Product

    def connect_to_db(self):
        """
        Connect to database
        @return:
        """
        mydb = mysql.connector.connect(
            host="localhost",
            user="manyletters",
            passwd="12345678*Aa",
            database="base"
        )

        return mydb

    def change_database(self, mydb, query: str, args):
        """
        Change database
        @param mydb:
        @param query:
        @param args:
        @return:
        """
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(query, args)
        mydb.commit()

    def get_from_database(self, mydb, query: str, args):
        """
        Get Data from Database
        @param mydb:
        @param query:
        @param args:
        @return:
        """
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(query, args)
        myresult = mycursor.fetchall()

        return myresult

    def get_product_for_user(self, _id: int) -> Product:
        """
        Get product for current user
        :param _id:
        :return  Product for user
        """
        query = "SELECT title, description FROM product"

        db = self.connect_to_db()
        args = _id
        products = self.get_from_database(db, query, args)

        return products

    def add_product(self, _id: int, title: str, description: str):
        """
        Add Product
        @param _id:
        @param title:
        @param description:
        @return:
        """
        query = "INSERT INTO product (uuid, user_id, title, description) VALUES (%s, %s, %s, %s)"
        args = (uuid.uuid4().__str__(), _id, title, description)
        db = self.connect_to_db()
        product = self.change_database(db, query, args)

        return product
