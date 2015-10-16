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
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.article.forms import ArticleCreateForm, SectionCreateForm
from app.authentication.models import User
from app.sections.models import Sections
from app.article.models import Article


mod_art = Blueprint('art', __name__, url_prefix='/art')


@mod_art.route('/create', methods=['GET', 'POST'])
def article_create():
    if 'email' not in session:
        return redirect(url_for('sigin'))
    user     = User.query.filter_by(email=session['email']).first()
    username = user.username
    article  = Article()
    form     = ArticleCreateForm()
    form.user_name.data = user.username
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('user/create.html', form=form, user=user, username=username)

@mod_art.route('/section/create', methods=['GET', 'POST'])
def section():
    form = SectionCreateForm()
    if form.validate_on_submit():
        section = Sections()
        person = Person.query.filter_by(email=session['email']).first()
        name = person.firstname
        if form.validate_on_submit():
            form.populate_obj(section)
            db.session.add(section)
            db.session.commit()
            return redirect(url_for('dashboard', name=name))
    return render_template('cat_create.html', form=form)

