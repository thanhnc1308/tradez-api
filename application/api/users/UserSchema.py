from marshmallow import Schema, fields, post_load, validates, ValidationError


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    facebook = fields.Str()
    telegram = fields.Str()
    # emails = fields.Nested(ContactEmailSchema, many=True, required=True)
    created_at = fields.DateTime(dump_only=True)
    update_at = fields.DateTime(dump_only=True)
    # uri = fields.Method("get_item_uri")
    #
    # def get_item_uri(self, obj):
    #     return '/api/contacts/{obj.username}/'.format(
    #         obj=obj,
    #     )

    # @validates('username')
    # def validate_username(self, username, **kwargs):
    #     if bool(Contact.query.filter_by(username=username).first()):
    #         raise ValidationError(
    #             '"{username}" username already exists, '
    #             'please use a different username.'.format(username=username)
    #         )
    #
    # @validates('emails')
    # def validate_emails(self, emails):
    #     exists_in_contact_emails = []
    #     for d in emails:
    #         email = d.get('email')
    #         if bool(ContactEmail.query.filter_by(email=email).first()):
    #             exists_in_contact_emails.append(email)
    #
    #     if exists_in_contact_emails:
    #         raise ValidationError(
    #             '"{emails}" emails already exists, '
    #             'please try different emails.'.format(
    #                 emails=", ".join(exists_in_contact_emails)
    #             )
    #         )
    #
    # @post_load
    # def create_contact(self, data):
    #     email_list = data.pop('emails', list())
    #     contact = Contact(**data)
    #     contact_emails = [ContactEmail(email=d.get('email')) for d in email_list]
    #     contact.emails.extend(contact_emails)
    #     db.session.add(contact)
    #     db.session.add_all(contact_emails)
    #     db.session.commit()
    #     self.instance = contact
    #
    # def update_contact(self, contact, data):
    #     contact.username = data.get('username', contact.username)
    #     contact.first_name = data.get('first_name', contact.first_name)
    #     contact.last_name = data.get('last_name', contact.last_name)
    #     emails = data.get('emails')
    #     if emails:
    #         ContactEmail.query.filter_by(contact_id=contact.id).delete()
    #         db.session.commit()
    #         new_contact_emails = [ContactEmail(email=d.get('email')) for d in emails]
    #         contact.emails.extend(new_contact_emails)
    #         db.session.add_all(new_contact_emails)
    #     db.session.commit()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
