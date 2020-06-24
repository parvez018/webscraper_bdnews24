import datetime

start_date = datetime.date(2020,1,1)
url = "https://bdnews24.com/archive/?date=2020-03-01"
base_url = "https://bdnews24.com/archive/?date="
print(start_date)

for d in range(1000):
    current_date = start_date + datetime.timedelta(days=d)
    if current_date>datetime.date.today():
        break
    complete_url = base_url+str(current_date)
    print(complete_url)