from rest_project import db


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(255))

    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    center = db.relationship('Center', backref=db.backref('animals', lazy=True))
    
    specie_id = db.Column(db.Integer, db.ForeignKey('specie.id'))

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            "age": self.age,
            "price": self.price,
            "center": self.center.login,
            "specie": self.specie.name
        }


class Specie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    animals = db.relationship('Animal', backref=db.backref('specie', lazy=True))

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
        }