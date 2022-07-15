import os
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory



app = Flask(__name__)
app.secret_key='Clave'


mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_BD'] = 'pasteleriabd'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

@app.route('/uploads/<nombreImg>')
def uploads (nombreImg):
    return send_from_directory(app.config['CARPETA'], nombreImg)


@app.route('/')
def index():
    sql = "SELECT * FROM pasteleriabd.producto;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    pelis = cursor.fetchall()
    print(pelis,"p/ver si hay conexion")
    return render_template('peliculas/index.html', pelis=pelis)


@app.route('/create')
def create():
    return render_template('peliculas/create.html')


@app.route('/store', methods=['POST'])
def store():
    _nombre = request.form['txtNombre']
    _desc = request.form['txtDesc']
    _foto = request.files['txtImagen']
    _precioCosto = request.files['txtPrecioCosto']
    _precioVenta = request.files['txtPrecioVenta']
    if _nombre =='' or _desc == '' or _foto == ''or _precioCosto == ''or _precioVenta == '':
        flash("Faltan datos obligatorios!!")
        return redirect(url_for('create'))
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        nuevo_nombre_foto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevo_nombre_foto)
        
    datos = (_nombre, _desc, nuevo_nombre_foto, _precioCosto, _precioVenta)
    sql = "INSERT INTO netflax_22068.peliculas(`nombre_producto`, `descripcion_producto`, `precio_costo`, `precio_venta`) VALUES (%s,%s,%s,%s,%s)"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    # return render_template('peliculas/index.html')
    return redirect('/')


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # eliminar la imagen de uploads 
    cursor.execute("SELECT imagen FROM netflax_22068.peliculas WHERE id= %s", id)
    img = cursor.fetchone()    
    os.remove(os.path.join(app.config['CARPETA'], img[0]))
    
    cursor.execute("DELETE FROM netflax_22068.peliculas WHERE id=%s", id)
    conn.commit()
    return redirect('/')




@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql= "SELECT * FROM netflax_22068.peliculas WHERE id=%s"
    cursor.execute(sql, (id))
    peli = cursor.fetchone()
    
    return render_template('peliculas/edit.html', peli=peli)


@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _desc = request.form['txtDesc']
    _foto = request.files['txtImagen']
    _id = request.form['txtID']
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename !='':
        nuevo_nombre_foto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevo_nombre_foto)    
            
    conn = mysql.connect()
    cursor = conn.cursor()   
    
    cursor.execute("SELECT imagen FROM netflax_22068.peliculas WHERE id= %s", _id)
    img = cursor.fetchone()    
    os.remove(os.path.join(app.config['CARPETA'], img[0]))
    
    sql = "UPDATE netflax_22068.peliculas SET `nombre`= %s,`descripcion`= %s,`imagen`= %s WHERE `id` = %s;"
    datos = (_nombre, _desc, nuevo_nombre_foto, _id)
    
    cursor.execute(sql, datos)
    conn.commit()
     
     
     # return render_template('peliculas/index.html')
    return redirect('/')
    
    
    

        
    
    
   










# http://127.0.0.1:5000
if __name__ == '__main__':
    app.run(debug=True)
