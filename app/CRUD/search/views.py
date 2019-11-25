from flask import Blueprint, render_template, request, make_response, jsonify, redirect


search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/', methods=['GET'])
def home(error=None, form=None):
    return render_template('base.html')