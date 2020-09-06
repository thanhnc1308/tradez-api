class User(db.Model):
    """
    User.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    passwd_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def passwd(self):
        raise AttributeError('passwd is not a readable attribute.')

    @passwd.setter
    def passwd(self, passwd):
        self.passwd_hash = bcrypt.generate_passwd_hash(passwd)

    def verify_passwd(self, passwd):
        return bcrypt.check_password_hash(self.passwd_hash, passwd)