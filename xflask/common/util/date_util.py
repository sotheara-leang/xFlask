from datetime import datetime

dd_MM_yyyy_hh_mm_ss = '%d-%m-%Y %H:%M:%S'

def to_date_str(date: datetime, df=dd_MM_yyyy_hh_mm_ss):
    return date.strftime(df)

def now():
    return datetime.now()
