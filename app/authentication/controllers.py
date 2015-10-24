from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)

from app import app, db, mail

from app.authentication.constants import ReadRole, CommentRole, WriteRole
from app.authentication.forms import LoginForm, SignupForm
from app.authentication.models import User

from app.authentication.forms import RecoverPassForm, ResetPasswordSubmit
from flask_mail import Mail, Message
from flask.ext.login import login_required, logout_user
from werkzeug import check_password_hash, generate_password_hash

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('auth.signin'))


@mod_auth.route('/profile')
def profile():

    if 'token' not in session:
        return redirect(url_for('auth.signin'))
    user = User.verify_token(session['token'])
    if user is None:
        flash(u'Token Time Out', 'error')
        return redirect(url_for('auth.signin'))
    else:
        return render_template('authentication/profile.html')


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if ('token' in session) and (User.verify_token(session['token'])):
        return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        if form.validate() == False:
            return render_template("authentication/signup.html", form=form)
        else:
            new_user = User(form.username.data, form.email.data,\
             form.password.data,ReadRole+CommentRole+WriteRole,1)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            session['token'] = new_user.generate_token()
            session['email'] = new_user.email
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        return render_template("authentication/signup.html", form=form)


@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    form = LoginForm(request.form)
    if 'token' in session:
        user = User.verify_token(session['token'])
        if user:
            return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            session['user_id'] = user.id
            session['token'] = user.generate_token()
            session['email'] = user.email
            return redirect(url_for('auth.profile'))
    return render_template("authentication/signin.html", form=form)


@mod_auth.route('/recover_pass/', methods=('GET','POST'))
def recover_pass():
    form = RecoverPassForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_token()
            print token
            url = 'http://0.0.0.0:8080/auth/change_pass?token=' + token
            send_mail(email,url)
            return render_template("authentication/confirm.html",email=email)
    return render_template("authentication/recover_pass.html", form=form)


@mod_auth.route('/change_pass/', methods=['GET','POST'])
def change_pass():
    token = request.args.get('token',None)
    verified_result = User.verify_token_email(token)
    if token and verified_result:
        print verified_result
        password_submit_form = ResetPasswordSubmit(request.form)
        if password_submit_form.validate_on_submit():
            verified_result.password = generate_password_hash(password_submit_form.password.data)
            db.session.commit()
            flash("password updated successfully")
            return render_template('authentication/base.html')
        return render_template("authentication/change_pass.html",form=password_submit_form)      


def send_mail(email,url):
    msg = Message("Recupera tu Contrasenia", sender="pruebas.cms@asacoop.com",
    recipients=[email])
    msg.body = "Este mensaje te llego porque solicitaste recuperar tu contrasenia, utiliza esta direccion de correo " + url
    mail.send(msg)


@mod_auth.route('/logout/')
def logout():
	return render_template("authentication/logout.html")