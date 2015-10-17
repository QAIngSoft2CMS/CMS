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
from app.article.forms import ArticleCreateForm, ArticleDeleteForm
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
    

@mod_art.route('/delete/', methods=['GET', 'POST'])
def article_delete():
    if 'token' not in session:
        flash(u'You Need Login', 'error')
        return redirect(url_for('auth.signin'))
    user  = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    form = ArticleDeleteForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            section = str(form.section.data)
            section = section[section.find("'") + 1 : section.find(">") - 1]
            article = Article.query.filter_by(user_name=user.username, section_name=section, title=form.title.data).first()
            if(not (article is None)):
                db.session.delete(article)
                db.session.commit()
                return 'Article Deleted'
            flash(u'This Article not exist', 'error')
    return render_template('article/delete.html', form=form)


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
    user  = User.verify_token(session['token'])
    if user is None:
        return redirect(url_for('auth.signin'))
    
    id_article = request.args.get('id')    
    my_article= Article.find_by_id(id_article)    
    
    if user.username != my_article.user_name:
        return 'No tiene permisos'

    form      = ArticleCreateForm()
    form.user_name.data = my_article.user_name
    form.title.data     = my_article.title
    form.body.data      = my_article.body
    form.section.data   = my_article.section
    
    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.delete(article)
            db.session.commit()
            return 'Article updated'
    
    return render_template('article/update.html', form=form, id=id)
