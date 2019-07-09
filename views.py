import os
import json
from functools import wraps
from DatabaseAccess import *
from Employee import *
from EmployeeService import *
from Specialty import *
from SpecialtyService import *
from Address import *
from AddressService import *
from Medic import *
from MedicService import *
from Doctor import *
from DoctorService import *
from Authentification import *
import requests
from flask_simpleldap import LDAP
import os

# imported packages
from flask import jsonify, Response, Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, send_file


app = Flask(__name__)
app.config.from_object(__name__)
app.config['LDAP_HOST'] = '192.168.236.154'
app.config['LDAP_BASE_DN'] = 'CN=Users,dc=bts-gam,dc=local'
app.config['LDAP_USERNAME'] = 'CN=Administrateur,CN=Users,DC=bts-gam,DC=local'
app.config['LDAP_PASSWORD'] = 'Admin6259'
app.config['UPLOAD_FOLDER'] = 'uploads'

app.config.update(dict(SECRET_KEY='development'))

ldap = LDAP(app)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'UserLogged' in session:
            if 'token' in session:
                return f(*args, **kwargs)
        return redirect(url_for('auth'))
    return decorated


@app.route('/authentification')
def auth():
    session.pop('UserLogged', None)
    session.pop('token', None)
    return render_template('auth.html')


@app.route('/valider-auth', methods=['POST'])
def auth_validation():
    auth = Authentification()
    if request.form['email'] and request.form['password']:
        password, email = request.form['password'], request.form['email']
        user_info = ldap.bind_user(email,password)
        if user_info is not None:
            session['UserLogged'] = email
            group = ldap.get_user_groups(user=session['UserLogged'])
            print(group)
            for i in range(len(group)):
                if(group[i].decode('UTF-8') == 'AdminGSB'):
                    token = auth.postAuth(email, password)
                    try:
                        token = token['token']
                        session['token'] = token
                        res = make_response(redirect(url_for('show_main_page')))
                        res.set_cookie('notice', value=session['UserLogged'], max_age=None)
                        return res
                    except:
                        flash("Acces refuse.")
                elif(group == 'Visiteurs'):
                    print('oui')
                    return redirect(url_for('down'))
        else:
            flash("Acces refuse.")
    else:
        flash("Authentification incomplete.")
    return redirect(url_for('auth'))


@app.route('/')
@requires_auth
def show_main_page():
    return render_template('main_page.html')

@app.route('/down.jpg')
def down():
    uploads = os.path.join('/home/ryltar/workspace/sf_GSB-ADMIN', app.config['UPLOAD_FOLDER'])
    return send_file('/home/ryltar/workspace/sf_GSB-ADMIN/uploads/oui.jpg',
                     mimetype='image/jpeg',
                     attachment_filename='oui.jpg',
                     as_attachment=True)



@app.route('/ajouter-medic')
@requires_auth
def show_add_medic():
    return render_template('add_medic.html')


@app.route('/ajouter-doc')
@requires_auth
def show_add_doctor():
    return render_template('add_doctor.html')

@app.route('/ajouter-specialty')
@requires_auth
def show_add_specialty():
    return render_template('add_specialty.html')


@app.route('/ajouter-emp')
@requires_auth
def show_add_employee():
    return render_template('add_employee.html')

@app.route('/ajouter-address')
@requires_auth
def show_add_address():
    return render_template('add_address.html')


@app.route('/consulter-chat')
def show_see_chat():
    return render_template('see_chat.html')


@app.route('/grille-employe')
@requires_auth
def show_grid_employee():
    return render_template('grid_employee.html')

@app.route('/grille-address')
@requires_auth
def show_grid_address():
    return render_template('grid_address.html')

@app.route('/grille-specialty')
@requires_auth
def show_grid_specialty():
    return render_template('grid_specialty.html')

@app.route('/grille-docteur')
@requires_auth
def show_grid_doctor():
    employeeService = EmployeeService()
    employees = employeeService.getAllEmployee(session['token'])
    employees = employees['data']
    addressService = AddressService()
    addresses = addressService.getAllAddress(session['token'])
    addresses = addresses['data']
    specialtyService = SpecialtyService()
    specialties = specialtyService.getAllSpecialty(session['token'])
    specialties = specialties['data']
    return render_template('grid_doctor.html', employees = employees, addresses = addresses, specialties = specialties)

@app.route('/grille-medic')
@requires_auth
def show_grid_medic():
    token = session['token']
    return render_template('grid_medic.html')

@app.route('/loadEmployee', methods=['POST'])
@requires_auth
def loadEmployee():
    employeeService = EmployeeService()
    token = session['token']
    users = employeeService.getAllEmployee(token)
    users = users['data']
    length = len(users)
    temp_users = []
    total = 0
    temp = []
    if(request.form['rowCount'] != "-1"):
        for i in range((int(request.form['current'])-1)*int(request.form['rowCount']),int(request.form['current'])*int(request.form['rowCount'])):
            try:
                temp_key = []
                user = Employee(users[i])
                total = total + 1
                temp_users.append(user.dictionarize())
            except IndexError:
                continue;
    else:
         for i in range(length):      
                temp_key = []
                user = Employee(users[i])
                total = total + 1
                temp_users.append(user.dictionarize())

    if(request.form["searchPhrase"] != ''):
        for j in range(len(temp_users)):
            flag = False
            for cle,valeur in temp_users[j].items():   
                if str(request.form["searchPhrase"]) not in str(valeur):
                    flag = True
                else:
                    flag = False
                    temp.append(temp_users[j])
                    break;
        temp_users = temp
    data = {"current":request.form['current'], "rowCount":request.form['rowCount'] ,"rows":temp_users, "total":length }
    users=json.dumps(data)
    res = Response(response=users, status=200, mimetype="application/json")
    return res

@app.route('/loadSpecialty', methods=['POST'])
@requires_auth
def loadSpecialty():
    specialtyService = SpecialtyService()
    token = session['token']
    specialties = specialtyService.getAllSpecialty(token)
    specialties = specialties['data']
    length = len(specialties)
    temp_specialties = []
    total = 0
    temp = []
    if(request.form['rowCount'] != "-1"):
        for i in range((int(request.form['current'])-1)*int(request.form['rowCount']),int(request.form['current'])*int(request.form['rowCount'])):
            try:
                temp_key = []
                specialty = Specialty(specialties[i])
                total = total + 1
                temp_specialties.append(specialty.dictionarize())
            except IndexError:
                continue
    else:
        for i in range(length):
            temp_key = []
            specialty = Specialty(specialties[i])
            total = total + 1
            temp_specialties.append(specialty.dictionarize())
                    
    if(request.form["searchPhrase"] != ''):
        for j in range(len(temp_specialties)):
            flag = False
            for cle,valeur in temp_specialties[j].items():   
                if str(request.form["searchPhrase"]) not in str(valeur):
                    flag = True
                else:
                    flag = False
                    temp.append(temp_specialties[j])
                    break;
        temp_specialties = temp
    data = {"current":request.form['current'], "rowCount":request.form['rowCount'] ,"rows":temp_specialties, "total":length }
    specialties=json.dumps(data)
    res = Response(response=specialties, status=200, mimetype="application/json")
    return res

@app.route('/loadAddress', methods=['POST'])
@requires_auth
def loadAddress():
    addressService = AddressService()
    token = session['token']
    addresses = addressService.getAllAddress(token)
    addresses = addresses['data']
    length = len(addresses)
    temp_addresses = []
    temp=[]
    total = 0
    if(request.form['rowCount'] != "-1"):
        for i in range((int(request.form['current'])-1)*int(request.form['rowCount']),int(request.form['current'])*int(request.form['rowCount'])):
            try:
                temp_key = []
                address = Address(addresses[i])
                total = total + 1
                temp_addresses.append(address.dictionarize())
            except IndexError:
                continue
    else:   
        for i in range(length):
            temp_key = []
            address = Address(addresses[i])
            total = total + 1
            temp_addresses.append(address.dictionarize())
    if(request.form["searchPhrase"] != ''):
        for j in range(len(temp_addresses)):
            flag = False
            for cle,valeur in temp_addresses[j].items(): 
                if str(request.form["searchPhrase"]) not in str(valeur):
                    flag = True
                else:
                    flag = False
                    temp.append(temp_addresses[j])
                    break;
        temp_addresses = temp
    data = {"current":request.form['current'], "rowCount":request.form['rowCount'] ,"rows":temp_addresses, "total":length }
    addresses=json.dumps(data)
    res = Response(response=addresses, status=200, mimetype="application/json")
    return res

@app.route('/loadMedic', methods=['POST'])
@requires_auth
def loadMedic():
    medicService = MedicService()
    token = session['token']
    medics = medicService.getAllMedic(token)
    medics = medics['data']
    length = len(medics)
    temp_medics = []
    temp = []
    total = 0
    if(request.form["rowCount"] != "-1"):  
        for i in range((int(request.form['current'])-1)*int(request.form['rowCount']),int(request.form['current'])*int(request.form['rowCount'])):
            try:
                temp_key = []
                medic = Medic(medics[i])
                total = total + 1
                temp_medics.append(medic.dictionarize())
            except IndexError:
                continue
    else:
        for i in range(length):
            temp_key = []
            medic = Medic(medics[i])
            total = total + 1
            temp_medics.append(medic.dictionarize())
    if(request.form["searchPhrase"] != ''):
        for j in range(len(temp_medics)):
            flag = False
            for cle,valeur in temp_medics[j].items():   
                if str(request.form["searchPhrase"]) not in str(valeur):
                    flag = True
                else:
                    flag = False
                    temp.append(temp_medics[j])
                    break;
        temp_medics = temp
    data = {"current":request.form['current'], "rowCount":request.form['rowCount'] ,"rows":temp_medics, "total":length }
    medics=json.dumps(data)
    res = Response(response=medics, status=200, mimetype="application/json")
    return res

@app.route('/loadDoctor', methods=['POST'])
@requires_auth
def loadDoctor():
    doctorService = DoctorService()
    token = session['token']
    doctors = doctorService.getAllDoctor(token)
    doctors = doctors['data']
    length = len(doctors)
    temp_doctors = []
    temp = []
    total = 0
    if(request.form["rowCount"] != "-1"):  
        for i in range((int(request.form['current'])-1)*int(request.form['rowCount']),int(request.form['current'])*int(request.form['rowCount'])):
            try:
                temp_key = []
                doctor = Doctor(doctors[i])
                total = total + 1
                temp_doctors.append(doctor.dictionarize())
            except IndexError:
                continue
    else:
        for i in range(length):
            temp_key = []
            doctor = Doctors(doctors[i])
            total = total + 1
            temp_doctors.append(doctor.dictionarize())
    if(request.form["searchPhrase"] != ''):
        for j in range(len(temp_doctors)):
            flag = False
            for cle,valeur in temp_doctors[j].items():   
                if str(request.form["searchPhrase"]) not in str(valeur):
                    flag = True
                else:
                    flag = False
                    temp.append(temp_doctors[j])
                    break;
        temp_doctors = temp
    data = {"current":request.form['current'], "rowCount":request.form['rowCount'] ,"rows":temp_doctors, "total":length }
    doctors = json.dumps(data)
    res = Response(response=doctors, status=200, mimetype="application/json")
    return res

@app.route('/editEmployee', methods=['PUT'])
@requires_auth
def editEmployee():
    employee = Employee()
    token = session['token']
    employeeService = EmployeeService()
    employee.id = request.form['edit_id']
    employee.admin = request.form['edit_admin']
    employee.lastname = request.form['edit_lastname']
    employee.firstname = request.form['edit_firstname']
    employee.pseudo = request.form['edit_pseudo']
    employee.email = request.form['edit_email']
    employee.phone = request.form['edit_phone']
    employeeService.putOneEmployee(token, employee)
    res = Response(response=employee.dictionarize(), status=200, mimetype="application/json")
    return res


@app.route('/deleteEmployee', methods=['DELETE'])
@requires_auth
def deleteEmployee():
    employeeService = EmployeeService()
    token = session['token']
    res = request.form['id']
    employeeService.deleteOneEmployee(token, res)
    return res

@app.route('/editMedic', methods=['PUT'])
@requires_auth
def editMedic():
    medic = Medic()
    token = session['token']
    medicService = MedicService()
    medic.id = request.form['edit_id']
    medic.name = request.form['edit_libmedic']
    medic.description = request.form['edit_descmedic']
    medicService.putOneMedic(token, medic)
    res = Response(response=medic.dictionarize(), status=200, mimetype="application/json")
    return res


@app.route('/deleteMedic', methods=['DELETE'])
@requires_auth
def deleteMedic():
    token = session['token']
    medicService = MedicService()
    res = request.form['id']
    medicService.deleteOneMedic(token, res)
    return res


@app.route('/editSpecialty', methods=['PUT'])
@requires_auth
def editSpecialty():
    specialty = Specialty()
    token = session['token']
    specialtyService = SpecialtyService()
    specialty.id = request.form['edit_id']
    specialty.label = request.form['edit_libspec']
    specialtyService.putOneSpecialty(token, specialty)
    res = Response(response=specialty.dictionarize(), status=200, mimetype="application/json")
    return res

@app.route('/deleteSpecialty', methods=['DELETE'])
@requires_auth
def deleteSpecialty():
    specialtyService = SpecialtyService()
    token = session['token']
    res = request.form['id']
    specialtyService.deleteOneSpecialty(token, res)
    return res

@app.route('/editAddress', methods=['PUT'])
@requires_auth
def editAddress():
    address = Address()
    token = session['token']
    addressService = AddressService()
    address.id = request.form['edit_idaddr']
    address.num = request.form['edit_num']
    address.street = request.form['edit_street']
    address.codepost = request.form['edit_codepost']
    address.city = request.form['edit_city']
    address.country = request.form['edit_country']
    address.indication = request.form['edit_indication']
    addressService.putOneAddress(token, address)
    res = Response(response=address.dictionarize(), status=200, mimetype="application/json")
    return res

@app.route('/deleteAddress', methods=['DELETE'])
@requires_auth
def deleteAddress():
    addressService = AddressService()
    token = session['token']
    res = request.form['id']
    addressService.deleteOneAddress(token, res)
    return res

@app.route('/editDoctor', methods=['PUT'])
@requires_auth
def editDoctor():
    doctor = Doctor()
    token = session['token']
    doctorService = DoctorService()
    doctor.id = request.form['edit_id']
    doctor.lastname = request.form['edit_lastname']
    doctor.firstname = request.form['edit_firstname']
    doctor.email = request.form['edit_email']
    doctor.num_tel = request.form['edit_num']
    doctor.employee = request.form['edit_employee']
    doctor.address = request.form['edit_address']
    doctor.specialty = request.form['edit_specialty']
    print(doctor.dictionarize())
    doctorService.putOneDoctor(token, doctor)
    res = Response(response=doctor.dictionarize(), status=200, mimetype="application/json")
    return res

@app.route('/deleteDoctor', methods=['DELETE'])
@requires_auth
def deleteDoctor():
    doctorService = DoctorService()
    token = session['token']
    res = request.form['id']
    doctorService.deleteOneDoctor(token, res)
    return res

@app.route('/creer-employe')
@requires_auth
def show_create_employee():
    return render_template('create_employee.html')

@app.route('/creer-specialty')
@requires_auth
def show_create_specialty():
    print('test')
    return render_template('create_specialty.html')

@app.route('/creer-docteur')
@requires_auth
def show_create_doctor():
    employeeService = EmployeeService()
    employees = employeeService.getAllEmployee(session['token'])
    employees = employees['data']
    addressService = AddressService()
    addresses = addressService.getAllAddress(session['token'])
    addresses = addresses['data']
    return render_template('create_doctor.html', employees = employees, addresses = addresses)

@app.route('/creer-medic')
@requires_auth
def show_create_medic():
    token = session['token']
    return render_template('create_medic.html')

@app.route('/creer-address')
@requires_auth
def show_create_address():
    return render_template('create_address.html')


@app.route('/envoyer-employe', methods=['POST'])
@requires_auth
def send_employee():
    employee = Employee()
    token = session['token']
    employeeService = EmployeeService()
    if((request.form['passwordemployee']) == (request.form['confirm-passwordemployee'])):
        employee.admin = request.form['add_admin']
        employee.lastname = request.form['nameemployee']
        employee.firstname = request.form['surnameemployee']
        employee.pseudo = request.form['pseudoemployee']
        employee.email = request.form['emailemployee']
        employee.phone = request.form['numemployee']
        employee.password = request.form['passwordemployee']
        employeeService.createOneEmployee(token, employee)
    else:
        flash('les deux mots de passe sont different !')

    return redirect(url_for('show_add_employee'))

@app.route('/envoyer-doctor', methods=['POST'])
@requires_auth
def send_doctor():
    doctor = Doctor()
    token = session['token']
    doctorService = DoctorService()
    doctor.num_tel = request.form['num']
    doctor.lastname = request.form['lastname']
    doctor.firstname = request.form['firstname']
    doctor.email = request.form['email']
    doctor.employee = request.form['employee']
    doctor.address = request.form['address']
    doctorService.createOneDoctor(token, doctor)
    return redirect(url_for('show_add_doctor'))

@app.route('/envoyer-specialty', methods=['POST'])
@requires_auth
def send_specialty():
    specialty = Specialty()
    token = session['token']
    specialtyService = SpecialtyService()
    specialty.label = request.form['lib']
    specialtyService.createOneSpecialty(token, specialty)
    return redirect(url_for('show_add_specialty'))

@app.route('/envoyer-address', methods=['POST'])
@requires_auth
def send_address():
    address = Address()
    token = session['token']
    addressService = AddressService()
    address.num = request.form['num']
    address.street = request.form['street']
    address.codepost = request.form['codepost']
    address.city = request.form['city']
    address.country = request.form['country']
    address.indication = request.form['indication']
    addressService.createOneAddress(token, address)
    return redirect(url_for('show_add_address'))

@app.route('/envoyer-medic', methods=['POST'])
@requires_auth
def send_medic():
    medic = Medic()
    token = session['token']
    medicService = MedicService()
    medic.name = request.form['libmedic']
    medic.description = request.form['descmedic']
    print(medic)
    medicService.createOneMedic(token, medic)
    return redirect(url_for('show_add_medic'))