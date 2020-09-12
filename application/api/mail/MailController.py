from flask import Blueprint, jsonify
from http import HTTPStatus
from application.extensions import mail
from flask_mail import Message
mail_api = Blueprint('mail_api', __name__, url_prefix='/api/mail')


@mail_api.route('/test', methods=["GET"])
def test():
    msg = Message(
        'Test mail',
        recipients=['thanhcongaone@gmail.com']
    )
    msg.body = 'Test body'
    mail.send(msg)
    return jsonify('ok'), HTTPStatus.OK
