"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for
from datetime import datetime
from datetime import date
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.73.36.248/project1
#
# For example, if you had username zy2431 and password 123123, then the following line would be:
#
#     DATABASEURI = "postgresql://zy2431:123123@34.73.36.248/project1"
#
DATABASEURI = "postgresql://ait2117:project1ait2117@34.73.36.248/project1" # Modify this with your own credentials you received from Joseph!

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#

#engine.execute("""DROP TABLE IF EXISTS doc_login""")

engine.execute("""CREATE TABLE IF NOT EXISTS doc_login (
        login_id INT
        );""")

engine.execute("""DROP TABLE IF EXISTS patient_login""")
engine.execute("""CREATE TABLE IF NOT EXISTS patient_login (
        name VARCHAR,
        dob DATE
        );""")

engine.execute("""CREATE TABLE IF NOT EXISTS pcp_full_info (
        patient_id VARCHAR, 
        patient_name VARCHAR,
        doc_id VARCHAR,
        doc_name VARCHAR,
        license_num VARCHAR,
        PRIMARY KEY (patient_id, doc_id, license_num)
        );""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  nIf you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

#@app.route('/')
#def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
  """
"""
  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
"""

patient_id_list = []
doc_id_list = []
patient_name = []
patient_dob = []
doctor_login_list = []
med_id_list = []

@app.route('/')
def home(): 

    # for debugging
#    print(request.args)
    return render_template("home.html")

"""Patient Portal"""
@app.route('/patient_portal')
def patient_portal(): 
    return render_template("patient_portal.html", title="Patient Portal")

@app.route('/patient_portal/returning_patient', methods=['GET', 'POST'])
def returning_patient(): 
    if request.method=='POST': 
        name = request.form.get('name')
        dob = request.form.get('dob')
        patient_name.append(name)
        patient_dob.append(dob)
        g.conn.execute('INSERT INTO patient_login VALUES (%s, %s)', (name, dob))
        return redirect(url_for('patient_portal_main', user=name, dob = dob))
    else:
      return render_template("patient_returning.html", title="Returning Patient")

@app.route('/patient_portal/<user>/<dob>', methods=['GET', 'POST'])
def patient_portal_main(user,dob):
#    cursor = g.conn.execute("SELECT patient.patient_id, patient.name, patient.dob, patient.insurance, patient.medical_history, patient.is_guardian, patient.diagnoses, doctor.doc_name, testing.test_id, testing.lab_reports, testing.shots_given FROM patient inner join views on patient.patient_id = views.patient_id inner join doctor on views.doc_id = doctor.doc_id inner join testing on doctor.doc_id = testing.doc_id WHERE patient.name = (%s) and patient.dob = (%s)", (user, dob)).fetchall()
    cursor = g.conn.execute("SELECT * FROM patient WHERE patient.name=(%s) and patient.dob=(%s)", (user, dob))

    return render_template("patient_main.html", title="Patient Data", data=cursor)


@app.route('/patient_portal/new_patient', methods=['GET', 'POST'])
def new_patient():
    patient_id = random.randrange(11,5000)
    while patient_id in patient_id_list: 
        patient_id = random.randrange(11,5000)
    patient_id_list.append(patient_id)

    if request.method == 'POST': 
        name = request.form.get('name')
        dob = request.form.get('dob')
#        patient_name.append(name)
#        patient_dob.append(dob)
#        patient_name[0]=name
#        patient_dob[0]=dob
        insurance = request.form.get('insurance')
        medical_history = request.form.get('medical_history')
        guardian = False
        diagnoses = ""
        cursor = g.conn.execute('INSERT INTO patient(patient_id, name, dob, insurance, medical_history, is_guardian, diagnoses) VALUES (%s, %s, %s, %s, %s, %s, %s)', patient_id, name, dob, insurance, medical_history, guardian, diagnoses)
        cursor.close()
        return redirect(url_for('patient_portal_main', user=name, dob=dob))
    else: 
        return render_template("patient_new.html", title="New Patient")

"""Scheduling Function"""
@app.route('/scheduling_add', methods=['GET', 'POST'])
def scheduling_add(): 
    if request.method=='GET':
        cursor = g.conn.execute('SELECT * FROM doctor')
        return render_template("scheduling_add.html", data=cursor)

    if request.method=='POST':
        patient_id = request.form.get('patient_id')
        doc_id = request.form.get('doc_id')
        license_num = request.form.get('license_num')
        date_appt = request.form.get('date_appt')
        start_time = request.form.get('start_time')
        room_num = request.form.get('room_num')
        cursor = g.conn.execute('INSERT INTO schedule VALUES (%s, %s, %s, %s, %s, %s)', (patient_id, doc_id, license_num, date_appt, start_time, room_num))
        cursor.close()
        return redirect(url_for('home'))
    else: 
        return render_template("scheduling_add.html", title="Scheduling an Appointment")

"""Clinic Portal"""
@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method=='POST': 
        login_id = request.form.get('login_id')
        doctor_login_list.append(login_id)
        cursor = g.conn.execute('INSERT INTO doc_login VALUES (%s)', login_id)
        cursor.close()
        return redirect(url_for('clinic_portal'))
    else:
      return render_template("staff_login.html")

@app.route('/clinic_portal')
def clinic_portal(): 
    return render_template("clinic_portal.html", title="Clinic Portal") 

@app.route('/clinic_portal/logins')
def clinic_logins(): 
    cursor = g.conn.execute("SELECT * FROM doc_login").fetchall()
    return render_template("clinic_logins.html", title="Clinic Portal Logins", data=cursor)


@app.route('/clinic_portal/patients')
def clinic_patients(): 
    cursor = g.conn.execute("SELECT * FROM patient").fetchall()
    return render_template("clinic_patients.html", title="Patient Files", data=cursor)

@app.route('/diagnosis_add', methods=['GET', 'POST'])
def diagnosis_add(): 
    if request.method=='POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        diagnoses = request.form.get('diagnoses')
        cursor = g.conn.execute('UPDATE patient SET diagnoses = (%s) WHERE name=(%s) and dob=(%s)', (diagnoses, name, dob))
#        cursor = g.conn.execute('INSERT INTO patient VALUES (%s) WHERE name=(%s) and dob=(%s)', diagnoses, name, dob) 
        cursor.close()
        return redirect(url_for('clinic_patients'))
    else: 
        return render_template("diagnosis_add.html", title="Adding a Doctor")



@app.route('/clinic_portal/doctors')
def clinic_doctors(): 
    cursor = g.conn.execute("SELECT * FROM doctor").fetchall()
    return render_template("clinic_doctors.html", title="Doctor Files", data=cursor)

@app.route('/doctor_add', methods=['GET', 'POST'])
def doctor_add(): 
    doctor_id = random.randrange(11,5000)
    while doctor_id in doc_id_list: 
        doctor_id = random.randrange(11,5000)
    doc_id_list.append(doctor_id)

    if request.method=='POST':
        doc_name = request.form.get('doc_name')
        license_num = request.form.get('license_num')
        job_title = request.form.get('job_title')
        date_hired = request.form.get('date_hired')
        degrees = request.form.get('degrees')
        expertise = request.form.get('expertise')
        cursor = g.conn.execute('INSERT INTO doctor VALUES (%s, %s, %s, %s, %s, %s, %s)', (doctor_id, license_num, job_title, date_hired, degrees, expertise, doc_name))
        cursor.close()
        return redirect(url_for('clinic_doctors'))
#        return redirect('/clinic_portal/doctors')
    else: 
        return render_template("doctor_add.html", title="Adding a Doctor")


@app.route('/clinic_portal/pcps')
def clinic_pcps(): 
    cursor = g.conn.execute("SELECT pcp.patient_id, patient.name, pcp.doc_id, doctor.doc_name, doctor.license_num FROM pcp, patient, doctor WHERE pcp.patient_id=patient.patient_id and pcp.doc_id=doctor.doc_id and pcp.license_num=doctor.license_num").fetchall()
#   cursor = g.conn.execute("SELECT * FROM pcp").fetchall()
    return render_template("clinic_pcps.html", title="PCP Files", data=cursor)

@app.route('/clinic_portal/schedule')
def clinic_schedule(): 
    cursor = g.conn.execute("SELECT * FROM schedule ORDER BY date_appt, start_time").fetchall()
    return render_template("clinic_schedule.html", title="Schedule", data=cursor)

@app.route('/clinic_portal/testing')
def clinic_testing(): 
    cursor = g.conn.execute("SELECT * FROM testing").fetchall()
    return render_template("clinic_testing.html", title="Testing", data=cursor)

@app.route('/clinic_portal/medications')
def clinic_medications(): 
    cursor = g.conn.execute("SELECT * FROM medication").fetchall()
    return render_template("clinic_medications.html", title="Medications", data=cursor)

@app.route('/medication_add', methods=['GET', 'POST'])
def medication_add(): 
    # random med_id generate
    medication_id = random.randrange(11,5000)
    while medication_id in med_id_list: 
        medication_id = random.randrange(11,5000)
    med_id_list.append(medication_id)

    if request.method=='POST':
        license_num = request.form.get('license_num')
        pharmacy_addr = request.form.get('pharmacy_addr')
        refills_num = request.form.get('refills_num')
        type_ = request.form.get('type')
        is_prescription = request.form.get('is_prescription')
        doc_id = request.form.get('doc_id')
        p_name = request.form.get('p_name')
        cursor = g.conn.execute('INSERT INTO medication VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (medication_id, license_num, pharmacy_addr, refills_num, type_, is_prescription, doc_id, p_name))
#        cursor = g.conn.execute('INSERT INTO patient VALUES (%s) WHERE name=(%s) and dob=(%s)', diagnoses, name, dob) 
        cursor.close()
        return redirect(url_for('clinic_medications'))
    else: 
        return render_template("medication_add.html", title="Adding a Medication")


@app.route('/clinic_portal/labs')
def clinic_labs(): 
    cursor = g.conn.execute("SELECT * FROM views").fetchall()
    return render_template("clinic_labs.html", title="Patient Labs", data=cursor)

@app.route('/clinic_portal/timeslots')
def clinic_timeslots(): 
    cursor = g.conn.execute("SELECT * FROM timeslot").fetchall()
    return render_template("clinic_timeslots.html", title="All Timeslots", data=cursor)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    #print("patient_id_list: " + str(patient_id_list))
    #print("patient_name: " + str(patient_name))
    #print("patient_dob: " + str(patient_dob))

  run()
