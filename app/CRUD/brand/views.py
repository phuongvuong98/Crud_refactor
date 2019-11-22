from flask import Blueprint, render_template, request, make_response, jsonify, redirect
from app.CRUD.brand.forms import BrandForm
from app.CRUD.brand.models import BrandModel

brand_blueprint = Blueprint('brand', __name__, template_folder='templates')


@brand_blueprint.route('/api/list', methods=['GET'])
def list_brand_api():
    page = request.args.get('page', 1, type=int)
    brand = BrandModel()
    brands, total_pages = brand.query_paginate(page)
    arr_brand = []
    for brand in brands:
        tmp_brand = {
            'id': str(brand.id),
            'name': brand.name
        }
        arr_brand.append(tmp_brand)
    res = {
        "total_pages": total_pages,
        "data": arr_brand,
    }
    return make_response(jsonify(res), 200)


@brand_blueprint.route('/', methods=['GET'])
def list_brand(error=None):
    form = BrandForm()
    page = request.args.get('page', 1, type=int)
    brand = BrandModel()
    brands, total_pages = brand.query_paginate(page)
    return render_template('CRUD/brand/list.html', total_pages=total_pages, brand_active="active", form=form, error=error)


@brand_blueprint.route('/create', methods=['GET', 'POST'])
def create_brand(error=None):
    form = BrandForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            brand_name = request.form['brand_name']
            brand = BrandModel()
            brand_exist = brand.find(brand_name)
            if brand_exist is None or len(brand_exist) == 0:
                return BrandModel.create(brand_name) and redirect('/brand')
            else:
                error = "Your brand is error"
    return render_template('CRUD/brand/create.html', error=error, brand_active="active", form=form)


@brand_blueprint.route('/edit', methods=['POST'])
def edit_brand():
    form = BrandForm()
    brand = BrandModel()
    brands, total_pages = brand.query_paginate(1)
    if form.validate_on_submit():
        brand_id = request.form['brand_id']
        brand_name = request.form['brand_name']
        result, error = brand.edit(brand_id, brand_name)
        if error:
            return list_brand(error)
    return render_template('CRUD/brand/list.html', total_pages=total_pages, brand_active="active", form=form)
