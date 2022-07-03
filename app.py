from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

from pkg_resources import resource_stream


app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_BD'] = 'netflax_22068'
mysql.init_app(app)


@app.route('/')
def index():
    sql = "SELECT * FROM netflax_22068.peliculas;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    pelis = cursor.fetchall()
    # print(pelis)
    return render_template('peliculas/index.html', pelis=pelis)


@app.route('/create')
def create():
    return render_template('peliculas/create.html')


@app.route('/store', methods=['POST'])
def store():
    _nombre = request.form['txtNombre']
    _desc = request.form['txtDesc']
    _foto = request.files['txtImagen']
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        nuevo_nombre_foto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevo_nombre_foto)
        
    datos = (_nombre, _desc, nuevo_nombre_foto)
    sql = "INSERT INTO netflax_22068.peliculas(`nombre`, `descripcion`, `imagen`) VALUES (%s,%s,%s)"
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
    cursor.execute("DELETE FROM netflax_22068.peliculas WHERE id=%s", (id))
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


# http://127.0.0.1:5000
if __name__ == '__main__':
    app.run(debug=True)
