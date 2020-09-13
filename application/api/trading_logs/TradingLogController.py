# from flask import abort
# from flask_restful import Resource, reqparse, marshal_with, fields
#
# from application.api import api, meta_fields
# from application.api.trading_logs.TradingLog import TradingLog
# from application.api.users.User import User
# from application.helpers import paginate
#
# trading_log_parser = reqparse.RequestParser()
# trading_log_parser.add_argument('user_id', type=str)
# trading_log_parser.add_argument('entry', type=float)
# # trading_log_parser.add_argument('stop_loss', type=float)
# # trading_log_parser.add_argument('take_profit', type=float)
# # trading_log_parser.add_argument('reason', type=str)
#
# # Marshaled field definitions for trading_log objects
# trading_log_fields = {
#     'id': fields.String,
#     'user_id': fields.String,
#     'entry': fields.Float,
#     # 'stop_loss': fields.Float,
#     # 'take_profit': fields.Float,
#     # 'reason': fields.String,
#     # 'closed_date': fields.DateTime,
#     # 'closed_price': fields.Float,
#     # 'real_pnl': fields.Float,
#     # 'real_pnl_percentage': fields.Float,
#     # 'closed_reason_type': fields.Integer,
#     # 'closed_reason': fields.String,
#     # 'chart_url_image': fields.String
# }
#
# # Marshaled field definitions for lists of trading_log objects
# trading_log_list_fields = {
#     'items': fields.List(fields.Nested(trading_log_fields)),
#     'meta': fields.Nested(meta_fields),
# }
#
#
# class TradingLogResource(Resource):
#     # decorators = [
#     #     self_only,
#     #     auth.login_required,
#     # ]
#
#     @marshal_with(trading_log_fields)
#     def get(self, trading_log_id=None, **kwargs):
#         trading_log = TradingLog.get_by_id(trading_log_id)
#
#         if not trading_log:
#             abort(404)
#
#         return trading_log
#
#     @marshal_with(trading_log_fields)
#     def put(self, trading_log_id=None, **kwargs):
#         trading_log = TradingLog.get_by_id(trading_log_id)
#
#         if not trading_log:
#             abort(404)
#
#         trading_log.update(**trading_log_parser.parse_args())
#         return trading_log
#
#     def delete(self, trading_log_id=0, **kwargs):
#         trading_log = TradingLog.get_by_id(trading_log_id)
#
#         if not trading_log:
#             abort(404)
#
#         trading_log.delete()
#         return 204
#
#
# class TradingLogListResource(Resource):
#     # decorators = [
#     #     self_only,
#     #     auth.login_required,
#     # ]
#
#     @marshal_with(trading_log_list_fields)
#     @paginate()
#     def get(self, user_id=None, username=None):
#         # Find user that trading_log goes with
#         user = None
#         if user_id:
#             user = User.get_by_id(user_id)
#         else:
#             user = User.get_by_username(username)
#
#         if not user:
#             abort(404)
#
#         # Get the user's trading_logs
#         trading_logs = TradingLog.query.filter_by(user_id=user.id)
#
#         return trading_logs
#
#     @marshal_with(trading_log_fields)
#     def post(self, user_id=None, username=None):
#         args = trading_log_parser.parse_args()
#         # user owns the trading_log
#         # args['user_id'] = g.user.id
#         trading_log = TradingLog.create(**args)
#         return trading_log, 201
#
#
# api.add_resource(TradingLogResource, '/users/<string:user_id>/trading_logs/<string:trading_log_id>',
#                  '/users/<username>/trading_logs/<string:trading_log_id>')
# api.add_resource(TradingLogListResource, '/users/<string:user_id>/trading_logs',
#                  '/users/<username>/trading_logs')
