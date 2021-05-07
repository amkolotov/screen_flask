from flask import render_template, send_from_directory, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

import app as screen
from app import app, db
from .forms import TaskForm
from .models import Task
from .services import get_screen


def get_page(req):
    page = req.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    return page


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', form=TaskForm())


@app.route('/create', methods=['POST'])
def create_task():
    """Создание новой задачи"""
    form = TaskForm()
    if form.validate_on_submit():
        try:
            url = form.data.get('url')
            filename = get_screen(url)
            task = Task(url=url, image=filename)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('task_list'))
        except Exception as e:
            print('Error: ', e)
    return redirect(url_for('index'))


@app.route('/list')
def task_list():
    page = get_page(request)
    tasks = Task.query.order_by(Task.created_at.desc())
    page_obj = tasks.paginate(page=page, per_page=screen.Configuration.PAGINATE_BY)
    return render_template('task_list.html', page_obj=page_obj)


@app.route('/screen/<int:task_id>')
def load_screen(task_id):
    """Скачивание скриншота"""
    task = Task.query.get_or_404(task_id)
    if task:
        try:
            task = Task.query.filter_by(id=task_id).first()
            return send_from_directory(screen.Configuration.MEDIA_DIR, filename=task.image, as_attachment=True)
        except FileNotFoundError:
            abort(404)


@app.route('/view/<int:task_id>')
def view_screen(task_id):
    """Просмотр скриншота в браузере"""
    task = Task.query.get_or_404(task_id)
    if task:
        try:
            task = Task.query.filter_by(id=task_id).first()
            return send_from_directory(screen.Configuration.MEDIA_DIR, filename=task.image)
        except FileNotFoundError:
            abort(404)


@app.route('/search')
def search():
    """Обработка поискового запроса"""
    search = request.args.get('search')
    page = get_page(request)
    if search:
        tasks = Task.query.filter(Task.url.ilike(f'%{search}%'))
        page_obj = tasks.paginate(page=page, per_page=len(list(tasks)))
        if page_obj:
            return render_template('task_list.html', page_obj=page_obj)

    return redirect(url_for('task_list'))
