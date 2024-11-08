from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('almacen.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=('GET', 'POST'))
def agregar_producto():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        # Validar que los campos no estén vacíos
        if descripcion and cantidad and precio:
            conn = get_db_connection()
            conn.execute('INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)',
                         (descripcion, cantidad, precio))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else:
            # Mensaje de error si faltan campos
            error = "Todos los campos son obligatorios."
            return render_template('agregar.html', error=error)

    return render_template('agregar.html')


@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar_producto(id):
    conn = get_db_connection()
    producto = conn.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        # Verifica si los datos existen antes de actualizar
        if descripcion and cantidad and precio:
            conn.execute('UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?',
                         (descripcion, cantidad, precio, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else:
            # Opcional: manejo de errores si los campos están vacíos
            error = "Todos los campos son obligatorios"
            return render_template('editar.html', producto=producto, error=error)

    conn.close()
    return render_template('editar.html', producto=producto)


@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM producto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
