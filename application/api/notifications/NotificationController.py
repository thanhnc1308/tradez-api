from flask import Blueprint
from flask_restful import Api
from application.api.notifications.Notification import Notification
from application.api.notifications.NotificationSchema import notification_schema, notifications_schema, notifications_paging_schema
from application.api.base.BaseController import BaseController, BaseListController

notification_api = Blueprint("notification_api", __name__, url_prefix='/api/notifications')
api = Api(notification_api)


class NotificationController(BaseController):
    model = Notification
    schema = notification_schema


api.add_resource(NotificationController, '/<string:id>', endpoint='notification')


class NotificationListController(BaseListController):
    model = Notification
    schema = notification_schema
    list_schema = notifications_schema
    paging_schema = notifications_paging_schema


api.add_resource(NotificationListController, '', endpoint='notifications')
