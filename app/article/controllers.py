from flask  import (
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
from app.article.forms import ArticleCreateForm,  ArticleUpdateForm
from app.authentication.models import User
from app.sections.models import Sections
from app.article.models import Article


mod_art = Blueprint('art', __name__, url_prefix='/art')


@mod_art.route('/create/', methods=['GET', 'POST'])
def article_create():
    if 'token' not in session:
        flash(u'You Need Login', 'error')
        return redirect(url_for('auth.signin'))
    user  = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    username = user.username
    form     = ArticleCreateForm()
    form.user_name.data = user.username
    if request.method == 'POST':
        if form.validate_on_submit():
            article = Article()
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
            return 'CREADO'
    return render_template('article/create.html', form=form , user=user, username=username)
    

@mod_art.route('/delete/', methods=['GET'])
def article_delete():
    if 'token' not in session:
        flash(u'You Need Login', 'error')
        return redirect(url_for('auth.signin'))
    user  = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    id = request.args.get('id',None)
    if(id):
        article = Article.query.filter_by(id=id).first()
        if(not (article is None)):
            db.session.delete(article)
            db.session.commit()
            flash(u'Article Deleted','messages')
        return redirect(url_for('art.article_views'))


@mod_art.route('/views/', methods=['GET'])
def article_views():
    if 'token' not in session:
        flash(u'You Need Login', 'error')
        return redirect(url_for('auth.signin'))
    user  = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    article = Article.find_by_author(user.username)
    return render_template("article/views.html", article = article)


@mod_art.route('/modify/', methods=['GET', 'POST'])
def article_update():
    if 'token' not in session:
        flash(u'You Need Login', 'error')
        return redirect(url_for('auth.signin'))
    user = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    form = ArticleUpdateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            section = str(form.section.data)
            section = section[section.find("'") + 1 : section.find(">") - 1]
            my_article = Article.find_by_id(form.id_article.data)
            my_article.section_name  = section
            my_article.title    = form.title.data
            my_article.body     = form.body.data
            db.session.commit()
            return 'update realizado'
    else:    
        id_article = request.args.get('id')
        my_article= Article.find_by_id(id_article)
        if user.username != my_article.user_name:
            return 'No tiene permisos'
        form.id_article.data    = id_article
        form.user_name.data     = my_article.user_name
        form.title.data         = my_article.title
        form.body.data          = my_article.body
        form.section.data       = my_article.section
    return render_template('article/update.html', form=form)