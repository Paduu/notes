"""Database models"""
from datetime import datetime, date
from calendar import Calendar
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from .database import Base

class Notes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    note = Column(Text)
    created = Column(DateTime, default=datetime.now)

class AT(Base):
    __tablename__ = 'AT'
    day = Column(Date, primary_key=True)
    lunch_time = Column(Float, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    notes = Column(Text)
    tasks =  relationship('AT_TASK', backref=backref('at', lazy=True), cascade="all, delete")

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

class AT_TASK(Base):
    __tablename__ = 'AT_TASK'
    id = Column(Integer, primary_key=True)
    hours = Column(Float, nullable=False)
    task = Column(String(255), nullable=False)
    at_day = Column(Date, ForeignKey('AT.day'), nullable=False)

class AM(Base):
    __tablename__ = 'AM'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    hours_per_day = Column(Float, nullable=False)
    work_percentage = Column(Float, nullable=False)
    workdays = Column(Integer, nullable=False)
    total_hours_per_day = Column(Float, nullable=False)
    total_worktime_month = Column(Float, nullable=False)

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

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    todo = Column(String(255), nullable=False)
    done = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now)
