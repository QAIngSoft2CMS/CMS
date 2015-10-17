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


@mod_art.route('/create', methods=['GET', 'POST'])
def article_create():

    #if 'token' not in session:
    #    return redirect(url_for('signin'))    
    #id_user  = User.verify_token(session['token'])
    #user     = User.query.filter_by(id=id_user).first()
    user      = User.query.filter_by(email=session['email']).first()

    if user is None:        
        return redirect(url_for('auth.signin'))

    username = user.username
    article  = Article()
    form     = ArticleCreateForm()
    form.user_name.data = user.username
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
            return 'CREADO'
    return render_template('article/create.html', form=form , user=user, username=username)

    


@mod_art.route('/delete', methods=['GET', 'POST'])
def article_delete():
    form = ArticleDeleteForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            section = str(form.section.data)
            section = section[section.find("'") + 1 : section.find(">") - 1]
            article = Article.query.filter_by(user_name=session['user_name'], section_name=section, title=form.title.data).first()
            if(not (article is None)):
                db.session.delete(article)
                db.session.commit()
                return 'Article Deleted'
            flash(u'This Article not exist', 'error')
    return render_template('article/delete.html', form=form)
