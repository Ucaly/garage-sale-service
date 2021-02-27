import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

class SaleItem(db.Model):
    __tablename__ = 'saleitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.Integer, nullable=False, default=0)
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    users = db.relationship('User', secondary='waitinglist')

    status_dict = {
        0: 'Available',
        1: 'Pending',
        2: 'Sold'
    }

    def status_string(self):
        return self.status_dict[self.status]
    
    def __init__(self, name, price, image, description, status) -> None:
        self.name = name
        self.price = price
        self.image = image
        self.description = description
        self.status = status
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'description': self.description,
            'status': self.status_string(),
            'added_at': self.added_at
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    nickname = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    items = db.relationship('SaleItem', secondary='waitinglist')

    def __init__(self, name, nickname, email):
        self.name = name
        self.nickname = nickname
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'nickname': self.nickname,
            'email': self.email
        }

class WaitingList(db.Model):
    __tablename__ = 'waitinglist'
    item_id = db.Column(db.Integer, db.ForeignKey('saleitem.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    saleitem = db.relationship(SaleItem, backref=backref('items', cascade='all,delete-orphan'))
    user = db.relationship(User, backref=backref('users', cascade='all,delete-orphan'))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
