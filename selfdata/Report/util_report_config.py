"""
y_lim_offset
0 = Checks only itself to see max/min y
1 = Checks both side of month (e.g if it's Febuary, it will check Jan, March also) to see max/min y
y_lim_offset_percentage = uses to decide max/min extra space to buffer on top.
"""


daily_config = {
    'weight':
        {
            'tbl_name': 'weight',
            'date_name': 'Date',
            'y_axis': 'Weight',
            'y_lim_offset': 0, # number of month to get data from
            'y_lim_offset_percentage': 0.01 # 0.10 = 10%
        },
    'weather_daily':
        {
            'tbl_name': 'weather_daily',
            'date_name': 'Date',
            'y_axis': 'Temp_mean',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'google_fit':
        {
            'tbl_name': 'google_fit',
            'date_name': 'Date',
            'y_axis': 'Step count',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'mood':
        {
            'tbl_name': 'mood',
            'date_name': 'Date',
            'y_axis': 'mood',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'pomo_excel_daily':
        {
            'tbl_name': 'pomo_excel_daily',
            'date_name': 'Date',
            'y_axis': 'pomo_total',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'pomo_kanban_daily':
        {
            'tbl_name': 'pomo_kanban_daily',
            'date_name': 'Date',
            'y_axis': 'pomo_total',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'pomodoro':
        {
            'tbl_name': 'pomodoro',
            'date_name': 'Date',
            'y_axis': 'pomodoro',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        },
    'sleep':
        {
            'tbl_name': 'sleep',
            'date_name': 'Date',
            'y_axis': 'total_hours',
            'y_lim_offset': 1,
            'y_lim_offset_percentage': 0.10
        }
}


tbl_name_web_temp = {
    'google_fit': 'steps',
    'mood': 'mood',
    'sleep': 'sleep',
    'weather_daily': 'weather',
    'weight': 'weight',
    'pomo_excel_daily': 'pomodoro'
    #'pomodoro': 'pomodoro'
}

tbl_name_web_temp_rev = {
    'steps': 'google_fit',
    'mood': 'mood',
    'sleep': 'sleep',
    'weather': 'weather_daily',
    'weight': 'weight',
    'pomodoro': 'pomo_excel_daily'
    #'pomodoro': 'pomodoro'

}