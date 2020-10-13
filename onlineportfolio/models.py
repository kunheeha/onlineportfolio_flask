from onlineportfolio import db, login_manager
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cv_file = db.Column(db.String(20), nullable=True)
    statement = db.Column(db.String(240), nullable=True)

    def __repr__(self):
        return f"User('{self.name}')"
