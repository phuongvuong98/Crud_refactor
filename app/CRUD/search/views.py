from flask import Blueprint, render_template, redirect, request, jsonify

from app.CRUD.search.forms import SearchForm
from app.CRUD.address.models import AddressModel
from app.CRUD.brand.models import BrandModel
from app.CRUD.category.models import CategoryModel
from app.CRUD.city.models import CityModel
from app.CRUD.color.models import ColorModel
from app.CRUD.district.models import DistrictModel
from app.CRUD.product.models import ProductModel
from app.CRUD.search.models import FullTextSearch, FuzzySearch, SuggestionSearch
from app.CRUD.store.models import StoreModel
from app.CRUD.product_variant.models import ProductVariantModel

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/full-text', methods=['GET'])
def full_text():
    form = SearchForm()
    if not form.validate() or not form.q.data:
        return redirect('/city')
    cls_model = [AddressModel, BrandModel, CategoryModel, CityModel, ColorModel, DistrictModel, ProductModel,
                 StoreModel, ProductVariantModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = FullTextSearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)
    return render_template('CRUD/search/list.html', search_obj=search_obj, form=form)


@search_blueprint.route('/fuzzy', methods=['GET'])
def fuzzy():
    form = SearchForm()
    if not form.validate() or not form.q.data:
        return redirect('/city')
    cls_model = [AddressModel, BrandModel, CategoryModel, CityModel, ColorModel, DistrictModel, ProductModel,
                 StoreModel, ProductVariantModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = FuzzySearch()
    search_model = [model.search(form.q.data, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)

    return render_template('CRUD/search/fuzzy.html', search_obj=search_obj, form=form)


@search_blueprint.route('/suggestion', methods=['POST'])
def suggestion():
    search_term = request.data.decode("utf-8").split("=")[1]
    cls_model = [AddressModel, BrandModel, CategoryModel, CityModel, ColorModel, DistrictModel, ProductModel,
                 StoreModel, ProductVariantModel]
    # reindex_all = [model.reindex() for model in cls_model]
    kind_search = SuggestionSearch()
    search_model = [model.search(search_term, 1, 10, kind_search) for model in cls_model]
    search_obj = []
    for obj, total in search_model:
        if not isinstance(total, int):
            search_obj.extend(total)

    return jsonify({"data": search_obj})
