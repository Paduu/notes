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

webapp_bp = Blueprint('webapp', __name__, url_prefix='/webapp')

# tempDB = []

@webapp_bp.route('/')
def index():
    return render_template('webapp/index.html')

@webapp_bp.route('/arbeitszeit')
def index_AM():
    today = date.today()
    return(redirect(url_for('webapp.view_AM', year=today.year, month=today.month)))


@webapp_bp.route('/arbeitszeit/<year>/<month>')
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
        return(redirect(url_for('webapp.view_AM', year=data.day.year, month=data.day.month)))

@webapp_bp.route('/arbeitszeit/edit/<id>',  methods=['POST', 'GET'])
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
        return(redirect(url_for('webapp.view_AM', year=data.day.year, month=data.day.month)))

@webapp_bp.route('/arbeitszeit/config/<year>/<month>',  methods=['POST', 'GET'])
def edit_AM(year, month):
    am = AM.query.filter_by(year=year, month=month).first()
    if request.method == 'GET':
        return(render_template('webapp/config_AM.html', am=am))
    else:
        am.hours_per_day = float(request.form['hpdAM'])
        am.work_percentage = float(request.form['wpAM']) / 100
        am.calc()
        db.session.commit()
        return(redirect(url_for('webapp.view_AM', year=am.year, month=am.month)))

@webapp_bp.route('/arbeitszeit/delete/<id>')
def delete_AT(id):
    data = AT.query.filter_by(day=id).first()
    db.session.delete(data)
    db.session.commit()
    return(redirect(url_for('webapp.view_AM', year=data.day.year, month=data.day.month)))

@webapp_bp.route('/arbeitszeit/task/delete/<id>')
def delete_AT_TASK(id):
    data = AT_TASK.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return(redirect(url_for('webapp.edit_AT', id=request.args.get('atId'))))


@webapp_bp.route('/notes')
def view_Notes():
    data = Notes.query.all()
    return render_template('webapp/view_Notes.html', data=data)

@webapp_bp.route('/notes/add', methods=['POST', 'GET'])
def add_Note():
    if request.method == 'GET':
        return render_template('webapp/add_Note.html')
    else:
        newNote = Notes(title=request.form['title'], note=request.form['note'])
        db.session.add(newNote)
        db.session.commit()
        return(redirect(url_for('webapp.view_Notes')))

@webapp_bp.route('/notes/edit/<id>', methods=['POST', 'GET'])
def edit_Note(id):
    data = Notes.query.filter_by(id=id).first()
    if request.method == 'GET':
        return(render_template('webapp/edit_Note.html', data=data))
    else:
        data.title = request.form['title']
        data.note = request.form['note']
        db.session.commit()
        return(redirect(url_for('webapp.view_Notes')))

@webapp_bp.route('/notes/delete/<id>')
def delete_Note(id):
    data = Notes.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return(redirect(url_for('webapp.view_Notes')))

