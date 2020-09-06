from marshmallow import Schema, fields, post_load, validates, ValidationError
from application.api.stock.Stock import Stock


class StockSchema(Schema):
    id = fields.String(dump_only=True)
    index = fields.String(required=True)

    @validates('index')
    def validate_index(self, index, **kwargs):
        if bool(Stock.query.filter_by(index=index).first()):
            raise ValidationError(
                '"{index}" index already exists, '
                'please use a different index.'.format(index=index)
            )

    @post_load
    def create_contact(self, data):
        print('posted data', data)
        stock = Stock(**data)
        Stock.session.add(stock)
        Stock.session.commit()
        self.instance = stock

    def update_contact(self, stock, data):
        stock.update(**data)
        # contact.username = data.get('username', contact.username)
        # contact.first_name = data.get('first_name', contact.first_name)
        # contact.last_name = data.get('last_name', contact.last_name)
        # emails = data.get('emails')
        # if emails:
        #     ContactEmail.query.filter_by(contact_id=contact.id).delete()
        #     db.session.commit()
        #     new_contact_emails = [ContactEmail(email=d.get('email')) for d in emails]
        #     contact.emails.extend(new_contact_emails)
        #     db.session.add_all(new_contact_emails)
        # db.session.commit()


stock_schema = StockSchema()
stock_list_schema = StockSchema(many=True)
