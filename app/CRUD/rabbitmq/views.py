import json
from flask import Response
import pymongo
from flask import Blueprint, render_template, redirect, request, jsonify
from bson import ObjectId
from app.CRUD.address.models import AddressModel
from app.CRUD.brand.models import BrandModel
from app.CRUD.category.models import CategoryModel
from app.CRUD.city.models import CityModel
from app.CRUD.color.models import ColorModel
from app.CRUD.district.models import DistrictModel
from app.CRUD.product.models import ProductModel
from app.CRUD.store.models import StoreModel
from app.CRUD.product_variant.models import ProductVariantModel
import pika

rabbitmq_blueprint = Blueprint('rabbitmq', __name__, template_folder='templates')


@rabbitmq_blueprint.route('/create', methods=['GET'])
def create_queue():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='create')

    def async_mongodb(obj):
        from pymongo import MongoClient
        client = MongoClient()

        mongodb = client.crud_1

        item = obj["create_mongo"]
        try:
            if str(obj["table"]) == "district":
                city = mongodb.city.find_one({"mysql_id": str(obj["mysql_city_id"])})
                item = obj["create_mongo"]
                item["city_id"] = city["_id"]
                res = mongodb[str(obj["table"])].insert_one(item)
                return "Success"

            if str(obj["table"]) == "category":
                brand = mongodb.brand.find_one({"mysql_id": str(obj["mysql_brand_id"])})
                item = obj["create_mongo"]
                item["brand_id"] = brand["_id"]
                res = mongodb[str(obj["table"])].insert_one(item)
                return "Success"

            res = mongodb[str(obj["table"])].insert_one(item)
            return "Success"
        except pymongo.errors.DuplicateKeyError:
            return "Error"

    def on_request(ch, method, props, body):
        print("Handle create queue")
        dict_obj = json.loads(body)
        print("Receive body:", dict_obj)
        response = async_mongodb(dict_obj)
        print(" result after calculate: ", response)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='create', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


@rabbitmq_blueprint.route('/edit', methods=['GET'])
def edit_queue():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='edit')

    def async_mongodb(obj):
        from pymongo import MongoClient
        client = MongoClient()
        mongodb = client.crud_1

        new_data = obj["edit_mongo"]

        try:
            if str(obj["table"]) == "district":
                city = mongodb.city.find_one({"mysql_id": str(obj["mysql_city_id"])})
                new_data = obj["edit_mongo"]
                new_data["$set"]["city_id"] = city["_id"]
                res = mongodb[str(obj["table"])].update({"mysql_id": str(obj["mysql_id"])}, new_data)
                return "Success"

            if str(obj["table"]) == "category":
                brand = mongodb.brand.find_one({"mysql_id": str(obj["mysql_brand_id"])})
                new_data = obj["edit_mongo"]
                new_data["$set"]["brand_id"] = brand["_id"]
                res = mongodb[str(obj["table"])].update({"mysql_id": str(obj["mysql_id"])}, new_data)
                return "Success"

            res = mongodb[str(obj["table"])].update({"mysql_id": str(obj["mysql_id"])}, new_data)
            return "Success"
        except pymongo.errors.DuplicateKeyError:
            return "Error"

    def on_request(ch, method, props, body):
        print("Handle edit queue")
        dict_obj = json.loads(body)
        print(dict_obj)

        response = async_mongodb(dict_obj)
        print(" result after calculate edit : ", response)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='edit', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
