from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from autoservisas import klases

class RegistracijosForma(FlaskForm):

    vardas = StringField('Vardas', [DataRequired()])
    pavarde = StringField('Pavarde', [DataRequired()])
    el_pastas = StringField('El.pastas', [DataRequired(), Email("Negerai ivestas E.Pasto adresas")])
    slaptazodis = PasswordField('Slaptazodis', [DataRequired()])
    patvirtinimas = PasswordField('Pakartokite slaptažodį', [EqualTo('slaptazodis', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(self, vardas):
        vartotojas = klases.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = klases.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')


class PrisijungimoForma(FlaskForm):
    prisijungimo_vardas = StringField('Prisijungimo vardas', [DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')


class ProfilioForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    pavarde = StringField('Pavarde', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email("Blokas El.pasto adresas")])
    tipas = StringField('Vartotojo tipas', [DataRequired()])
    is_admin = BooleanField('Administratorius')
    submit = SubmitField('Atnaujinti')

    def tikrinti_varda(self, vardas):
        vartotojas = klases.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = klases.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')


class NaujoIrasoForma(FlaskForm):
    make = StringField('Laisvas tekstas', [DataRequired()])
    details = StringField('Laisvas tekstas', [DataRequired()])
    total_amount = StringField('Total amount', [DataRequired()])
    submit = SubmitField('Sukurti Irasa')

class AtnaujintoIrasoForma(FlaskForm):

    repair_status = StringField('Remonto statusas', [DataRequired()])
    details = StringField('Laisvas tekstas', [DataRequired()])
    total_amount = StringField('Total amount', [DataRequired()])
    submit = SubmitField('Atnaujinti Irasa')


class NaujoAutomobilioForma(FlaskForm):

    make = StringField('Automobilio zenklas', [DataRequired()])
    model = StringField('Modelis', [DataRequired()])
    engine = StringField('Variklis', [DataRequired()])
    vin_number = StringField('Vin number', [DataRequired()])
    plate_number = StringField('Plate number', [DataRequired()])
    submit = SubmitField('Sukurti Irasa')