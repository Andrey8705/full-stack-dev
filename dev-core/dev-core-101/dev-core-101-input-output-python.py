import datetime

Name = input("Как тебя зовут? ")
Age = int(input("Год твоего рождения в формате(YYYY)? "))
Today = datetime.date.today()
Formateddate = int(Today.strftime("%Y"))
a = 100
Years100 =((Age + a) - Formateddate)
Year = Formateddate + Years100
print(Name, ", через ", Years100," года тебе будет 100 лет.Это будет ", Year," год.")
