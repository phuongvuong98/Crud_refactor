from app import db
import json
import pika
import uuid
import threading
import requests
queue = {}

class AsyncRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call_create(self, obj):
        print("Call create:", obj)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        queue[self.corr_id] = None

        self.channel.basic_publish(
            exchange='',
            routing_key='create',
            properties = pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(obj, indent=4, sort_keys=True))

        while self.response is None:
            self.connection.process_data_events()
        queue[self.corr_id] = self.response
        print(self.response)
        return self.response

    def call_edit(self, obj):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        queue[self.corr_id] = None

        print("Call edit:", obj)

        self.channel.basic_publish(
            exchange='',
            routing_key='edit',
            properties = pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(obj, indent=4, sort_keys=True))

        while self.response is None:
            self.connection.process_data_events()
        queue[self.corr_id] = self.response
        print(self.response)
        return self.response


class RabbitMqMixin(object):


    @classmethod
    def before_commit(cls, session):
        print("before_commit")
        print(db.session.update)
        session._changes = {
            'add': list(session.new),
            'update': list(db.session.update),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        print("after_commit")
        print("session change: ", session._changes)


        for obj in session._changes['add']:
            if isinstance(obj, RabbitMqMixin):
                async_rpc = AsyncRpcClient()
                threading.Thread(target=async_rpc.call_create, args=(obj.convert_dict(),)).start()

        try:
            url = "http://0.0.0.0:5000/rabbitmq/create"
            response = requests.request("GET", url, timeout=2)
        except requests.exceptions.Timeout as e:
            print("Completed create")


        for obj in session._changes['update']:
            if isinstance(obj, RabbitMqMixin):
                async_rpc = AsyncRpcClient()
                threading.Thread(target=async_rpc.call_edit, args=(obj.convert_dict(),)).start()


        try:
            url = "http://0.0.0.0:5000/rabbitmq/edit"
            response = requests.request("GET", url, timeout=3)
        except requests.exceptions.Timeout as e:
            print("Completed edit")


db.event.listen(db.session, 'before_commit', RabbitMqMixin.before_commit)
db.event.listen(db.session, 'after_commit', RabbitMqMixin.after_commit)