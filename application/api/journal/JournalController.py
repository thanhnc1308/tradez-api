from flask import Blueprint
from flask_restful import Api
from application.api.journal.Journal import Journal
from application.api.journal.JournalSchema import journal_schema, journals_schema, journals_paging_schema
from application.api.base.BaseController import BaseController, BaseListController

journal_api = Blueprint("journal_api", __name__, url_prefix='/api/journals')
api = Api(journal_api)


class JournalController(BaseController):
    model = Journal
    schema = journal_schema


api.add_resource(JournalController, '/<string:id>', endpoint='journal')


class JournalListController(BaseListController):
    model = Journal()
    schema = journal_schema
    list_schema = journals_schema
    paging_schema = journals_paging_schema


api.add_resource(JournalListController, '', endpoint='journals')
