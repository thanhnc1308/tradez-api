def get(self, user_id=None):
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        return marshal(user, user_fields)
    else:
        args = request.args.to_dict()
        limit = args.get('limit', 0)
        offset = args.get('offset', 0)

        args.pop('limit', None)
        args.pop('offset', None)

        user = User.query.filter_by(**args).order_by(User.id)
        if limit:
            user = user.limit(limit)

        if offset:
            user = user.offset(offset)

        user = user.all()

        return marshal({
            'count': len(user),
            'users': [marshal(u, user_fields) for u in user]
        }, user_list_fields)
