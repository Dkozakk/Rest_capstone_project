from datetime import datetime

from sqlalchemy.orm import backref
from rest_project import db


class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    jwt_accesses = db.relationship('JWTAccess', backref=db.backref('center', lazy=True))
    def serialize(self):
        return {
            "login": self.login,
            "password": self.password,
            "address": self.address
        }
    
    def get_animals_names(self):
        return [f"{animal.name} - {animal.specie.name}" for animal in self.animals]

class JWTAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
