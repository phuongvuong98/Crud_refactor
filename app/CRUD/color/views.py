from flask import Blueprint, render_template, request, make_response, jsonify, redirect
from app.CRUD.color.forms import ColorForm
from app.CRUD.color.models import ColorModel

color_blueprint = Blueprint('color', __name__, template_folder='templates')


@color_blueprint.route('/api/list', methods=['GET'])
def list_color_api():
    page = request.args.get('page', 1, type=int)
    color = ColorModel()
    colors, total_pages = color.query_paginate(page)
    arr_color = []
    for color in colors:
        tmp_color = {
            'id': str(color.id),
            'name': color.value
        }
        arr_color.append(tmp_color)
    res = {
        "total_pages": total_pages,
        "data": arr_color,
    }
    return make_response(jsonify(res), 200)


@color_blueprint.route('/', methods=['GET'])
def list_color(error=None):
    form = ColorForm()
    page = request.args.get('page', 1, type=int)
    color = ColorModel()
    colors, total_pages = color.query_paginate(page)
    return render_template('CRUD/color/list.html', total_pages=total_pages, color_active="active", form=form, error=error)


@color_blueprint.route('/create', methods=['GET', 'POST'])
def create_color(error=None):
    form = ColorForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            color_value = request.form['color_name']
            color = ColorModel()
            color_exist = color.find(color_value)
            if color_exist is None or len(color_exist) == 0:
                return ColorModel.create(color_value) and redirect('/color')
            else:
                error = "Your color is error"
    return render_template('CRUD/color/create.html', error=error, color_active="active", form=form)


@color_blueprint.route('/edit', methods=['POST'])
def edit_color():
    form = ColorForm()
    color = ColorModel()
    colors, total_pages = color.query_paginate(1)
    if form.validate_on_submit():
        color_id = request.form['color_id']
        color_value = request.form['color_name']
        result, error = color.edit(color_id, color_value)
        if error:
            return list_color(error)
    return render_template('CRUD/color/list.html', total_pages=total_pages, color_active="active", form=form)
