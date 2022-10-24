from configparser import ConfigParser 
import mariadb, logging
import sys, os

def caseBtn(form):
    resp = ""

    for k in form:
        if k == 'start':
            resp = "start"
            break
        elif k == 'done':
            resp = "done"
            break
            
    return resp

def connectDB():
    try:
        db = ConfigParser()
        db.read(os.environ['DB_CONFIG_CONNECTION'])

    except Exception as e:
        logging.critical("Wrong DB configuration was found missing or bad syntexed")
        sys.exit(str(e))
        
    try:
        conn = mariadb.connect(
            user=db['mariadb']['USER'],
            password=db['mariadb']['PASSWORD'],
            host=db['mariadb']['HOST'],
            port=int(db['mariadb']['PORT']),
            database=db['mariadb']['DATABASE']
            )
        
        conn.autocommit = True
        
    except mariadb.Error as e:
        logging.critical(str(e))
        sys.exit(str(e))

    return conn

def randomQuery(query):
    conn = connectDB()
    
    try:
        cur = conn.cursor(dictionary=True)

        data = cur.execute(query)
        data = cur.fetchall()

        assert data != None, "Error retriving data"

        cur.close()
        
    except mariadb.Error as e:
        logging.critical(str(e))
        sys.exit(str(e))

    return data

def insertUpdate(query):
    conn = connectDB()

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query)

    except mariadb.Error as e:
        logging.critical(str(e))
        sys.exit(str(e))

    cur.close()

def nameFromid(id):
    data = randomQuery("SELECT name FROM users WHERE id = '" + str(id) + "'")[0]
    return data['name']

def idFromname(name):
    data = randomQuery("SELECT id FROM users WHERE name = '" + name + "'")[0]
    return data['id']

def usernameFromid(id):
    data = randomQuery("SELECT username FROM users WHERE id = '" + str(id) + "'")[0]
    return data['username']

def checkGuardia(id):
    return randomQuery("SELECT id FROM active WHERE iduser = '" + str(id) + "' and isActive = TRUE")

def whenStarted(id):
    data = randomQuery("SELECT start_date FROM active WHERE id = '" + str(id) + "'")
    return data[0]['start_date'].strftime("%d/%m/%Y, %H:%M:%S")

def startGuardia(uid):
    return insertUpdate("INSERT INTO sreaio.active (iduser) VALUES (" + str(uid) + ")")

def stopGuardia(uid,gid):
    return insertUpdate("UPDATE sreaio.active SET stop_date=NOW(), isActive = FALSE WHERE id=" + str(gid))