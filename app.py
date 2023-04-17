# coding: UTF-8
"""
Script: sae23/app
Création: maurelji, le 13/05/2022
"""

# Imports
from flask import Flask, render_template, request, flash, redirect, url_for, session
import util
from flask_wtf.csrf import CSRFProtect

# Initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = '2033090bb1a123046aef055a852e254ca3f056f0a4454af930cffc019b601465'
app.config['DATABASE'] = 'bdd/bdd_v2.sqlite'
app.teardown_appcontext(util.close_db)
csrf = CSRFProtect(app)


# Routes
@app.route("/")
def home():
    return render_template("vacataires.html", vacataires=util.get_all_vacataires())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if util.check_login(login, password):
        flash("Connexion réussie", "success")
        session['login'] = login
        return redirect(url_for('home'))
    flash("Identifiants invalides", "error")
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'login' in session:
        session.pop('login')
        flash('Déconnexion réussie', 'success')
    return redirect(url_for('login'))


@app.route('/add/vacataires', methods=['GET', 'POST'])
def add_vacataire():
    if request.method == 'GET':
        return render_template('add_vacataire.html')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    tel = request.form.get('tel')
    statut = request.form.get('statut')
    employeur = request.form.get('employeur')
    login = request.form.get('login')
    recrutable = request.form.get('recrutable')
    password = util.password_hash('vacataire')
    if login:
        compte = {'login': login, 'password': password, 'role': 'vacataire'}
        util.add_compte(compte)

    vacataire = {'nom': nom, 'prenom': prenom, 'email': email, 'tel': tel, 'statut': statut,
                 'employeur': employeur, 'login': login, 'recrutable': 1 if recrutable else 0}

    util.add_vacataire(vacataire)
    return redirect(url_for('home'))


@app.route('/del/vacataires/<id_vacataire>', methods=['GET', 'POST'])
def delete_vacataire(id_vacataire):
    data = util.get_vacataire(id_vacataire)
    if request.method == 'GET':
        return render_template('del_vacataire.html', data=data)
    else:
        if request.form.get('compte'):
            util.delete_compte(data['login'])
        util.delete_vacataire(id_vacataire)
        return redirect(url_for('home'))


@app.route('/edit/vacataires/<id_vacataire>')
def edit_vacataire(id_vacataire):
    vacataire = util.get_vacataire(id_vacataire)
    if vacataire is None:
        flash("Utilisateur Introuvable", "error")
        return redirect(url_for('liste_vacataires'))
    return render_template('edit_vacataire.html', data=vacataire)


@app.route('/update/vacataires/<id_vacataire>', methods=['POST'])
def update_vacataire(id_vacataire):
    vacataire = {'id_vacataire': id_vacataire, 'nom': request.form.get('nom'), 'prenom': request.form.get('prenom'),
                 'email': request.form.get('email'), 'tel': request.form.get('tel'),
                 'statut': request.form.get('statut'), 'employeur': request.form.get('employeur'),
                 'recrutable': 1 if request.form.get('recrutable') else 0}
    util.update_vacataire(vacataire)
    return redirect(url_for('liste_vacataires'))


@app.route('/add/enseignants', methods=['GET', 'POST'])
def add_enseignant():
    if request.method == 'GET':
        return render_template('add_enseignant.html')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    tel = request.form.get('tel')
    login = request.form.get('login')
    password = util.password_hash('enseignant')
    if login:
        compte = {'login': login, 'password': password, 'role': 'enseignant'}
        util.add_compte(compte)

    enseignant = {'nom': nom, 'prenom': prenom, 'email': email, 'tel': tel, 'login': login}

    util.add_enseignant(enseignant)

    return redirect(url_for('liste_enseignants'))


@app.route('/del/enseignants/<id_enseignant>', methods=['GET', 'POST'])
def delete_enseignant(id_enseignant):
    data = util.get_enseignant(id_enseignant)
    if request.method == 'GET':
        return render_template('del_enseignant.html', data=data)
    else:
        if request.form.get('compte'):
            util.delete_compte(data['login'])
        util.delete_enseignant(id_enseignant)
        return redirect(url_for('liste_enseignants'))


@app.route('/edit/enseignants/<id_enseignant>')
def edit_enseignant(id_enseignant):
    enseignant = util.get_enseignant(id_enseignant)
    if enseignant is None:
        flash("Utilisateur Introuvable", "error")
        return redirect(url_for('liste_enseignants'))
    return render_template('edit_enseignant.html', data=enseignant)


@app.route('/update/enseignants/<id_enseignant>', methods=['POST'])
def update_enseignant(id_enseignant):
    enseignant = {'id_enseignant': id_enseignant, 'nom': request.form.get('nom'), 'prenom': request.form.get('prenom'),
                  'email': request.form.get('email'), 'tel': request.form.get('tel')}
    util.update_enseignant(enseignant)
    return redirect(url_for('liste_enseignants'))


@app.route('/add/contrats', methods=['GET', 'POST'])
def add_contrat():
    if request.method == 'GET':
        vacataires = util.get_vacataire_sans_contrats()
        enseignants = util.get_enseignant_sans_contrats()
        return render_template('add_contrat.html', vacataires=vacataires, enseignants=enseignants)
    date_deb = request.form.get('date_deb')
    date_fin = request.form.get('date_fin')
    id_vacataire = request.form.get('id_vacataire')
    id_referent = request.form.get('id_referent')
    contrat = {'date_deb': date_deb, 'date_fin': date_fin, 'id_vacataire': id_vacataire, 'id_referent': id_referent}
    util.add_contrat(contrat)
    return redirect(url_for('liste_contrats'))


@app.route('/del/contrats/<id_contrat>', methods=['GET', 'POST'])
def delete_contrat(id_contrat):
    util.delete_contrat(id_contrat)
    return redirect(url_for('liste_contrats'))


@app.route('/add/interventions', methods=['GET', 'POST'])
def add_intervention():
    if request.method == 'GET':
        contrats = util.get_all_contrats()
        modules=util.get_all_modules()
        return render_template('add_intervention.html', contrats=contrats, modules=modules)
    id_contrat = request.form.get('id_contrat')
    code_module = request.form.get('code_module')
    nbre_heures = request.form.get('nbre_heures')
    intervention = {'id_contrat': id_contrat, 'code_module': code_module, 'nbre_heures': nbre_heures}
    util.add_intervention(intervention)
    return redirect(url_for('liste_interventions'))


@app.route('/del/interventions/<id_intervention>', methods=['GET', 'POST'])
def delete_intervention(id_intervention):
    util.delete_intervention(id_intervention)
    return redirect(url_for('liste_interventions'))


@app.route('/add/comptes', methods=['GET', 'POST'])
def add_compte():
    if request.method == 'GET':
        return render_template('add_compte.html')
    login = request.form.get('login')
    password = util.password_hash(request.form.get('password'))
    role = request.form.get('role')
    compte = {'login': login, 'password': password, 'role': role}
    util.add_compte(compte)
    return redirect(url_for('liste_comptes'))


@app.route('/del/comptes/<login>', methods=['GET', 'POST'])
def delete_compte(login):
    if request.method == 'GET':
        data = util.get_compte(login)
        return render_template('del_compte.html', data=data)
    util.delete_compte(login)
    return redirect(url_for('liste_comptes'))


# Pages de visualisation


@app.route('/enseignants')
def liste_enseignants():
    return render_template(f'enseignants.html', enseignants=util.get_all_enseignants())


@app.route('/vacataires')
def liste_vacataires():
    return render_template(f'vacataires.html', vacataires=util.get_all_vacataires())


@app.route('/modules')
def liste_modules():
    return render_template(f'modules.html', modules=util.get_all_modules())


@app.route('/interventions')
def liste_interventions():
    return render_template(f'interventions.html', interventions=util.get_all_interventions())


@app.route('/contrats')
def liste_contrats():
    return render_template(f'contrats.html', contrats=util.get_all_contrats_details())


@app.route('/comptes')
def liste_comptes():
    return render_template(f'comptes.html', comptes=util.get_comptes())


if __name__ == '__main__':
    app.run(debug=True, port=5001)
