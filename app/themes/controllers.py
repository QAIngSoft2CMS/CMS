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
from app.authentication.constants import ReadRole, CommentRole, WriteRole
from app.authentication.models import User
from app.themes.forms import ConfigurationForm
from app.themes.forms import SearchThemeForm
from app.themes.models import Theme

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
    return render_template("themes/configuration.html", form=form)

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
            session['user_name'] = user.username
            return redirect(url_for('auth.profile'))
    return render_template("authentication/signin.html", form=form)

@mod_theme.route('/delete_theme/', methods=['GET','POST'])
def delete_theme():
    id_ = request.args.get('id',None)
    theme = Theme.query.get(id_)
    db.session.delete(theme)
    db.session.commit()
    return redirect("/themes/view_themes")

@mod_theme.route('/view_themes/')
def view_themes():
    
    themes_filter = Theme.query.filter().all()
    return render_template("themes/view_themes.html",themes = themes_filter)
    
@mod_theme.route('/search_filter/',methods=['GET', 'POST'])
def view_search_themes_filter():
    
    id_theme = request.args.get("id")
    name_theme = request.args.get("name")
    str_name_theme = '%'+str(name_theme)+'%'
    
    if (id_theme == '') and (name_theme != ''):
        themes_filter = Theme.query.filter(Theme.name.ilike(str_name_theme)).all()
        return render_template("themes/view_themes.html",themes = themes_filter)
    
    elif (name_theme == '') and (id_theme != ''):
        themes_filter = Theme.query.filter_by(id=id_theme).all()
        return render_template("themes/view_themes.html",themes = themes_filter)

    themes_filter = Theme.query.filter_by(id=id_theme,name = name_theme).all()
    return render_template("themes/view_themes.html",themes = themes_filter)

@mod_theme.route('/search_theme',methods=('GET','POST')) 
def search_themes():

    form = SearchThemeForm()
    if form.validate():
        id_theme = form.id.data
        name_theme = form.name.data
        if (id_theme == '') and (name_theme == ''):
            return redirect(url_for('themes.view_themes'))
        return redirect(url_for('themes.view_search_themes_filter',id=id_theme,name=name_theme))
    return render_template("themes/search.html", form=form)

