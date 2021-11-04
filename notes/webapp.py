from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    current_app,
    flash,
    session,
    url_for,
)

from .models import *
from .config import Config
from datetime import date
from dateutil import relativedelta
from sqlalchemy import extract
from functools import wraps
import os

webapp_bp = Blueprint('webapp', __name__, url_prefix='/webapp')

@webapp_bp.before_request
def force_https():
    if request.url.startswith('http://'):
        return redirect(request.url.replace('http://', 'https://'))

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('webapp.login'))
    return wrapper

@webapp_bp.route('/login',  methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('webapp/login.html')
    else:
        if request.form['access_key'] == Config.APP_ACCESS_KEY:
            session['logged_in'] = True
            return redirect(url_for('webapp.index'))
        else:
            return render_template('webapp/login.html'), 401

@webapp_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('webapp.index'))

@webapp_bp.route('/')
@auth_required
def index():
    return render_template('webapp/index.html')

@webapp_bp.route('/arbeitszeit')
@auth_required
def index_AM():
    today = date.today()
    return redirect(url_for('webapp.view_AM', year=today.year, month=today.month))


@webapp_bp.route('/arbeitszeit/<year>/<month>')
@auth_required
def view_AM(year, month):
    d = date(int(year), int(month), 1)
    am = AM.query.filter_by(year=d.year, month=d.month).first()
    if am == None:
        am = AM()
        am.year = d.year
        am.month = d.month
        am.hours_per_day = Config.APP_WORKDAY_HOURS
        am.work_percentage = Config.APP_WORK_PERCENTAGE
        am.calc()
        db.session.add(am)
        db.session.commit()
    data =  AT.query.filter(extract('month', AT.day) == d.month, extract('year', AT.day) == d.year).order_by(AT.day).all()
    total = sum([e.calc() for e in data])
    mprev = d - relativedelta.relativedelta(months=1)
    mnext = d + relativedelta.relativedelta(months=1)
    return render_template('webapp/view_AM.html', data=data, total=total, am=am, mprev=mprev, mnext=mnext)

@webapp_bp.route('/arbeitszeit/add',  methods=['POST', 'GET'])
@auth_required
def add_AT():
    if request.method == 'GET':
        return render_template('webapp/add_AT.html')
    else:
        data = AT()
        # depricated:
        # data.day = datetime.strptime(request.form['dateAT'], '%Y-%m-%d').date()
        year, month, day = request.form['dateAT'].split('-')
        data.updateDay(year, month, day)
        data.updateStart(request.form['beginAT'])
        data.updateEnd(request.form['endAT'])
        data.lunch_time = float(request.form['lunchAT'])
        data.notes = request.form['notesAT']
        db.session.add(data)
        # add tasks
        tasks = [(request.form.get('hoursTask{0}'.format(x)),
                request.form.get('taskTask{0}'.format(x))) for x in range(1,9)]
        for task in tasks:
            if task != (None, None):
                t = AT_TASK()
                t.hours = float(task[0])
                t.task = task[1]
                t.at = data
                db.session.add(t)
        db.session.commit()
        return redirect(url_for('webapp.view_AM', year=data.day.year, month=data.day.month))

@webapp_bp.route('/arbeitszeit/edit/<id>',  methods=['POST', 'GET'])
@auth_required
def edit_AT(id):
    data = AT.query.filter_by(day=id).first()
    if request.method == 'GET':
        return render_template('webapp/edit_AT.html', data=data)
    else:
        year, month, day = request.form['dateAT'].split('-')
        data.updateDay(year, month, day)
        data.updateStart(request.form['beginAT'])
        data.updateEnd(request.form['endAT'])
        data.lunch_time = float(request.form['lunchAT'])
        data.notes = request.form['notesAT']
        # update already existing tasks
        for task in data.tasks:
            task.hours = float(request.form.get('hoursId{0}'.format(task.id)))
            task.task = request.form.get('taskId{0}'.format(task.id))
        # newly added tasks
        tasks = [(request.form.get('hoursTask{0}'.format(x)),
                request.form.get('taskTask{0}'.format(x))) for x in range(1,9)]
        for task in tasks:
            if task != (None, None):
                t = AT_TASK()
                t.hours = float(task[0])
                t.task = task[1]
                t.at = data
                db.session.add(t)
        db.session.commit()
        return redirect(url_for('webapp.view_AM', year=data.day.year, month=data.day.month))

@webapp_bp.route('/arbeitszeit/config/<year>/<month>',  methods=['POST', 'GET'])
@auth_required
def edit_AM(year, month):
    am = AM.query.filter_by(year=year, month=month).first()
    if request.method == 'GET':
        return(render_template('webapp/config_AM.html', am=am))
    else:
        am.hours_per_day = float(request.form['hpdAM'])
        am.work_percentage = float(request.form['wpAM']) / 100
        am.calc()
        db.session.commit()
        return redirect(url_for('webapp.view_AM', year=am.year, month=am.month))

@webapp_bp.route('/arbeitszeit/delete/<id>')
@auth_required
def delete_AT(id):
    data = AT.query.filter_by(day=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('webapp.view_AM', year=data.day.year, month=data.day.month))

@webapp_bp.route('/arbeitszeit/task/delete/<id>')
@auth_required
def delete_AT_TASK(id):
    data = AT_TASK.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('webapp.edit_AT', id=request.args.get('atId')))


@webapp_bp.route('/notes')
@auth_required
def view_Notes():
    data = Notes.query.all()
    return render_template('webapp/view_Notes.html', data=data)

@webapp_bp.route('/notes/add', methods=['POST', 'GET'])
@auth_required
def add_Note():
    if request.method == 'GET':
        return render_template('webapp/add_Note.html')
    else:
        newNote = Notes(title=request.form['title'], note=request.form['note'])
        db.session.add(newNote)
        db.session.commit()
        return redirect(url_for('webapp.view_Notes'))

@webapp_bp.route('/notes/edit/<id>', methods=['POST', 'GET'])
@auth_required
def edit_Note(id):
    data = Notes.query.filter_by(id=id).first()
    if request.method == 'GET':
        return(render_template('webapp/edit_Note.html', data=data))
    else:
        data.title = request.form['title']
        data.note = request.form['note']
        db.session.commit()
        return redirect(url_for('webapp.view_Notes'))

@webapp_bp.route('/notes/delete/<id>')
@auth_required
def delete_Note(id):
    data = Notes.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('webapp.view_Notes'))

@webapp_bp.route('/todo')
@auth_required
def view_Todos():
    data = Todo.query.all()
    return render_template('webapp/view_Todos.html', data=data)

@webapp_bp.route('/todo/add', methods=['POST'])
@auth_required
def add_Todo():
        newTodo = Todo(todo=request.form['todo'])
        db.session.add(newTodo)
        db.session.commit()
        return redirect(url_for('webapp.view_Todos'))

@webapp_bp.route('/todo/change', methods=['POST'])
@auth_required
def change_Todo():
    data = Todo.query.filter_by(id=request.form['id']).first()
    data.done = True if request.form['checked'] == 'true' else False
    db.session.commit()
    return redirect(url_for('webapp.view_Todos'))


@webapp_bp.route('/todo/delete', methods=['POST'])
@auth_required
def delete_Todo():
    for item in request.form:
        data = Todo.query.filter_by(id=int(item[4:])).first()
        db.session.delete(data)
    db.session.commit()
    return redirect(url_for('webapp.view_Todos'))
