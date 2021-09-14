from datetime import date, datetime
from calendar import Calendar
#from dateutil.relativedelta import relativedelta

class AT:
    """Class 'Arbeitstag' used to claculate Arbeitszeit"""

    def __init__(self, day=date.today()):
        self.lunch_time = 1
        self.day = day
        self.start = datetime.strptime('{0} 08:00'.format(day),  '%Y-%m-%d %H:%M')
        self.end = datetime.strptime('{0} 17:00'.format(day),  '%Y-%m-%d %H:%M')

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

class AM:
    """Class 'Arbeitsmonat' used to claculate Arbeitszeit"""

    def __init__(self, year=None, month=None):
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
        self.year = year
        self.month = month
        # set the days you have to work (at 100% pensum)
        self.hours_per_day = 8
        # set the percentage you work per day
        self.work_percentage = 0.9
        self.calc()
    
    def __repr__(self):
        return('arbeitszeit.AM({0}, {1})'.format(self.year, self.month))

    def calc(self):
        """(Re-)Calculate the totals"""
        calendar=Calendar()
        self.day_table = [x for x in calendar.itermonthdays4(self.year, self.month) if x[1] == self.month]
        self.workday_table = [x for x in self.day_table if x[3] in range(0,5)]
        self.workdays = len(self.workday_table)
        self.total_hours_per_day = self.hours_per_day * self.work_percentage
        self.total_worktime_month = self.workdays * self.total_hours_per_day
        return(None)

    def print_stats(self):
        """Print statistics, only for debug purpose"""
        print('Year/Month: {0}/{1}'.format(self.year, self.month))
        print('Workdays (Mo-Fr): {0}'.format(self.workdays))
        print('Hours per day: {0}'.format(self.hours_per_day))
        print('Work percentage: {0}'.format(self.work_percentage))
        print('Total time to work: {0}'.format(self.total_worktime_month))



if __name__ == '__main__':
    pass

