import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

file="eschooldata.db"

db = sqlite3.connect(file) #open if file exists, otherwise create
cursor = db.cursor()       #facilitate db ops

#==========================================================
def SQLcommands(text):
    command = text
    cursor.execute(command)

SQLcommands("CREATE TABLE courses (code TEXT, mark INTEGER, id INTEGER)")
SQLcommands("CREATE TABLE peeps (name TEXT, age INTEGER, id INTEGER)")

with open("data/courses.csv", "rb") as csvfile:
    dictReader = csv.DictReader(csvfile)
    for row in dictReader:
        SQLcommands("INSERT INTO courses VALUES ('" + row["code"] + "', '" + row["mark"] + "', '" + row["id"] + "')")

with open("data/peeps.csv", "rb") as csvfile:
    dictReader = csv.DictReader(csvfile)
    for row in dictReader:
        SQLcommands("INSERT INTO peeps VALUES ('" + row["name"] + "', '" + row["age"] + "', '" + row["id"] + "')")
        
def look_grade(id):
    SQLcommands("SELECT mark FROM courses WHERE courses.id = " + str(id) + ";")
    return cursor.fetchall()

def compute_average(id):
    total = 0.0
    index = 0
    for row in look_grade(id):
        index += 1
        total += int(row[0])
    return total/index

def count_ids():
    SQLcommands("SELECT COUNT(id) FROM peeps;")
    return cursor.fetchall()[0][0]
    
def display_student():
    for id in range(1,count_ids()+1):
        SQLcommands("SELECT name, id FROM peeps;")
    for row in cursor.fetchall():
        print str(row[0]) + "," + str(row[1]) + "," + str(compute_average(row[1]))

def make_peeps_avg():
    SQLcommands("CREATE TABLE peeps_avg (id INTEGER, average NUMERIC)")
    SQLcommands("SELECT id FROM peeps;")
    for row in cursor.fetchall():
        SQLcommands("INSERT INTO peeps_avg VALUES (%s, %s);" % (row[0], compute_average(row[0])))
        
print compute_average(1)
print count_ids()
display_student()
make_peeps_avg()
#==========================================================
db.commit() #save changes
db.close()  #close database
