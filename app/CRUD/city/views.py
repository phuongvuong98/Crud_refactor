from flask import Blueprint, render_template, request, make_response, jsonify, redirect
from app.CRUD.city.forms import CityForm
from app.CRUD.city.models import CityModel

city_blueprint = Blueprint('city', __name__, template_folder='templates')


@city_blueprint.route('/api/list', methods=['GET'])
def list_city_api():
    page = request.args.get('page', 1, type=int)
    city = CityModel()
    cities, total_pages = city.query_paginate(page)
    arr_city = []
    for city in cities:
        tmp_city = {
            'id': str(city.id),
            'name': city.name
        }
        arr_city.append(tmp_city)
    res = {
        "total_pages": total_pages,
        "data": arr_city,
    }
    return make_response(jsonify(res), 200)


@city_blueprint.route('/', methods=['GET'])
def list_city(error=None):
    form = CityForm()
    page = request.args.get('page', 1, type=int)
    city = CityModel()
    cities, total_pages = city.query_paginate(page)
    return render_template('CRUD/city/list.html', total_pages=total_pages, city_active="active", form=form, error=error)


@city_blueprint.route('/create', methods=['GET', 'POST'])
def create_city(error=None):
    form = CityForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            city_name = request.form['city_name']
            city = CityModel()
            city_exist = city.find(city_name)
            if city_exist is None or len(city_exist) == 0:
                return CityModel.create(city_name) and redirect('/city')
            else:
                error = "Your city is error"
    return render_template('CRUD/city/create.html', error=error, city_active="active", form=form)


@city_blueprint.route('/edit', methods=['POST'])
def edit_city():
    form = CityForm()
    city = CityModel()
    cities, total_pages = city.query_paginate(1)
    if form.validate_on_submit():
        city_id = request.form['city_id']
        city_name = request.form['city_name']
        result, error = city.edit(city_id, city_name)
        if error:
            return list_city(error)
    return render_template('CRUD/city/list.html', total_pages=total_pages, city_active="active", form=form)
