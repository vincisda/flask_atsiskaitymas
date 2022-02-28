from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user
from autoservisas.__init__ import login_manager
from autoservisas.klases import Automobilis, Vartotojas, Irasas ,LimitedAdmin
from autoservisas import forms
from autoservisas.__init__ import app, db, admin


admin.add_view(LimitedAdmin(Vartotojas, db.session))
admin.add_view(LimitedAdmin(Irasas, db.session))
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))

@app.route('/')
def home():
    return render_template('base.html', current_user=current_user)

@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        flash('Atsijunkite, kad priregistruoti naują vartotoją.')
        return redirect(url_for('home'))
    form = forms.RegistracijosForma()
    
    

    if form.validate_on_submit():
        if len(Vartotojas.query.all()) > 0:
            admin = False
            is_employee = False
            user_type ="Pirkejas"
        else:
            admin = True
            is_employee = True
            user_type ="Administratorius"
        
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        naujas_vartotojas = Vartotojas(
            name = form.vardas.data,
            surname = form.pavarde.data,
            email = form.el_pastas.data,
            password = koduotas_slaptazodis,
            username = ((form.vardas.data[:3])+(form.pavarde.data[:3])).lower(),
            is_admin = admin,
            user_type = user_type,
            is_employee = is_employee
        )
        db.session.add(naujas_vartotojas)
        db.session.commit()
    
        flash(f'Sėkmingai prisiregistravote! Galite prisijungti su prisijungimo vardu: {naujas_vartotojas.username}. \n Prisijungimo informacija buvo issiusta i jusu el.pasta: {naujas_vartotojas.email}', 'success')
        return redirect(url_for('home'))
    return render_template('registracija.html', form=form, current_user=current_user)



@app.route('/prisijungimas', methods=['GET', 'POST'])
def prisijungimas():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        flash('Vartotojas jau prisijungęs. Atsijunkite ir bandykite iš naujo.')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(username=form.prisijungimo_vardas.data).first()
        if user and bcrypt.check_password_hash(user.password, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko, neteisingas prisijungimo vardas arba slaptažodis.', 'danger')
    return render_template('prisijungimas.html', form=form, current_user=current_user)


@app.route("/records")
@login_required
def records():
   
    pirmas_automobilis = Automobilis.query.filter_by(vartotojas_id=current_user.id).first()
    visi_irasai = Irasas.query.filter_by(automobilis_id=pirmas_automobilis.id)
    return render_template("irasai.html", visi_irasai=visi_irasai, datetime=datetime, pirmas_automobilis=pirmas_automobilis)

@app.route('/profilis', methods=['GET', 'POST'])
@login_required
def profilis():
    form = forms.ProfilioForma()
    if form.validate_on_submit():
        current_user.name = form.vardas.data
        current_user.surname = form.pavarde.data
        current_user.email = form.el_pastas.data
        current_user.user_type = form.tipas.data
        current_user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Profilis atnaujintas!', 'success')
        return redirect(url_for('profilis'))
    elif request.method == "GET":
        form.vardas.data = current_user.name
        form.el_pastas.data = current_user.email
       
    return render_template('profilis.html', current_user=current_user, form=form)

@app.route('/iraso_koregavimas', methods=['GET', 'POST'])
@login_required

def iraso_koregavimas():
    if current_user.is_employee:
        page = request.args.get('page', 1, type=int)
        visi_irasai = Irasas.query.all()
        form = forms.AtnaujintoIrasoForma()
        if form.validate_on_submit():
            visi_irasai.total_amount = form.total_amount.data
            visi_irasai.details = form.details.data
            visi_irasai.repair_status = form.repair_status.data
            db.session.commit()
            flash('Irasas atnaujintas!', 'success')
            return redirect(url_for('iraso_koregavimas'))
        elif request.method == "GET":
            form.total_amount.data = visi_irasai.total_amount
            form.details.data = visi_irasai.details
            form.repair_status.data = visi_irasai.repair_status
    else:
        return redirect(url_for('home'))
    
    return render_template('koregavimas.html', current_user=current_user, form=form, visi_irasai=visi_irasai)

@app.route("/atsijungimas")
def atsijungimas():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))

@app.route("/admin")
def admin():
    pass




@app.route('/naujas_irasas', methods=['GET', 'POST'])
@login_required
def new_post():
    visi_automobiliai = Automobilis.query.filter_by(vartotojas_id=current_user.id)
    form = forms.NaujoIrasoForma()
    if form.validate_on_submit():
        automobilis = Automobilis.query.filter_by(make=form.make.data).first()
        naujas_irasas = Irasas(
            
            model = automobilis.model,
            engine = automobilis.engine,
            total_amount= form.total_amount.data,
            details = form.details.data
            
        )
        db.session.add(naujas_irasas)
        db.session.commit()
        flash('Sėkmingai pridetas naujas irasas.', 'success')
        return redirect(url_for('home'))
    return render_template('naujas_irasas.html', form=form, current_user=current_user, visi_automobiliai=visi_automobiliai)



@app.route("/mano_automobilis")
@login_required
def cars():
    visi_automobiliai = Automobilis.query.filter_by(vartotojas_id=current_user.id)
    return render_template("mano_automobilis.html", visi_automobiliai=visi_automobiliai)


@app.route('/naujas_automobilis', methods=['GET', 'POST'])
@login_required
def new_car():
    form = forms.NaujoAutomobilioForma()
    if form.validate_on_submit():
        naujas_automobilis = Automobilis(
            make = form.make.data,
            model = form.model.data,
            engine = form.engine.data,
            vin_number= form.vin_number.data,
            plate_number = form.plate_number.data,
            vartotojas_id = current_user.id
        )
        db.session.add(naujas_automobilis)
        db.session.commit()
        flash('Sėkmingai pridetas naujas automobilis.', 'success')
        return redirect(url_for('home'))
    return render_template('naujas_automobilis.html', form=form, current_user=current_user)