import datetime


def get_date_str(date=None):
    if not date:
        date = datetime.datetime.today()
        return date.strftime("%d.%m.%Y")
    








if __name__ == "__main__":
    ...
    get_date_str()




