from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app=Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_BD'] = 'netflax_22068'
mysql.init_app(app)

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute(sql)
    conn.commit()
    
    return render_template('peliculas/index.html')

@app.route('/create')
def create():
    return render_template('peliculas/create.html')

@app.route('/store', methods = ['POST'])
def store():
    _nombre = request.form['txtNombre']
    _desc = request.form['txtDesc']
    _foto  = request.files['txtImagen']
    
    datos =(_nombre, _desc, _foto.filename)
    sql = "INSERT INTO netflax_22068.peliculas(`nombre`, `descripcion`, `imagen`) VALUES (%s,%s,%s);"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
        
    return render_template('peliculas/create.html')

# http://127.0.0.1:5000
if __name__ == '__main__':
    app.run(debug=True)



