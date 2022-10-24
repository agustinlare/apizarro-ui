from flask import Flask, request, render_template, flash, redirect, url_for
# from flask_restplus import Api
from flask_wtf import FlaskForm
from wtforms import SelectField
from db import *
from api import *
import datetime
import json

app = Flask(__name__)

today = datetime.datetime.now()
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
msg = ''

# if os.getenv('FLASK_APP'):
#     @property
#     def specs_url(self):
#         return url_for(self.endpoint('specs'), _external=True, _scheme='https')    
#     Api.specs_url = specs_url

if not os.path.isfile("config.json"):
    raise Exception("Configuration file is missing")
else:
    with open("config.json") as f:
        config = json.load(f)
        basedomain = config['basedomain']

class Person:
    usuario = ""
    nombre = ""
    time = ""
    count = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    resp = ''
    action_info = ''
    cluster_info = ''
    sel_0 = ''
    sel_1 = ''
    sel_n = ''
    text_on = ''
    btn_on = ''
    projects = ''
    pods = ''

    if request.method == 'POST':
        cluster_info = getCluster(config,request.form['cluster_sel'])
        action_info = getActions(config,request.form['action_sel'])

        if 'sel_0' in request.form:
            projects = request.form['projects']

        if 'sel_1' in request.form:
            pods = request.form['pods']

        if 'btn_1' in request.form:
            print(pods)
        
        if len(action_info['requires']) == 0:

            if action_info['opt'] == 'textbox': #borrarIndices 
                text_on = True
                btn_on = True

            elif action_info['opt'] == 'list':#deleteProject
                sel_0 = getProjects(cluster_info['prefix']) 
                btn_on = True
            
            elif action_info['opt'] == '': # deleteTridentds, deleteFluntdds
                btn_on = True
            
        else:
            sel_n = len(action_info['requires'])
            for req in action_info['requires']:
                if req == 'project' and projects == '':
                    sel_0 = getProjects(cluster_info['prefix'])

                if req == 'podss' and projects != '':
                    sel_1 = getPods(cluster_info['prefix'], projects)

            if action_info['opt'] == 'textbox':
                text_on = True
            
            btn_on = True

        if btn_on in request.form:
            resp = doYouthing(request.form)
        
        return render_template('home.html', msgs=resp, config=config, c_sel=cluster_info['name'], a_sel=action_info['name'], 
        sel_0=sel_0, sel_1=sel_1, sel_n=sel_n, text_on=text_on, btn_on=btn_on)

    else:
        pass

    return render_template('home.html', msgs=resp, config=config, sel_0=sel_0, sel_1=sel_1, text_on=text_on, btn_on=btn_on)

@app.route('/reporte', methods=['GET', 'POST'])    
def reporte():
    this_month = today.strftime('%B')
    tm = today.strftime('%m')
   
    if request.method == 'POST':
        btn = caseBtn(request.form)
        tm = int(tm) - 1

        if 'last' in btn:
            first = today.replace(day=1)
            lastMonth = first - datetime.timedelta(days=1)
            tm = lastMonth.strftime("%m")
    
    allusers = randomQuery("SELECT id FROM users")

    final_report = []
    for u in allusers:
        count = 0
        time = datetime.timedelta()
        
        allrecords = randomQuery("SELECT * FROM active WHERE isActive = 0 and MONTH(start_date) =" + str(tm) + " and iduser = " + str(u['id']))
        
        if len(allrecords) > 0:
            for r in allrecords:
                count = count + 1

                timeRecorded = r["stop_date"] - r["start_date"]
                time = time + timeRecorded

        a = Person()
        a.usuario = usernameFromid(u["id"])
        a.count = count
        a.time = str(time)
        a.nombre = nameFromid(u["id"])

        final_report.append(a)

    return render_template('reporte.html', this_month=this_month, 
    final_report=final_report, config=config)

@app.route('/guardias', methods=['GET','POST'])
def guardia():
    lastselection = ""
    users = randomQuery("SELECT * FROM users")
    guardiaActiva = ""
    fecha = ""
    msg = ""

    if request.method == 'POST':
        lastselection = request.form['uselection']
        uid = idFromname(lastselection)
        btn = caseBtn(request.form)

        gid = checkGuardia(uid)

        if len(gid) > 0:
            guardiaActiva = "True"
            fecha = wheprojectstarted(gid[0]['id'])
        else:
            guardiaActiva = "False"

        if 'done' in btn:
            gid = checkGuardia(uid)
            resp = stopGuardia(uid,gid[0]['id'])
            
            if resp == None:
                guardiaActiva = "False"
                msg = "Guardia con fecha de inicio " + wheprojectstarted(gid[0]['id']) + " finalizada"
            else:
                logging.error("DB | Un expected error at stopGuardia. " + resp)

        elif 'start' in btn:
            guardiaActiva = "New"
            resp = startGuardia(uid)
            
            if resp == None:
                msg = "Nueva guardia registrada"
            else:
                logging.error("DB | Un expected error at startGuardia. " + resp)
             
    return render_template('guardia.html', users=users, guardiaActiva=guardiaActiva, 
    fecha=fecha, msg=msg, config=config, defaultselection=lastselection)

if __name__ == '__main__':
    if os.getenv('FLASK_APP'):
        app.run(host=os.environ['FLASK_RUN_HOST'], port=os.environ['FLASK_RUN_PORT'])
    else:
        app.run(debug=True)