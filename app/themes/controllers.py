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
from app import db
from app import vglobs
from app import app
from app.authentication.constants import ReadRole, CommentRole, WriteRole
from app.authentication.models import User
#from app.themes.forms import ConfigurationForm
from app.themes.forms import UpdateTheme
from app.themes.models import Theme
from werkzeug import secure_filename
#from flask_wtf import From
from flask_wtf.file import FileField
from wtforms import StringField
from wtforms.validators import DataRequired
import os

mod_theme = Blueprint('themes', __name__, url_prefix='/themes')


@mod_theme.route('/config', methods=['GET', 'POST'])
def configuration_theme():
    if 'token' not in session:
        return redirect(url_for('auth.signin'))
    user = User.verify_token(session['token'])
    if user is None:
        flash(u'Token Time Out', 'error')
        return redirect(url_for('auth.signin'))
    if not user.role>>2:
        #return acces denied
        abort(401)
    form = ConfigurationForm()
    form.user_name.data = user.username
    if request.method == 'POST':
        if form.validate():
        #falta mejorar el logo
            theme = Theme(name=form.name.data,
                          default_use=form.default_use.data,
                          title=form.title.data,
                          #
                          logo=form.logo.data,
                          #
                          resources='themes/'+name,
                          description=form.description.data,
                          username=form.user_name.data)
            db.session.add(theme)
            db.session.commit()
            return redirect(url_for('auth.profile'))
    #return render_template("themes/configuration.html", form=form)


@mod_theme.route('/delete_theme/', methods=['GET','POST'])
def delete_theme():
    id_ = request.args.get('id',None)
    theme = Theme.query.get(id_)
    db.session.delete(theme)
    db.session.commit()
    return redirect("/themes/view_themes")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in vglobs.ALLOWED_EXTENSIONS

@mod_theme.route('/upload_theme/', methods=['GET', 'POST'])
def upload_theme():
    #if 'token' not in session:
    #    return redirect(url_for('auth.signin'))
    #user = User.verify_token(session['token'])
    #if user is None:
    #    flash(u'Token Time Out', 'error')
    #    return redirect(url_for('auth.signin'))
    if request.method == 'POST':
        form = UpdateTheme(csrf_enabled=False)
        if form.validate_on_submit():
            if form.fileMarkdown.data:
                #app.config['UPLOAD_FOLDER'] = vglobs.UPLOAD_FOLDE
                file = request.files['fileMarkdown']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('themes/update.html',form=form)
    else:
        form = UpdateTheme(csrf_enabled=False)
        return render_template('themes/update.html',form=form)
