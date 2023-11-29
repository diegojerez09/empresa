from flask import Flask, render_template,request,redirect,flash, session,url_for,make_response
from flaskext.mysql import MySQL
from datetime import datetime
import bcrypt
from flask_login import login_required, LoginManager
from flask import jsonify
import json
from functools import wraps 
from flask_login import LoginManager, login_required , UserMixin,login_user,logout_user
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField
#from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.secret_key="DiegoJerez"

# Configurar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Especifica la vista de login

# CONEXION A LA BASE DE DATOS ----------------------------
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'lifa_empresa'

mysql.init_app(app)

#---------------------------------------------------------------------
#
# INICIAR SESSION (USUARIO)
#
#---------------------------------------------------------------------


class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    # Esta función debe devolver un objeto de usuario o None si no se encuentra
    # el usuario con el ID proporcionado.
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario WHERE UsuarioId = %s', (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user = User()
        user.id = user_data[0]
        user.rol = user_data[3]
        #print(user.rol)
        return user
    else:
        return None

 

@app.route('/')
def home():
    return render_template('login/index.html')

@app.route('/admin')
def admin():
    return render_template('login/admin.html')

# FUNCION DE LOGIN
@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE correo = %s', (_correo,))
        account = cursor.fetchone()

        if account and bcrypt.checkpw(_password.encode('utf-8'), account[2].encode('utf-8')):
            user = User()
            user.id = account[0]
            login_user(user)  # Registra al usuario como autenticado
            return render_template('header.html')
        else:
            return render_template('login/index.html', mensaje="Usuario o Contraseña incorrecto")
            
        
    return render_template('login/index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
        

@app.route('/insertarusuario')
@login_required
def insertarusuario():

    return render_template('usuario/insertarusuario.html')


@app.route('/storeusuario', methods=["GET" , "POST"])
@login_required
def storageusuario():

    _correo = request.form['txtCorreo']
    _password = request.form['txtPassword']
    

    if _correo=='' or _password=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertarusuario')
    
    _password_bytes = _password.encode('utf-8')
    
    sal = bcrypt.gensalt()
    encript = bcrypt.hashpw(_password_bytes,sal)
    


    sql = "INSERT INTO `usuario` (`correo`, `password`) VALUES ( %s, %s);"

    datos=(_correo,encript)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #flash('Herramienta Agregada') 
    return render_template('header.html', mensaje="Usuario Agregado")


#---------------------------------------------------------------------
#
# CARGA DE HERRAMIENTAS (ABM DE HERRAMIETNAS)
#
#---------------------------------------------------------------------


@app.route('/herramienta')
@login_required
def indexherramienta():
    
    sql = "SELECT herramienta.HerramientaId, herramienta.Nombre, categoria.Nombre, herramienta.Cantidad, herramienta.Estado FROM `herramienta` INNER JOIN `categoria` ON herramienta.CategoriaId = categoria.CategoriaId;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    herramientas=cursor.fetchall()
    conn.commit()

    return render_template('herramienta/indexherramienta.html',herramienta=herramientas)




@app.route('/eliminarherramienta/<int:id>')
def eliminarherramienta(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM herramienta WHERE HerramientaId=%s",(id))
    conn.commit()
    flash('Herramienta Eliminada')
    return redirect('/herramienta')

@app.route('/editarherramienta/<int:id>')
def editarherramienta(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM herramienta WHERE HerramientaId=%s",(id))
    herramientas=cursor.fetchall()
    conn.commit()
    return render_template('herramienta/editarherramienta.html',herramienta=herramientas)
    

@app.route('/actualizarherramienta', methods=['POST'])
def actualizarherramienta():
    _nombre=request.form['txtNombre']
    _categoria=request.form['txtCategoria']
    _cantidad=request.form['txtCantidad']
    _estado=request.form['txtEstado']
    id=request.form['txtId']

    sql = "UPDATE herramienta SET Nombre =%s, CategoriaId=%s, Cantidad=%s, Estado=%s WHERE HerramientaId=%s ;"

    datos=(_nombre,_categoria,_cantidad,_estado,id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/herramienta')
    

@app.route('/insertarherramienta')
def insertarherramienta():

    return render_template('herramienta/insertarherramienta.html')


@app.route('/storeherramienta', methods=['POST'])
def storageherramienta():

    _nombre=request.form['txtNombre']
    opciones_seleccionadas = request.form.getlist('opciones')
    _cantidad=request.form['txtCantidad']
    opciones_seleccionadas1= request.form.getlist('Estado')

    if _nombre=='' or _cantidad=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertarherramienta')
    
    for opcion in opciones_seleccionadas:
        opcion_int = int(opcion)

    for Estado in opciones_seleccionadas1:
        opcion1 = Estado

    sql = "INSERT INTO `herramienta` (`HerramientaId`, `Nombre`, `Categoriaid`, `Cantidad`, `Estado`) VALUES (NULL, %s, %s, %s, %s);"

    datos=(_nombre,opcion_int,_cantidad,opcion1)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    cursor.execute("SELECT MAX(HerramientaId) AS ultimo_id FROM herramienta" )
    datosid = cursor.fetchone()
    ultimoid = datosid[0]

    sql1="INSERT INTO deposito_herramienta ( Cantidad, HerramientaId ,DepositoId) VALUES (%s,%s,%s);"
    datos1=(_cantidad,ultimoid,6)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql1,datos1)
    conn.commit()


    flash('Herramienta Agregada') 
    return redirect('/herramienta')



#--------------------------------------------------------------------------------------
#
# MUESTRA LA CANTIDAD DE HERRAMIENTAS EN UN DEPOSITO DE UNA HERRAMIENTA DETERMINADA
#
#-----------------------------------------------------------------------------------------

@app.route('/obtener_detalles_herramienta/<int:herramienta_id>')
@login_required
def obtener_detalles_herramienta(herramienta_id):
    # Utiliza el ID de la herramienta para ejecutar la nueva consulta SQL
    sql = "SELECT deposito.Nombre, herramienta.Nombre, deposito_herramienta.Cantidad " \
          "FROM deposito " \
          "INNER JOIN deposito_herramienta ON deposito.DepositoId = deposito_herramienta.DepositoId " \
          "INNER JOIN herramienta ON deposito_herramienta.HerramientaId = herramienta.HerramientaId " \
          "WHERE herramienta.HerramientaId = %s " \
          "GROUP BY deposito.Nombre;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (herramienta_id,))
    detalles_herramienta = cursor.fetchall()
    conn.close()

    # Formatear los detalles como un objeto JSON y devolverlos como respuesta
    detalles_json = [
    {
            'NombreHerramienta': detalle[1],
            'NombreDeposito': detalle[0],
            'CantidadDeposito': detalle[2]
        } for detalle in detalles_herramienta
    ]

    print(detalles_herramienta)
    print(detalles_json)
    return jsonify(detalles_json)


#--------------------------------------------------------------------------------------
#
# MUESTRA LA CANTIDAD DE MATERIALES EN UN DEPOSITO DE UN MATERIAL DETERMINADA
#
#-----------------------------------------------------------------------------------------

@app.route('/obtener_detalles_material/<int:material_id>')
@login_required
def obtener_detalles_material(material_id):
    # Utiliza el ID de la herramienta para ejecutar la nueva consulta SQL
    sql = "SELECT deposito.Nombre, material.Nombre, deposito_material.Cantidad " \
          "FROM deposito " \
          "INNER JOIN deposito_material ON deposito.DepositoId = deposito_material.DepositoId " \
          "INNER JOIN material ON deposito_material.MaterialId = material.MaterialId " \
          "WHERE material.MaterialId = %s " \
          "GROUP BY deposito.Nombre;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (material_id,))
    detalles_material = cursor.fetchall()
    conn.close()

    # Formatear los detalles como un objeto JSON y devolverlos como respuesta
    detalles_json = [
    {
            'NombreMaterial': detalle[1],
            'NombreDeposito': detalle[0],
            'CantidadDeposito': detalle[2]
        } for detalle in detalles_material
    ]

    print(detalles_material)
    print(detalles_json)
    return jsonify(detalles_json)




#---------------------------------------------------------------------
#
# CARGA DE MATERIALES (ABM DE MATERIALES)
#
#---------------------------------------------------------------------

@app.route('/material')
@login_required
def material():
    sql = "SELECT * FROM  `material`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    materiales=cursor.fetchall()
    conn.commit()
    return render_template('material/indexmaterial.html',material=materiales)


@app.route('/eliminarmaterial/<int:id>')
def eliminarmaterial(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM material WHERE MaterialId=%s",(id))
    conn.commit()
    return redirect('/material')


@app.route('/editarmaterial/<int:id>')
def editarmaterial(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM material WHERE MaterialId=%s",(id))
    materiales=cursor.fetchall()
    conn.commit()
    return render_template('material/editarmaterial.html',material=materiales)
    

@app.route('/actualizarmaterial', methods=['POST'])
def actualizarmaterial():
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _cantidad=request.form['txtCantidad']
    opciones_seleccionadas1 = request.form.getlist('txtMedida')
    id=request.form['txtId']

    sql = "UPDATE material SET Nombre=%s, Descripcion=%s, Cantidad=%s, Medida=%s WHERE MaterialId=%s ;"

    datos=(_nombre,_descripcion,_cantidad,opciones_seleccionadas1,id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/material')
    

@app.route('/insertarmaterial')
def method_name1():

    return render_template('material/insertarmaterial.html')


@app.route('/storematerial', methods=['POST'])
def storagematerial():
    
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _cantidad=request.form['txtCantidad']
    opciones_seleccionadas1 = request.form.getlist('txtMedida')
    

    if _nombre=='' or _descripcion=='' or _cantidad=='' or opciones_seleccionadas1=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertarmaterial')

    sql = "INSERT INTO `material` (`MaterialId`, `Nombre`, `Descripcion`, `Cantidad`, `Medida`) VALUES (NULL, %s, %s, %s, %s);"

    datos=(_nombre,_descripcion,_cantidad,opciones_seleccionadas1)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    cursor.execute("SELECT MAX(MaterialId) AS ultimo_id FROM material" )
    datosid = cursor.fetchone()
    ultimoid = datosid[0]

    sql1="INSERT INTO deposito_material ( Cantidad, MaterialId ,DepositoId) VALUES (%s,%s,%s);"
    datos1=(_cantidad,ultimoid,6)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql1,datos1)
    conn.commit()


    #flash('Material Agregada') 
    return redirect('/material')


#---------------------------------------------------------------------
#
# CARGA DE DEPOSITOS (ABM DE DEPOSITOS)
#
#---------------------------------------------------------------------

@app.route('/deposito')
@login_required
def deposito():
    sql = "SELECT * FROM  `deposito`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    depositos=cursor.fetchall()
    conn.commit()
    return render_template('deposito/indexdeposito.html',deposito=depositos)

@app.route('/eliminardeposito/<int:id>')
def eliminardeposito(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM deposito WHERE DepositoId=%s",(id))
    conn.commit()
    return redirect('/deposito')

@app.route('/editardeposito/<int:id>')
def editardeposito(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deposito WHERE DepositoId=%s",(id))
    depositos=cursor.fetchall()
    conn.commit()
    return render_template('deposito/editardeposito.html',deposito=depositos)


@app.route('/actualizardeposito', methods=['POST'])
def actualizardeposito():
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _fechainicio=request.form['txtFechaInicio']
    _fechafin=request.form['txtFechaFin']
    #_estado=request.form['txtEstado']
    opciones_seleccionadas1= request.form.getlist('Estado')
    
    id=request.form['txtId']

    

    for Estado in opciones_seleccionadas1:
            opcion1 = Estado

    print(opcion1)
    sql = "UPDATE deposito SET Nombre =%s, Descripcion=%s, FechaInicio=%s, FechaFin=%s, Estado=%s WHERE DepositoId=%s ;"

    datos=(_nombre,_descripcion,_fechainicio,_fechafin,opcion1, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/deposito')

@app.route('/insertardeposito')
def method_name2():

    return render_template('deposito/insertardeposito.html')


@app.route('/storedeposito', methods=['POST'])
def storagedeposito():

    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _fechainicio=request.form['txtFechaInicio']
    _fechafin=request.form['txtFechaFin']
    opciones_seleccionadas1= request.form.getlist('Estado')
    
    if _nombre=='' or _descripcion=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertardeposito')

    for Estado in opciones_seleccionadas1:
            opcion1 = Estado

    sql = "INSERT INTO `deposito` (`DepositoId`, `Nombre`, `Descripcion`, `FechaInicio`, `FechaFin`, `Estado`) VALUES (NULL, %s, %s, %s, %s, %s);"

    datos=(_nombre,_descripcion,_fechainicio,_fechafin,opcion1)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #flash('Deposito agregado') 
    return redirect('/deposito')

#---------------------------------------------------------------------
#
# CARGA DE PROVEEDOR (ABM DE PROVEEDORES)
#
#---------------------------------------------------------------------

@app.route('/proveedor')
@login_required
def proveedor():
    sql = "SELECT * FROM  `proveedor`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    proveedores=cursor.fetchall()
    conn.commit()
    return render_template('proveedor/indexproveedor.html',proveedor=proveedores)

@app.route('/eliminarproveedor/<int:id>')
def eliminarproveedor(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedor WHERE ProveedorId=%s",(id))
    conn.commit()
    return redirect('/proveedor')

@app.route('/editarproveedor/<int:id>')
def editarproveedor(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM proveedor WHERE ProveedorId=%s",(id))
    proveedores=cursor.fetchall()
    conn.commit()
    return render_template('proveedor/editarproveedor.html',proveedor=proveedores)


@app.route('/actualizarproveedor', methods=['POST'])
def actualizarproveedor():
    _nombre=request.form['txtNombre']
    _cuit=request.form['txtCuit']
    _direccion=request.form['txtDireccion']
    _telefono=request.form['txtTelefono']
    _email=request.form['txtEmail']
    _contacto=request.form['txtContacto']
    _telefonocontacto=request.form['txtTelefonoContacto']
    _estado=request.form['txtEstado']
    id=request.form['txtId']

    sql = "UPDATE proveedor SET NombreProveedor=%s, Cuit=%s, Direccion=%s, Telefono=%s, Email=%s, Contacto=%s, TelefonoContacto=%s, Estado=%s WHERE ProveedorId=%s ;"

    datos=(_nombre,_cuit,_direccion,_telefono,_email,_contacto,_telefonocontacto,_estado, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/proveedor')

@app.route('/insertarproveedor')
def method_name3():

    return render_template('proveedor/insertarproveedor.html')


@app.route('/storeproveedor', methods=['POST'])
def storageproveedor():

    _nombre=request.form['txtNombre']
    _cuit=request.form['txtCuit']
    _direccion=request.form['txtDireccion']
    _telefono=request.form['txtTelefono']
    _email=request.form['txtEmail']
    _contacto=request.form['txtContacto']
    _telefonocontacto=request.form['txtTelefonoContacto']
    opciones_seleccionadas1= request.form.getlist('txtEstado')
    
    if _nombre=='' or _cuit=='' or _direccion=='' or _telefono=='' or _email=='' or _contacto=='' or _telefonocontacto=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertarproveedor')

    for Estado in opciones_seleccionadas1:
            opcion1 = Estado

    

    sql = "INSERT INTO `proveedor` (`ProveedorId`, `NombreProveedor`, `Cuit`, `Direccion`, `Telefono`, `Email`, `Contacto`, `TelefonoContacto`, `Estado`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);"

    datos=(_nombre,_cuit,_direccion,_telefono,_email,_contacto,_telefonocontacto,opcion1)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    flash('Proveedor agregado')
    return redirect('/proveedor' )


#---------------------------------------------------------------------
#
# CARGA DE VEHICULO (ABM DE VEHICULOS)
#
#---------------------------------------------------------------------

@app.route('/vehiculo')
@login_required
def vehiculo():
    sql = "SELECT * FROM  `vehiculo`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    vehiculos=cursor.fetchall()
    conn.commit()
    return render_template('vehiculo/indexvehiculo.html',vehiculo=vehiculos)

@app.route('/eliminarvehiculo/<int:id>')
def eliminarvehiculo(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehiculo WHERE VehiculoId=%s",(id))
    conn.commit()
    return redirect('/vehiculo')

@app.route('/editarvehiculo/<int:id>')
def editarvehiculo(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehiculo WHERE VehiculoId=%s",(id))
    vehiculos=cursor.fetchall()
    conn.commit()
    return render_template('vehiculo/editarvehiculo.html',vehiculo=vehiculos)


@app.route('/actualizarvehiculo', methods=['POST'])
def actualizarvehiculo():
    _patente=request.form['txtPatente']
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _año=request.form['txtAño']
    id=request.form['txtId']

    sql = "UPDATE vehiculo SET Patente =%s, Marca=%s, Modelo=%s, Año=%s WHERE VehiculoId=%s ;"

    datos=(_patente,_marca,_modelo,_año, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/vehiculo')

@app.route('/insertarvehiculo')
def method_name4():

    return render_template('vehiculo/insertarvehiculo.html')


@app.route('/storevehiculo', methods=['POST'])
def storagevehiculo():

    _patente=request.form['txtPatente']
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _año=request.form['txtAño']
    
    if _patente=='' or _marca=='' or _modelo=='' or _año=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertarvehiculo')

    sql = "INSERT INTO `vehiculo` (`VehiculoId`, `Patente`, `Marca`, `Modelo`, `Año`) VALUES (NULL, %s, %s, %s, %s);"

    datos=(_patente,_marca, _modelo,_año)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #flash('Vehiculo Agregado') 
    return redirect('/vehiculo')

#---------------------------------------------------------------------
#
# CARGA DE EMPLEADOS (ABM DE EMPLEADOS)
#
#---------------------------------------------------------------------


@app.route('/empleado')
@login_required
def empleado():
    sql = "SELECT * FROM  `empleado`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleado/indexempleado.html',empleado=empleados)

@app.route('/eliminarempleado/<int:id>')
def eliminarempleado(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado WHERE EmpleadoId=%s",(id))
    conn.commit()
    return redirect('/empleado')

@app.route('/editarempleado/<int:id>')
def editarempleado(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleado WHERE EmpleadoId=%s",(id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleado/editarempleado.html',empleado=empleados)
    

@app.route('/actualizarempleado', methods=['POST'])
def actualizarempleado():
    _nombre=request.form['txtNombre']
    _fechanacimiento=request.form['txtFechaNacimiento']
    _direccion=request.form['txtDireccion']
    _telefono=request.form['txtTelefono']
    _email=request.form['txtEmail']
    id=request.form['txtId']

    sql = "UPDATE empleado SET Nombre=%s, FechaNacimiento=%s, Direccion=%s, Telefono=%s, Email=%s WHERE EmpleadoId=%s ;"

    datos=(_nombre,_fechanacimiento,_direccion,_telefono,_email,id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/empleado')

@app.route('/insertarempleado')
def method_name5():

    return render_template('empleado/insertarempleado.html')


@app.route('/storeempleado', methods=['POST'])
def storageempleado():

    _nombre=request.form['txtNombre']
    _fechanacimiento=request.form['txtFechaNacimiento']
    _direccion=request.form['txtDireccion']
    _telefono=request.form['txtTelefono']
    _email=request.form['txtEmail']
    
    if _nombre=='' or _fechanacimiento=='' or _direccion=='' or _telefono=='' or _email=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertarempleado')

    sql = "INSERT INTO `empleado` (`EmpleadoId`, `Nombre`, `FechaNacimiento`, `Direccion`, `Telefono`, `Email`) VALUES (NULL, %s, %s, %s, %s, %s);"

    datos=(_nombre,_fechanacimiento, _direccion,_telefono,_email)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #flash('Empleado Agregado') 
    return redirect('/empleado')


#---------------------------------------------------------------------
#
# CARGA DE DEPOSITO_HERRAMIENTA (ABM DE DEPOSITO_HERRAMIENTA)
#
#---------------------------------------------------------------------


@app.route('/deposito_herramienta')
def deposito_herramienta():
    sql = "SELECT deposito_herramientaId, deposito_herramienta.Cantidad, herramienta.Nombre, deposito.Nombre FROM `deposito_herramienta` INNER JOIN `herramienta` ON deposito_herramienta.HerramientaId = herramienta.HerramientaId INNER JOIN `deposito` ON deposito_herramienta.DepositoId = deposito.DepositoId;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    depositos_herramientas=cursor.fetchall()
    conn.commit()
    return render_template('deposito_herramienta/indexdeposito_herramienta.html',deposito_herramienta=depositos_herramientas)


@app.route('/editardeposito_herramienta/<int:id>')
def editardeposito_herramienta(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deposito_herramienta WHERE Deposito_HerramientaId=%s",(id))
    depositos_herramientas=cursor.fetchall()
    conn.commit()
    return render_template('deposito_herramienta/editardeposito_herramienta.html',deposito_herramienta=depositos_herramientas)
    

@app.route('/actualizardeposito_herramienta', methods=['POST'])
def actualizardeposito_herramienta():
    _cantidad=request.form['txtCantidad']
    _herramientaid=request.form['txtHerramientaid']
    _depositoid=request.form['txtDepositoid']
    id=request.form['txtId']

    sql = "UPDATE deposito_herramienta SET Cantidad=%s, HerramientaId=%s, DepositoId=%s WHERE Deposito_HerramientaId=%s ;"

    datos=(_cantidad,_herramientaid,_depositoid,id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/deposito_herramienta')


@app.route('/storedeposito_herramienta', methods=['POST'])
def storagedeposito_herramienta():

    _cantidad=request.form['txtCantidad']
    _herramientaid=request.form['txtHerramientaid']
    _depositoid=request.form['txtDepositoid']
    
    
    if _cantidad=='' or _herramientaid=='' or _depositoid=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertardeposito_herramienta')

    sql = "INSERT INTO `deposito_herramienta` (`Deposito_HerramientaId`, `Cantidad`, `HerramientaId`, `DepositoId`) VALUES (NULL, %s, %s, %s);"

    datos=(_cantidad,_herramientaid,_depositoid)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #flash('Deposito_Herramienta Agregado') 
    return redirect('/deposito_herramienta')


#---------------------------------------------------------------------
#
# CARGA DE DEPOSITO_MATERIAL (ABM DE DEPOSITO_MATERIAL)
#
#---------------------------------------------------------------------


@app.route('/deposito_material')
def deposito_material():
    sql = "SELECT deposito_materialId, deposito_material.Cantidad, material.Nombre, deposito.Nombre FROM `deposito_material` INNER JOIN `material` ON deposito_material.MaterialId = material.MaterialId INNER JOIN `deposito` ON deposito_material.DepositoId = deposito.DepositoId;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    depositos_materiales=cursor.fetchall()
    conn.commit()
    return render_template('deposito_material/indexdeposito_material.html',deposito_material=depositos_materiales)


@app.route('/editardeposito_material/<int:id>')
def editardeposito_material(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deposito_material WHERE Deposito_MaterialId=%s",(id))
    depositos_materiales=cursor.fetchall()
    conn.commit()
    return render_template('deposito_material/editardeposito_material.html',deposito_material=depositos_materiales)
    

@app.route('/actualizardeposito_material', methods=['POST'])
def actualizardeposito_material():
    _cantidad=request.form['txtCantidad']
    _materialid=request.form['txtMaterialid']
    _depositoid=request.form['txtDepositoid']
    id=request.form['txtId']

    sql = "UPDATE deposito_material SET Cantidad=%s, MaterialId=%s, DepositoId=%s WHERE Deposito_MaterialId=%s ;"

    datos=(_cantidad,_materialid,_depositoid,id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/deposito_material')


@app.route('/storedeposito_material', methods=['POST'])
def storagedeposito_material():

    _cantidad=request.form['txtCantidad']
    _materialid=request.form['txtMaterialid']
    _depositoid=request.form['txtDepositoid']
    
    
    if _cantidad=='' or _materialid=='' or _depositoid=='':
        flash('Todos los campos deben estar completos')
        return redirect ('insertardeposito_material')

    sql = "INSERT INTO `deposito_material` (`Deposito_MaterialId`, `Cantidad`, `MaterialId`, `DepositoId`) VALUES (NULL, %s, %s, %s);"

    datos=(_cantidad,_materialid,_depositoid)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    #flash('Deposito_Material Agregado') 
    return redirect('/deposito_material')


#---------------------------------------------------------------------
#
# CARGA DE MOVIMIENTOS Y MOVIMIENTO DETALLES
#
#---------------------------------------------------------------------

@app.route('/movimientos')
@login_required
def movimientos():
    sql1 = "SELECT proveedor.NombreProveedor, proveedor.ProveedorId FROM proveedor INNER JOIN movimientos ON movimientos.Origen = proveedor.ProveedorId GROUP by proveedor.NombreProveedor;"
    sql = "SELECT * FROM `movimientos`;"
    sql2 = "SELECT Nombre, DepositoId FROM deposito INNER JOIN movimientos ON movimientos.Origen = deposito.DepositoId GROUP BY Nombre;  "
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    movimientos = cursor.fetchall()
    cursor.execute(sql1)
    nombreproveedores = cursor.fetchall()
    cursor.execute(sql2)
    nombredepositos = cursor.fetchall()

    # Crear un diccionario para mapear ID de depósito a nombres
    depositos_dict = {id: nombre for nombre, id in nombredepositos}

    # Iterar sobre los movimientos y reemplazar los ID con nombres
    movimientos_con_nombres = []
    for movimiento in movimientos:
        tipo = "ENTRADA" if movimiento[1] == "1" else "SALIDA"
        origen_nombre = depositos_dict.get(movimiento[2], movimiento[2])
        destino_nombre = depositos_dict.get(movimiento[3], movimiento[3])
        movimientos_con_nombres.append((movimiento[0], tipo, origen_nombre, destino_nombre, movimiento[4],movimiento[5]))


    
    # Crear un diccionario con los datos de ID y nombre del proveedor
    proveedor_dic = {id: nombre for nombre, id in nombreproveedores}

    # Crear una lista de tuplas con ID y nombre del proveedor
    nombre_proveedorees = [(id, nombre) for nombre, id in nombreproveedores]

    # Imprimir la lista de tuplas
    print(nombre_proveedorees)
   
    id_proveedores=list(proveedor_dic.keys())
    print(id_proveedores)



    conn.commit()
    #print(movimientos_con_nombres)
    #print(nombreproveedores)
    return render_template('movimientos/indexmovimientos.html', movimientos=movimientos_con_nombres, nombre_proveedores=proveedor_dic, id_proveedores=list(proveedor_dic.keys()), nombres_depositos=depositos_dict.values(), id_depositos=depositos_dict.keys())


@app.route('/movimientos_detalle')
def movimientos_detalle():
    sql = "SELECT * FROM  `deposito`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    depositos=cursor.fetchall()
    cursor.execute("SELECT * FROM proveedor")
    proveedor=cursor.fetchall()
    return render_template('movimientos/movimientos_detalle.html',depositos=depositos,proveedor = proveedor)

@app.route('/buscar_material', methods=['GET'])
def buscar_material():
    term = request.args.get('term')  # Término de búsqueda ingresado por el usuario
    sql = "SELECT MaterialId,nombre FROM material WHERE nombre LIKE %s;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (f"%{term}%",))
    material = cursor.fetchall()
    material_dict = [{'id': material[0], 'nombre': material[1]} for material in material]
    #material_list = [row[0] for row in material]  # Extraer solo los nombres de los materiales
    return jsonify(material_dict)

@app.route('/buscar_herramienta', methods=['GET'])
def buscar_herramienta():
    term = request.args.get('term')  # Término de búsqueda ingresado por el usuario
    sql = "SELECT HerramientaId,nombre FROM herramienta WHERE nombre LIKE %s;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (f"%{term}%",))
    herramienta = cursor.fetchall()

        #herramienta_list = [row[1] for row in herramienta]  # Extraer solo los nombres de las herramientas

    # Crear una lista de diccionarios con el ID y el nombre de la herramienta
   
    herramientas_dict = [{'id': herramienta[0], 'nombre': herramienta[1]} for herramienta in herramienta]
    return jsonify(herramientas_dict)
    



@app.route('/store_movimientos', methods=['POST'])
def storage_movimientos():

    #_tipo=request.form['txtTipo']
    #_origen=request.form['txtOrigen']

    if 'txtRemito' in request.form:
        _numeroremito = request.form['txtRemito']
    else:
        _numeroremito = None

    #_numeroremito = request.form['txtRemito']
    #if request.form['txtRemito'] :
    #    _numeroremito = request.form['txtRemito']
    #else:
    #    _numeroremito = None

    _fecha = request.form['txtFecha']
    opciones_tipo=request.form.getlist('Tipo')
    opciones_origen= request.form.getlist('Origen')
    opciones_destino= request.form.getlist('Destino')
    opciones_proveedor = request.form.getlist('Proveedor')
    tabla_data_json = request.form.get('tablaData') #OBTIENE TODOS LOS CAMPOS DE LA TABLA

    
    # Inicializa opcionD con un valor predeterminado (puede ser None)

    opcionD = None
    opcionP = None
    
    for Tipo in opciones_tipo:
        opcionT = Tipo

    for Origen in opciones_origen:
        opcionO = Origen
    
    for Destino in opciones_destino:
        opcionD = Destino

    for Proveedor in opciones_proveedor:
        opcionP = Proveedor
        
    

    if tabla_data_json=='' or opciones_tipo=='' or opciones_destino=='' or opciones_origen=='' or _numeroremito=='':
        flash('Todos los campos deben estar completos')
        return redirect ('movimientos_detalle')

    tabla_data = json.loads(tabla_data_json) #LOS PASA A FORMATO JSON
    
    #print(opcionT,opcionO,opcionD,_fecha,_numeroremito,opcionP)


    #agrego los datos en la tabla movimientos
    if opcionT == "1":
        Destino = 6
        sql = "INSERT INTO movimientos( Tipo , Origen , Destino, Fecha, NumeroRemito) VALUES ( %s, %s,%s,%s,%s);"
        datos=(opcionT,opcionP,Destino,_fecha,_numeroremito,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,datos)
        conn.commit()

        # Obtén los datos JSON de tablaData
    
        for row_data in tabla_data:
            nombre = row_data['nombre']  # Cambia 'herramientaMaterial' a 'nombre'
            cantidad = row_data['cantidad']
            tipo = row_data['tipo']
            id = row_data['id']
        
            #print(tipo)
            # Realiza la lógica de inserción en la base de datos según tus necesidades

            #print(id,cantidad)
        
            cantidad_deposito = cantidad
            cantidad_deposito_material = cantidad
            comprobar_cantidad = cantidad
    
            if tipo == 1:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT HerramientaId, Cantidad FROM herramienta WHERE HerramientaId = %s", (id))
                exite_herramienta = cursor.fetchone()
                if exite_herramienta:
                    cantidad= int(cantidad) + exite_herramienta[1]
                    cursor.execute("UPDATE herramienta SET Cantidad = %s WHERE HerramientaId = %s", (cantidad, id))
                    conn.commit()
                    cursor.execute("SELECT HerramientaId, Cantidad FROM deposito_herramienta WHERE HerramientaId = %s", (id))
                    exite_herramienta_depostio = cursor.fetchone()
                    

                if exite_herramienta_depostio:
                    cantidad_deposito= int(cantidad_deposito) + exite_herramienta_depostio[1]
                    
                    cursor.execute("UPDATE deposito_herramienta SET Cantidad = %s WHERE HerramientaId = %s", (cantidad_deposito, id))
                    conn.commit()
                else:
                    sql1 = "INSERT INTO deposito_herramienta(HerramientaId , Cantidad , DepositoId, fecha) VALUES (%s,%s,%s,%s);"
                    datos1 =(id,cantidad,opcionD,_fecha)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql1,datos1)
                    conn.commit()
            

            elif tipo == 2:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT MaterialId, Cantidad FROM material WHERE MaterialId = %s", (id))
                exite_material = cursor.fetchone()
                print(exite_material[1])
                if exite_material:
                
                    cantidad_deposito_material= int(cantidad_deposito_material) + exite_material[1]
                
                    cursor.execute("UPDATE material SET Cantidad = %s WHERE MaterialId = %s", (cantidad_deposito_material, id))
                    conn.commit()

                    cursor.execute("SELECT MaterialId, Cantidad FROM deposito_material WHERE MaterialId = %s", (id))
                    exite_material_depostio = cursor.fetchone()
                    cantidad_deposito_material = cantidad
                    print(exite_material_depostio)
                if exite_material_depostio:
                    print(cantidad_deposito_material)
                    cantidad_deposito_material= int(cantidad_deposito_material) + exite_material_depostio[1]
                    
                    cursor.execute("UPDATE deposito_material SET Cantidad = %s WHERE MaterialId = %s", (cantidad_deposito_material, id))
                    conn.commit()

                else:
                    opcionD = 6
                    sql1 = "INSERT INTO deposito_material(MaterialId , Cantidad , DepositoId, fecha) VALUES (%s,%s,%s,%s);"
                    datos1 =(id,cantidad,opcionD,_fecha)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sql1,datos1)
                    conn.commit()
    
    else:
        conn = mysql.connect()
        cursor = conn.cursor()
            #BUSCO EL IDMOVIMIENTO,IDMATERIAL,IDHERRAMIENTA Y LAS CANTIDADES
        cursor.execute("SELECT MAX(NumeroRemito) AS ultimo_remito FROM movimientos WHERE Tipo = 2" )
        datosremito = cursor.fetchone()
        ultimo_remito = int(datosremito[0]) + 1
        print(ultimo_remito)
        sql = "INSERT INTO movimientos( Tipo,Origen, Destino,Fecha,NumeroRemito) VALUES ( %s, %s,%s,%s,%s);"
        datos=(opcionT,opcionO,opcionD,_fecha,ultimo_remito)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,datos)
        conn.commit()

        for row_data in tabla_data:
            nombre = row_data['nombre']  # Cambia 'herramientaMaterial' a 'nombre'
            cantidad = row_data['cantidad']
            tipo = row_data['tipo']
            id = row_data['id']

            cantidad_deposito_herramienta = cantidad
            cantidad_deposito_material = cantidad
    
            if tipo == 1:
                conn = mysql.connect()
                cursor = conn.cursor()
                #BUSCO LA HERRAMIENTA EN LA OPCIONES DESTINO
                cursor.execute("SELECT HerramientaId, Cantidad FROM deposito_herramienta WHERE HerramientaId = %s AND DepositoId = %s", (id,opcionD))
                exite_herramienta_destino = cursor.fetchone()

                #BUSCO LA HERRAMIENTA EN LA OPCION ORGIEN
                cursor.execute("SELECT HerramientaId, Cantidad FROM deposito_herramienta WHERE HerramientaId = %s AND DepositoId = %s", (id,opcionO))
                exite_herramienta_origen = cursor.fetchone()
                if exite_herramienta_origen[1] > int(cantidad_deposito_herramienta):
                                
                    if exite_herramienta_destino:

                        cantidad= int(cantidad) + exite_herramienta_destino[1]
                        #print(cantidad)
                        cursor.execute("UPDATE deposito_herramienta SET Cantidad = %s WHERE HerramientaId = %s AND DepositoId =%s", (cantidad, id ,opcionD))
                        conn.commit()
                        cantidad_resta= exite_herramienta_origen[1] - int(cantidad_deposito_herramienta)
                        #print(cantidad_resta)
                        cursor.execute("UPDATE deposito_herramienta SET Cantidad = %s WHERE HerramientaId = %s AND DepositoId =%s", (cantidad_resta, id ,opcionO))
                        conn.commit()
                    else:
                        sql1 = "INSERT INTO deposito_herramienta(HerramientaId , Cantidad , DepositoId, fecha) VALUES (%s,%s,%s,%s);"
                        datos1 =(id,cantidad,opcionD,_fecha)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql1,datos1)
                        conn.commit()
                        cantidad_resta_noE= exite_herramienta_origen[1] - int(cantidad)
                        #print(cantidad_resta_noE)
                        cursor.execute("UPDATE deposito_herramienta SET Cantidad = %s WHERE HerramientaId = %s AND DepositoId =%s", (cantidad_resta_noE, id ,opcionO))
                        conn.commit()
                else : 
                    flash('No tiene suficiente cantidad de '+ nombre ) 
                    #return render_template('movimientos/movimientos_detalle.html')
                    return redirect('/movimientos_detalle')
                           

            elif tipo == 2:
                conn = mysql.connect()
                cursor = conn.cursor()
                #BUSCO EL MATERIAL EN LA OPCIONES DESTINO
                cursor.execute("SELECT MaterialId, Cantidad FROM deposito_material WHERE MaterialId = %s AND DepositoId = %s", (id,opcionD))
                exite_material_destino = cursor.fetchone()
                #BUSCO EL MATERIAL EN LA OPCION ORGIEN
                cursor.execute("SELECT MaterialId, Cantidad FROM deposito_material WHERE MaterialId = %s AND DepositoId = %s", (id,opcionO))
                exite_material_origen = cursor.fetchone()
                if exite_material_origen[1] > int(cantidad):

                    if exite_material_destino:
                        cantidad= int(cantidad) + exite_material_destino[1]
                        #print(cantidad)
                        cursor.execute("UPDATE deposito_material SET Cantidad = %s WHERE MaterialId = %s AND DepositoId =%s", (cantidad, id ,opcionD))
                        conn.commit()
                        cantidad_resta= exite_material_origen[1] - int(cantidad_deposito_material)
                        #print(cantidad_resta)
                        cursor.execute("UPDATE deposito_material SET Cantidad = %s WHERE MaterialId = %s AND DepositoId =%s", (cantidad_resta, id ,opcionO))
                        conn.commit()
                    else:
                        sql1 = "INSERT INTO deposito_material(MaterialId , Cantidad , DepositoId, fecha) VALUES (%s,%s,%s,%s);"
                        datos1 =(id,cantidad,opcionD,_fecha)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sql1,datos1)
                        conn.commit()
                        cantidad_resta_noE= exite_material_origen[1] - int(cantidad)
                        #print(cantidad_resta_noE)
                        cursor.execute("UPDATE deposito_material SET Cantidad = %s WHERE MaterialId = %s AND DepositoId =%s", (cantidad_resta_noE, id ,opcionO))
                        conn.commit()
                else:
                    flash('No tiene suficiente cantidad de '+ nombre ) 
                    #return render_template('movimientos/movimientos_detalle.html')
                    return redirect('/movimientos_detalle')


    for row_data in tabla_data:
            nombre = row_data['nombre']  # Cambia 'herramientaMaterial' a 'nombre'
            cantidad_movimientos_detalle = row_data['cantidad']
            tipo = row_data['tipo']
            id = row_data['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            #BUSCO EL IDMOVIMIENTO,IDMATERIAL,IDHERRAMIENTA Y LAS CANTIDADES
            cursor.execute("SELECT MAX(MovimientoId) AS ultimo_id FROM movimientos" )
            datosid = cursor.fetchone()
            ultimoid = datosid[0]
            #cursor.execute("SELECT MovimientoId, Fecha , NumeroRemito ,ProveedorId FROM movimientos")
            #datos_movimientos = cursor.fetchone()
            #movimientoid = datos_movimientos[0]
            #fecha = datos_movimientos[1]
            #numeroremito = datos_movimientos[2]
            #proveedorid = datos_movimientos[3]
            if tipo == 1:
                sql1 = "INSERT INTO movimientos_detalle(MovimientosId , HerramientaId , CantidadHerramienta) VALUES (%s,%s,%s);"
                datos1 =(ultimoid,id,cantidad)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql1,datos1)
                conn.commit()
            elif tipo == 2:
                sql1 = "INSERT INTO movimientos_detalle(MovimientosId, MaterialId, CantidadMaterial) VALUES (%s,%s,%s);"
                datos1 =(ultimoid,id,cantidad)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql1,datos1)
                conn.commit()
                

    flash('Movimiento Agregado') 
    return redirect('/movimientos')

@app.route('/eliminarmovimiento/<int:id>')
def eliminarmovimiento(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from movimientos WHERE MovimientoId=%s",(id))
    conn.commit()
    flash('MOVIMIENTO ELIMINADO')
    return redirect('/movimientos')


@app.route('/MostarMovimiento/<int:id>')
def MostarMovimiento(id):
    print(id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("Select NumeroRemito,ProveedorId,HerramientaId,CantidadHerramienta,MaterialId,CantidadMaterial from movimientos INNER JOIN movimientos_detalle ON movimientos.MovimientoId = movimientos_detalle.MovimientosId WHERE MovimientoId = %s",(id))
    movimientosdetalles = cursor.fetchall()
    
    print(movimientosdetalles)
    #conn.commit()
    #flash('MOVIMIENTO ELIMINADO')
    
    # Determinar si se deben mostrar los encabezados
    #show_headers = any(any(dato is not None for dato in detalle) for detalle in movimientosdetalles)

    # Filtrar los detalles para excluir aquellos con todos los datos como None
    #filtered_movimientosdetalles = [detalle for detalle in movimientosdetalles if any(dato is not None for dato in detalle)]

    # Devolver los detalles como JSON
    #return render_template('movimientos/detalles.html', movimientosdetalles=filtered_movimientosdetalles, show_headers=show_headers)
    # Devolver los detalles como JSON
    return render_template('movimientos/detalles.html', movimientosdetalles = movimientosdetalles)





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
