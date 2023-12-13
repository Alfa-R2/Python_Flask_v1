from flask import Flask, request, jsonify, render_template
from psycopg2 import connect, extras
from dotenv import load_dotenv
from os import environ
load_dotenv()
app=Flask(__name__)

HOST=environ.get("DB_HOST"); PORT=environ.get("DB_PORT")
DBNAME=environ.get("DB_NAME");USERNAME=environ.get("DB_USER")
PASSWORD=environ.get("DB_PASSWORD")

def get_cnx():
    cnx=connect(host=HOST, port=PORT, dbname=DBNAME, user=USERNAME, password=PASSWORD)
    return cnx

def get_cur(cnx):
    cur =cnx.cursor(cursor_factory=extras.RealDictCursor)
    return cur

def not_found():
    return jsonify({'mensaje':'Producto no encontrado'}),404

@app.get("/api/productos")
def get_productos():
    cnx=get_cnx()
    cur=get_cur(cnx)
    cur.execute("SELECT * FROM SELECT_PRODUCTOS()")
    result=cur.fetchall()
    cur.close();cnx.close()
    return jsonify(result)

@app.post("/api/productos")
def post_productos():
    data=request.get_json()
    cnx=get_cnx()
    cur= get_cur(cnx)
    cur.execute("SELECT INSERT_PRODUCTOS(%s,%s,%s)",
                (data["descripcion"] ,data["categoria"],data["precio"]))
    result= cur.fetchall()
    cnx.commit()
    cur.close();cnx.close()
    return jsonify(result)

@app.delete("/api/productos/<int:id>")
def delete_productos(id):
    cnx=get_cnx()
    cur=get_cur(cnx)
    cur.execute("select delete_productos(%s)",(id,))
    result=cur.fetchall()
    cnx.commit()
    cnx.close();cur.close()
    if result[0]["delete_productos"]==None:
        return not_found()
    return jsonify(result)

@app.put("/api/productos/<int:id>")
def put_productos(id):
    data=request.get_json()
    cnx=get_cnx()
    cur=get_cur(cnx)
    cur.execute("select update_productos(%s,%s,%s,%s)",
                (data["descripcion"],data["categoria"],
                 data["precio"], id))
    result=cur.fetchall()
    cnx.commit()
    cur.close();cnx.close()
    if result[0]["update_productos"]==None:
        return not_found()
    return jsonify(result)

@app.get("/api/productos/<int:id>")
def get_producto(id):
    cnx=get_cnx()
    cur=get_cur(cnx)
    cur.execute("select * from find_producto(%s)",(id,))
    result=cur.fetchone()
    cur.close();cnx.close()
    if result==None:
        return not_found()
    return jsonify(result)

@app.route("/")
def index():
    return render_template("index.html")