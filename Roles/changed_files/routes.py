"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from Roles.roles import getuserroles
from wiki.core import Processor
from wiki.web.forms import EditorForm, AddRoleForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.forms import CreateUserForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect


bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@login_required
@protect
def edit(url):
    if current_user.is_moderator() or current_user.is_admin():
        page = current_wiki.get(url)
        form = EditorForm(obj=page)
        if form.validate_on_submit():
            if not page:
                page = current_wiki.get_bare(url)
            form.populate_obj(page)
            page.save()
            flash('"%s" was saved.' % page.title, 'success')
            return redirect(url_for('wiki.display', url=url))
        return render_template('editor.html', form=form, page=page)
    return render_template('denied.html')


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@login_required
@protect
def move(url):
    if current_user.is_moderator() or current_user.is_admin():
        page = current_wiki.get_or_404(url)
        form = URLForm(obj=page)
        if form.validate_on_submit():
            newurl = form.url.data
            current_wiki.move(url, newurl)
            return redirect(url_for('wiki.display', url=newurl))
        return render_template('move.html', form=form, page=page)
    return render_template('denied.html')


@bp.route('/delete/<path:url>/')
@login_required
@protect
def delete(url):
    if current_user.is_admin():
        page = current_wiki.get_or_404(url)
        current_wiki.delete(url)
        flash('Page "%s" was deleted.' % page.title, 'success')
        return redirect(url_for('wiki.home'))
    return render_template('denied.html')


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/', methods=['GET', 'POST'])
def user_create():
    """
    This route will render the user creation page template, which consists
    of a form that the person on the web page can create a Wiki system user with.

    After submission of the form it will be validated and then created in the
    users.json file by the UserManager
    """
    form = CreateUserForm()
    if form.validate_on_submit():
        current_users.add_user(form.name.data, form.password.data)
        return redirect(url_for('wiki.user_login'))
    return render_template('user_create.html', form=form)


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


@bp.route('/roles/')
@login_required
def roles():
    if current_user.is_admin():
        users = current_users.read()
        user_names = [name for name in users.keys()]
        rolelist = getuserroles(users)
        return render_template('roles.html', nameswithroles=zip(user_names, rolelist))
    return render_template('denied.html')


@bp.route('/add_role/', methods=['GET', 'POST'])
def add_roll():
    form = AddRoleForm()
    if form.validate_on_submit():
        current_users.get_user(form.name.data).add_role(form.role.data)
        return redirect(url_for('wiki.roles'))
    return render_template('add_roll.html', form=form)


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

