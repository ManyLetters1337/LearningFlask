"""
Views for Product Class
"""
from flask import url_for, render_template, redirect, session, request, Blueprint
from database.service_registry import services
from flask_login import login_required
from form.forms import ProductForm, create_product_form
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from product.models import Product

product = Blueprint('product', __name__, template_folder='templates')


@product.route('/', methods=['GET'])
@login_required
def product_page(uuid):
    """
    Page for product
    :return: Page with product
    """

    return render_template("/product.html")


@product.route('/all', methods=['GET'])
@login_required
def products_page():
    """
    Page with all products
    @return:
    """
    products = services.products.get_product_for_user(session['user_id'])

    return render_template("/products.html", products=products)


@product.route('add_product', methods=['GET'])
@login_required
def add_product():
    """
    Add Product Get Method
    @return: page with add product form
    """
    form: ProductForm = create_product_form()

    return render_template('add_product.html', form=form)


@product.route('/add_product', methods=['POST'])
@login_required
def add_product_post():
    """
    Add Product Post Method
    @return: page with all products
    """
    form: ProductForm = create_product_form()

    product_: Product = services.products.add_product(session['user_id'], form.title.data, form.description.data)

    return redirect(url_for('product.products_page'))
