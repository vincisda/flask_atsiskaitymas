from datetime import datetime
from email.policy import default
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from sqlalchemy import DateTime
from autoservisas.__init__ import db




class Vartotojas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Vardas', db.String(200), nullable=False)
    surname = db.Column('Pavarde', db.String(200), nullable=False)
    email = db.Column('El.pastas', db.String(200), unique=True, nullable=False)
    password = db.Column('Slaptazodis', db.String(200), nullable=False)
    is_admin = db.Column('Administratorius', db.Boolean())
    username = db.Column('Prisijungimo_vardas', db.String(20),unique=True, nullable=False)
    user_type = db.Column('Vartotojo_tipas', db.String(20), nullable=False)
    is_employee = db.Column('Yra_darbuotojas', db.Boolean())

    def __repr__(self) -> str:
        return self.vardas


class Irasas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('Sukurta', DateTime, default=datetime.utcnow())
    total_amount = db.Column('Suma', db.Numeric(16,2), default=0)
    details = db.Column("Tekstas", db.String(200), default="Privalomi remonto darbai")
    automobilis_id = db.Column(db.Integer, db.ForeignKey('automobilis.id'))
    automobilis = db.relationship("Automobilis", lazy=True)
    repair_status = db.Column("Remonto_Statusas", db.String(20), default="Naujas")

    def __repr__(self) -> str:
        return f'{self.suma}: {self.created} @ {self.vartotojas}'


class Automobilis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column("Marke", db.String(200))
    model = db.Column("Modelis", db.String(200))
    engine = db.Column("Variklis", db.String(200))
    vin_number = db.Column("Vin numeris", db.String(200))
    plate_number = db.Column("Valstybinis numeris", db.String(200))
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)

class LimitedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin