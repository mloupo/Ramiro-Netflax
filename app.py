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
    sql = "INSERT INTO netflax_22068.peliculas(`nombre`, `descripcion`, `imagen`) VALUES ('El Padrino II','El Padrino II (descripcion)','');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    
    return render_template('peliculas/index.html')


if __name__ == '__main__':
    app.run(debug=True)



