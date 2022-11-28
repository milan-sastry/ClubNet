from datetime import datetime
def get_alumni_year():
    alumniyear = -1
    if (datetime.now().month > 5):
        alumniyear = datetime.now().year
    else:
        alumniyear = datetime.now().year - 1
    return alumniyear

if __name__ == "__main__":

    print(get_alumni_year())
