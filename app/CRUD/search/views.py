from flask import Blueprint, render_template, request, make_response, jsonify, redirect, url_for
from app.CRUD.search.forms import SearchForm

from app.CRUD.address.models import AddressModel
from app.CRUD.brand.models import BrandModel
from app.CRUD.category.models import CategoryModel
from app.CRUD.city.models import CityModel
from app.CRUD.color.models import ColorModel
from app.CRUD.district.models import DistrictModel
from app.CRUD.product.models import ProductModel
from app.CRUD.store.models import StoreModel
from app.CRUD.product_variant.models import ProductVariantModel

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/', methods=['GET'])
def home(error=None, form=None):
    form = SearchForm()
    if not form.validate():
        return redirect('/')
    page = request.args.get('page', 1, type=int)
    print("data:", form.q.data)
    cls_model = [AddressModel, BrandModel, CategoryModel, CityModel, ColorModel, DistrictModel, ProductModel, StoreModel]
    reindex_all = [model.reindex() for model in cls_model]
    search_model = [model.search(form.q.data, page, 10) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if total != 0:
            search_obj.extend(obj)
    print("results", search_obj)
    # next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
    #     if total > page * current_app.config['POSTS_PER_PAGE'] else None
    # prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
    #     if page > 1 else None
    return render_template('base.html')
