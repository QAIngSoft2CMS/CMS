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

from app import app, db
from app.sections.forms import CreateSectionForm, EditSectionForm
from app.sections.models import Sections


mod_sec = Blueprint('sec', __name__, url_prefix='/sec')

@mod_sec.route('/views_sections/')
def views_sections():
    sections = Sections.query.filter().all()
    return render_template("sections/view_sections.html", sections = sections)

@mod_sec.route('/create_sections/', methods=['GET', 'POST'])
def create_section():
    form = CreateSectionForm(request.form)
    if form.validate_on_submit():
        section = Sections(form.section.data, form.description.data)
        db.session.add(section)
        db.session.commit()
        flash("sections created")
        return redirect("/sec/views_sections")
    return render_template("sections/create_sections.html",form = form)

@mod_sec.route('/modify_sections/', methods=['GET','POST'])
def modify_sections():
    
    id_  = request.args.get('id',None)
    section = Sections.query.get(id_)

    form_edit = EditSectionForm(request.form)
    
    if form_edit.validate_on_submit():
        section.section_name = form_edit.section.data
        section.description =  form_edit.description.data
        db.session.commit()
        flash("Row edited")
        return redirect("/sec/views_sections")
    return render_template("sections/modify_sections.html",form = form_edit)

@mod_sec.route('/delete_sections/', methods=['GET','POST'])
def delete_sections():
   
   id_  = request.args.get('id',None)
   section = Sections.query.get(id_)
   print section
   db.session.delete(section)
   db.session.commit()
   flash("Row Deleted")
   return redirect("/sec/views_sections")