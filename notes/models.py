"""Database models"""
from . import db
from datetime import datetime, date
from calendar import Calendar

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)

class AT(db.Model):
    day = db.Column(db.Date, primary_key=True)
    lunch_time = db.Column(db.Float, nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    tasks =  db.relationship('AT_TASK', backref=db.backref('at', lazy=True), cascade="all, delete")

    def __repr__(self):
        return('arbeitszeit.AT({0})'.format(self.day))

    def calc(self):
        return(((self.end - self.start).seconds/3600) - self.lunch_time)

    def getStart(self):
        return(self.start.strftime('%H:%M'))

    def getEnd(self):
        return(self.end.strftime('%H:%M'))

    def updateStart(self, t):
        # t (time) has to be passed in format HH:MM e.g. 08:00
        self.start = datetime.strptime('{0} {1}'.format(self.day, t),  '%Y-%m-%d %H:%M')

    def updateEnd(self, t):
        # t (time) has to be passed in format HH:MM e.g. 17:00
        self.end = datetime.strptime('{0} {1}'.format(self.day, t),  '%Y-%m-%d %H:%M')
    
    def updateDay(self, year, month, day):
        # set a new date
        self.day = date(int(year), int(month), int(day))

class AT_TASK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Float, nullable=False)
    task = db.Column(db.String(255), nullable=False)
    at_day = db.Column(db.Date, db.ForeignKey('AT.day'), nullable=False)

class AM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    hours_per_day = db.Column(db.Float, nullable=False)
    work_percentage = db.Column(db.Float, nullable=False)
    workdays = db.Column(db.Integer, nullable=False)
    total_hours_per_day = db.Column(db.Float, nullable=False)
    total_worktime_month = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return('arbeitszeit.AM({0}, {1})'.format(self.year, self.month))

    def calc(self):
        """(Re-)Calculate the totals"""
        calendar=Calendar()
        self.day_table = [x for x in calendar.itermonthdays4(self.year, self.month) if x[1] == self.month]
        self.workday_table = [x for x in self.day_table if x[3] in range(0,5)]
        self.workdays = len(self.workday_table)
        self.total_hours_per_day = self.hours_per_day * self.work_percentage
        self.total_worktime_month = round(self.workdays * self.total_hours_per_day, 1)
        return(None)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now)
