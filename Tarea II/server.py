from flask import Flask, render_template, request, flash
import time
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'logincreate'

usuarios = []

db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()


@app.route('/')
def inicio():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    cursor.execute(f'SELECT contraseña FROM login WHERE usuario="{usuario}"')
    datos_contraseña = cursor.fetchall()

    contraseña_correcta = False
    alerta_correcta = 'False'
    for i in datos_contraseña:
        for contraseña_usuario in i:
            if contraseña_usuario == contraseña:
                contraseña_correcta = True
                alerta_correcta = 'True'
                if alerta_correcta == 'True':
                    cursor.execute(
                        f'SELECT usuario FROM login WHERE usuario="{usuario}"')
                    datos_usuario = cursor.fetchone()
                    user = ''
                    for convertir_datos in datos_usuario:
                        nick_user = user.join(convertir_datos)
                        flash(f'Bienvenido {nick_user}!!', 'success')

            elif contraseña not in contraseña_usuario:
                contraseña_correcta = True
                flash('la contraseña es incorrecta', 'danger')

        if contraseña_correcta == True:
            break
    if contraseña_correcta == False:
        if alerta_correcta == 'False':
            flash('el usuario ingresado no existe!', 'danger')

    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('registrarse.html')


@app.route('/registrarse', methods=['POST'])
def registrarse():
    usuario = request.form['usuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']

    insertar_datos = usuario, correo, contraseña

    correos_usuarios = cursor.execute('SELECT correo FROM login')
    correos_DB = correos_usuarios.fetchall()

    data_usuario = cursor.execute('SELECT usuario FROM login')
    database_usuario = data_usuario.fetchall()

    correo_correcto = True
    alerta_correcta = 'True'

    for x in correos_DB:
        for y in x:
            if y == correo:
                correo_correcto = False
                alerta_correcta = 'False'

                if alerta_correcta == 'False':
                    flash('Este correo ya ha sido utilizado', 'danger')

        if correo_correcto == False:
            break
    if correo_correcto == True:
        usuario_correcto = False
        for verificar_usuario in database_usuario:
            for confirmar_usuario in verificar_usuario:
                if confirmar_usuario == usuario:
                    usuario_correcto = True
                    flash('Este usuario ya ha sido utilizado!', 'danger')

            if usuario_correcto == True:
                break

        if usuario_correcto == False:
            cursor.execute(
                    'INSERT into login(usuario, correo, contraseña) VALUES(?, ?, ?)', insertar_datos)
            db.commit()
            flash('te haz registrado con exito!', 'success')
            time.sleep(1)
            return render_template('login.html')

    return render_template('registrarse.html')

@app.route('/login/confirmardatos')
def confirmar_datos():
    return render_template('password.html')

@app.route('/confirmardatos/cambiarcontraseña', methods=['POST'])
def cambiar_contraseña():
    usuario = request.form['usuario']
    correo = request.form['correo']
    
    
    correo_user = cursor.execute(f'SELECT correo FROM login WHERE usuario="{usuario}"')
    datos_correo = correo_user.fetchall()
    
    confirmarCorreo = False
    for buscar_correo in datos_correo:
        for limpiar_datos in buscar_correo:
            if limpiar_datos == correo:
                confirmarCorreo = True
                usuarios.append(usuario)
                flash('correo verificado correctamente', 'success')
                time.sleep(1)
                return render_template('cambiarcontraseña.html')
                
        if confirmarCorreo == True:
            break
    if confirmarCorreo == False:
        flash('El correo ingresado no es correcto', 'danger')
    
    return render_template('password.html')

@app.route('/cambiarcontraseña/guardarcambios', methods=['POST'])
def cambiarGuardarPass():
    contraseña = request.form['contraseña']
    confirmar_contraseña = request.form['confirmarcontraseña']
    user = ''
    user_date = user.join(usuarios)
    contraseña_user = cursor.execute(f'SELECT contraseña FROM login WHERE usuario="{user_date}"')
    datos_contraseña = contraseña_user.fetchall()
    
    contraseñaCorrecta = True
    
    if contraseña == confirmar_contraseña:
        for buscar_contraseña in datos_contraseña:
            for limpiar_contraseña in buscar_contraseña:
                if limpiar_contraseña == confirmar_contraseña:
                    contraseñaCorrecta = False
                    flash('ya utilizaste esta contraseña', 'danger')
                        
            if contraseñaCorrecta == False:
                break
        if contraseñaCorrecta == True:
            cursor.execute(f'UPDATE login SET contraseña="{confirmar_contraseña}" WHERE usuario="{user_date}"')
            db.commit()
            flash('contraseña cambiada exitosamente!', 'success')
            time.sleep(1)
            return render_template('login.html')      
    else:
        flash('las contraseñas ingresadas no son iguales', 'danger')
    return render_template('cambiarcontraseña.html')

if __name__ == '__main__':
    app.run(debug=True, port=400)
