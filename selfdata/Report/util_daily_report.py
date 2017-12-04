import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg') #TODO: Enable this to make it work for web
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import seaborn as sns
from sklearn.linear_model import LinearRegression
import datetime
from dateutil import relativedelta
from selfdata.Report.util_report_config import daily_config, tbl_name_web_temp
import os
from peahead.settings import BASE_DIR


# Config related
file_loc = r'D:\MEGAsync\3 Workspace\1_Projects\2_peahead-sammy\selfdata_01.db'
# file_loc = r'D:\OneDrive\0 My Files\0 System\3 Workspace\PycharmProjects\1 Personal Host Git\1 SelfData\Cleaning\selfdata_01.db'


# =====================

conn = sqlite3.connect(file_loc, check_same_thread=False)
c = conn.cursor()

# ====================

def df_with_query(table, date_name, start_date, end_date):


    query = '''
    SELECT * FROM {}
    WHERE "{}" BETWEEN date("{}") AND date("{}")
    '''.format(table, date_name, start_date, end_date)

    df = pd.read_sql(query, con=conn)
    return df


def plot_monthly_old(series_dates, series_record, tbl_name, start_date, end_date, style='seaborn-pastel', save=True):

    series_dates = pd.to_datetime(series_dates, format="%Y-%m-%d %H:%M:%S")

    # date_list is require to create x-axis
    dates_list = []
    for i in series_dates:
        dates_list.append(i)

    # date1 = dates_list[0]
    # date2 = dates_list[len(dates_list)-1]

    # print(dates_list[0])

    # Best fit line

    df_temp = pd.DataFrame()
    df_temp['days_since'] = (series_dates - pd.to_datetime(dates_list[0])).astype('timedelta64[D]')

    lr = LinearRegression()
    # print(len(series_dates))
    # print(len(df_temp['days_since']))
    # print(len(series_record))

    lr.fit(df_temp[['days_since', ]], series_record)
    predict = lr.predict(df_temp[['days_since', ]])



    # Styling needs to be at top.
    plt.style.use(style)

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Ubuntu Mono'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12




    # Main part

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([0,1,2,3], [1,2,4,1])
    ax.plot(dates_list, series_record, c='#DCD6F7', alpha=0.3) #dashes=(1,10), dash_capstyle='round', dash_joinstyle='round'
    ax.scatter(dates_list, series_record, c='#4E4C67', s=20, alpha=0.8)

    ax.plot(dates_list, predict, c='#A6B1E1', solid_capstyle='round')

    #print(plt.style.available)

    # sns.lmplot(dates_list, series_record, data=series_record, fit_reg=True)
    # plt.gcf().autofmt_xdate()

    # Intelligently scaling x-axis labels

    # If it's under 3 month
    if len(series_dates) < 110:
        years = YearLocator()   # every year
        months = MonthLocator(interval=1)  # every month
        days = DayLocator(bymonthday=range(1,31,7)) #, interval=5
        loc = WeekdayLocator(byweekday=MO)
        dateFmt_Maj = DateFormatter('%d-%m-%Y %a')
        dateFmt_Min = DateFormatter('%d')

        # format the ticks
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(dateFmt_Min)
        # ax.autoscale_view()
    #if it's over 3 month and under year (ish)
    elif len(series_dates) >= 110 and len(series_dates) < 350:
        years = YearLocator()   # every year
        months = MonthLocator(interval=1)  # every month
        days = DayLocator(bymonthday=range(7,31,7)) #, interval=5
        dateFmt_Maj = DateFormatter('%d-%m')
        dateFmt_Min = DateFormatter('%d')

        # format the ticks
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(dateFmt_Min)
    else:
        years = YearLocator()   # every year
        months = MonthLocator(interval=3)  # every month
        #days = DayLocator(bymonthday=range(1,31,7)) #, interval=5
        loc = WeekdayLocator(byweekday=MO)
        dateFmt_Maj = DateFormatter('%Y')
        dateFmt_Min = DateFormatter('%m')

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_minor_formatter(dateFmt_Min)


    # Intelligently plot y-axis range

    lim_list = set_min_max_record(tbl_name, series_record.name, start_date, end_date)
    # print('lim_list'.format(lim_list))
    # print(start_date)
    # print(type(start_date))
    # print(end_date)
    ax.set_ylim(lim_list)

    # Plot x-range so it shows whole of x-axis instead of streching from where data is available.

    days = 1 # So edge values of x-axis doesn't get cut.
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + relativedelta.relativedelta(days=-days)
    # print(start_date)
    # print(type(start_date))
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date + relativedelta.relativedelta(days=+days)


    ax.set_xlim([start_date, end_date])


    # name axis
    ax.set_xlabel(removeUnderLine(series_dates.name), color='#5c5f6d')
    ax.set_ylabel(removeUnderLine(series_record.name), color='#5c5f6d')
    ax.set_title(removeUnderLine(tbl_name), color='#5c5f6d') #'#B4869F'


    # def price(x):
    #     return '$%1.2f' % x
    # ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    # ax.fmt_ydata = price
    # ax.grid(True)

    fig.autofmt_xdate()

    if save:


        # Format file name to save
        file_date_start = datetime.datetime.strftime(series_dates.iloc[0], '%Y-%m-%d')
        file_date_end = datetime.datetime.strftime(series_dates.iloc[len(series_dates)-1], '%Y-%m-%d')

        # fil_name = '{}_{}_to_{}_a01.png'.format(tbl_name, file_date_start, file_date_end)
        # print(fil_name)
        # plt.savefig(fil_name)
        sav_name = tbl_name_web_temp[tbl_name]
        my_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(my_path)
        print(f'saving as {sav_name}')
        # plt.savefig(os.path.join(my_path, 'static', sav_name + '.svg'), format='svg')
        print('new staic produdction loc')
        print(os.path.join(BASE_DIR, 'static', sav_name + '_qwerty_' +'.svg'))
        plt.savefig(os.path.join(BASE_DIR, 'static', sav_name + '_qwerty_' +'.svg'), format='svg')
        fig.clf()
        plt.clf()
        plt.close(fig)



def plot_monthly(series_dates, series_record, tbl_name, start_date, end_date, style='fivethirtyeight', save=True):

    series_dates = pd.to_datetime(series_dates, format="%Y-%m-%d %H:%M:%S")

    # date_list is require to create x-axis
    dates_list = []
    for i in series_dates:
        dates_list.append(i)

    # Best fit line
    df_temp = pd.DataFrame()
    df_temp['days_since'] = (series_dates - pd.to_datetime(dates_list[0])).astype('timedelta64[D]')
    lr = LinearRegression()
    lr.fit(df_temp[['days_since', ]], series_record)
    predict = lr.predict(df_temp[['days_since', ]])

    # Styling needs to be at top.

    plt.style.use(style)

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Ubuntu Mono'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12


    # Main part

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates_list, series_record, c='#DCD6F7', alpha=0.3, linewidth=1.5) #dashes=(1,10), dash_capstyle='round', dash_joinstyle='round'

    # Disabled for better visual
    ax.scatter(dates_list, series_record, c='#DCD6F7', s=2, alpha=0.8)

    # Best fit average
    ax.plot(dates_list, predict, c='#A6B1E1', solid_capstyle='round', linewidth=2)



    # Intelligently scaling x-axis labels

    # Under 1 month
    if len(series_dates) < 32:
        days = DayLocator(bymonthday=range(1,31,7)) #, interval=5
        loc = WeekdayLocator(byweekday=MO)
        dateFmt_Maj = DateFormatter('\n%a')
        dateFmt_Min = DateFormatter('%d')

        # format the ticks
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(dateFmt_Min)

    # If it's under 3 month
    elif len(series_dates) < 110:
        days = DayLocator(bymonthday=range(1,31,7)) #, interval=5
        months = MonthLocator(interval=1)  # every month
        dateFmt_Maj = DateFormatter('\n%m')
        dateFmt_Min = DateFormatter('%d')

        # format the ticks
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_minor_formatter(dateFmt_Min)


    #if it's over 3 month and under year (ish)
    elif len(series_dates) >= 110 and len(series_dates) < 370:
        months = MonthLocator(interval=1)  # every month
        days = DayLocator(bymonthday=range(7,31,7)) #, interval=5
        dateFmt_Maj = DateFormatter('\n%m')
        # dateFmt_Min = DateFormatter('%d')

        # format the ticks
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(days)
        # ax.xaxis.set_minor_formatter(dateFmt_Min)
    else:
        years = YearLocator()   # every year
        months = MonthLocator(interval=3)  # every 3 months
        dateFmt_Maj = DateFormatter('\n%Y')
        dateFmt_Min = DateFormatter('%m')

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(dateFmt_Maj)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_minor_formatter(dateFmt_Min)


    # Intelligently plot y-axis range

    lim_list = set_min_max_record(tbl_name, series_record.name, start_date, end_date)
    ax.set_ylim(lim_list)

    # Plot x-range so it shows whole of x-axis instead of streching from where data is available.
    days = 1 # So edge values of x-axis doesn't get cut.
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date + relativedelta.relativedelta(days=-days)
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date + relativedelta.relativedelta(days=+days)

    ax.set_xlim([start_date, end_date])


    # name axis
    ax.set_xlabel(removeUnderLine(series_dates.name), color='#ffffff')
    ax.set_ylabel(removeUnderLine(series_record.name), color='#ffffff')
    # ax.set_title(removeUnderLine(tbl_name), color='#ffffff') #'#B4869F'

    # Final Customization
    # ax.tick_params(bottom='off', top='off', left='off', right='off')
    ax.tick_params(axis='x', which='both', colors='white')
    ax.tick_params(axis='y', which='both', colors='white')
    for key, spine in ax.spines.items():
        spine.set_visible(False)

    fig.set_facecolor('#474e5d')
    ax.set_facecolor('#474e5d')



    if save:
        # Format file name to save
        file_date_start = datetime.datetime.strftime(series_dates.iloc[0], '%Y-%m-%d')
        file_date_end = datetime.datetime.strftime(series_dates.iloc[len(series_dates)-1], '%Y-%m-%d')

        # fil_name = '{}_{}_to_{}_a01.png'.format(tbl_name, file_date_start, file_date_end)
        # print(fil_name)
        # plt.savefig(fil_name)
        sav_name = tbl_name_web_temp[tbl_name]
        my_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(my_path)
        print(f'saving as {sav_name}')


        # Use this for production
        plt.savefig(os.path.join(BASE_DIR, 'static', sav_name + '.svg'), format='svg', facecolor=fig.get_facecolor())
        # Use this for dev
        plt.savefig(os.path.join(my_path, 'static', sav_name + '.svg'), format='svg', facecolor=fig.get_facecolor())


        fig.clf()
        plt.clf()
        plt.close(fig)







# Removes underline and Cap the every word.
def removeUnderLine(string):
    string_fixed = string.replace("_", " ")
    string_fixed = string_fixed.title()
    return string_fixed

# Used to find find range of y-axis
def min_max_record(tbl_name, col):

    query = '''
    SELECT {tbl_name}.{col} FROM {tbl_name}
    '''.format(col=col, tbl_name=tbl_name)
    # print(query)

    series = pd.read_sql(query, con=conn)
    series_max = series.max()
    series_min = series.min()
    return series_min, series_max

# Returns array to set for y_lim (or x_lim)
def set_min_max_record(tbl_name, col, start_date, end_date):

    if tbl_name in daily_config:
        print('table( {} ) found in config. Using config to set y_lim'.format(tbl_name))

        # offset value not used yet

        config = daily_config[tbl_name]

        y_lim_offset = config['y_lim_offset']
        tbl_name = tbl_name
        date_name = config['date_name']
        y_axis = config['y_axis']
        y_lim_offset_percentage = config['y_lim_offset_percentage']

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date + relativedelta.relativedelta(months=-y_lim_offset)
        # print(start_date)
        # print(type(start_date))
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_date + relativedelta.relativedelta(months=+y_lim_offset)
        # print(end_date)
        # print(type(end_date))


        df = df_with_query(tbl_name, date_name, start_date, end_date)
        series = df[y_axis]
        series_max = series.max()
        series_min = series.min()
        lim_min = series_min
        lim_max = series_max
        percent = ((lim_min+lim_max)/2)*y_lim_offset_percentage
        print('offset percentage value: '.format(percent))
        return [lim_min-percent, lim_max+percent]
        # return [lim_min-1, lim_max+1]

    else:
        print("not custom auto setting y-axis")


# Find previous or x month
#By default month finds only that month.
def find_dates(year, month, month_lenth=0):


    start_date = datetime.datetime(year, month, 1)
    end_date = start_date + relativedelta.relativedelta(months=+month_lenth+1, days=-1)


    # SQLlite wants between date to be smaller, greater first in query. To satisfy little logic to allow negative month_lenth
    if start_date > end_date:
        temp_start_date = start_date
        temp_end_date = end_date
        start_date = temp_end_date
        end_date = temp_start_date
        start_date = datetime.datetime(start_date.year, start_date.month, 1)
        end_date = end_date + relativedelta.relativedelta(days=-1)


    # Due to SQL returning string, other function to draw graph expects string formatted time.
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    return start_date, end_date



# For looking at whole of df
    query = '''
    SELECT "{col}" FROM {tbl_name}
    '''.format(col=col, tbl_name=tbl_name)

    # print(query)

    series = pd.read_sql(query, con=conn)
    # print(type(series))
    # print(series)
    series_max = series.max()
    series_min = series.min()
    lim_min = series_min.iloc[0]
    lim_max = series_max.iloc[0]
    ten_percent = ((lim_min+lim_max)/2)*0.10

    # print('lim min: {}'.format(lim_min))
    # print('lim max: {}'.format(lim_max))

    return [lim_min-ten_percent, lim_max+ten_percent]


if __name__ == '__main__':

    """
    tbl_name = 'weather_daily'
    date_name = 'Date'
    start_date = '2017-03-01'
    end_date = '2017-04-01'
    y_axis = 'Temp_mean'


    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name)


    #min_max_record(tbl_name='mood', col='mood')
    #min_max_record(tbl_name='weather_daily', col='Temp_mean')
    """

    """
    tbl_name = 'mood'
    date_name = 'Date'
    start_date = '2017-01-01'
    end_date = '2017-04-01'
    y_axis = 'mood'

    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name,start_date,end_date, style='ggplot')
    """


    """
    tbl_name = 'weight'
    date_name = 'Date'
    start_date = '2017-04-01'
    end_date = '2017-04-30'
    y_axis = 'Weight'

    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)
    """

    """
    tbl_name = daily_config['sleep']['tbl_name']
    date_name = daily_config['sleep']['date_name']
    start_date = '2017-04-01'
    end_date = '2017-04-30'
    y_axis = daily_config['sleep']['y_axis']

    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)
    """


    """
    date_name = 'Date'
    start_date = '2017-02-21'
    end_date = '2017-02-28'

    tbl_name = 'mood'
    y_axis = 'mood'

    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)
    """

"""
if __name__ == '__main__':
    print(find_dates(2017, 3, 1))
"""