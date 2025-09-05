from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pyodbc
from datetime import datetime
import logging
import os

app = Flask(__name__)
app.secret_key = 'llave secreta'  # Cambiar por una clave más segura

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dossier_operations.log'),
        logging.StreamHandler()
    ]
)

# Configuración de base de datos (completar con datos)
DB_CONFIG = {
    'server': '192.168.1.210',
    'database': '',
    'username': 'USUARIO',
    'password': 'ONTRASEÑA',
    'driver': '{ODBC Driver 17 for SQL Server}'                                                                                      # o el driver que tengas disponible
}

def get_db_connection():
    """Crear conexión a la base de datos"""
    try:
        conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        logging.error(f"Error conectando a la base de datos: {str(e)}")
        return None

def search_dossier(dossier_id):
    """Buscar información del dossier antes de eliminarlo"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        query = """
        SELECT U.UserName,DA.DossierArchivoID,D.DossierID,D.FechaAlta,D.Nombre,COUNT(*) AS Cantidad,DE.descripcion AS Tipo
        FROM dbo.gnNoti_Dossier AS D
        INNER JOIN dbo.aspnet_Users AS U ON D.UserID=U.UserID
        INNER JOIN dbo.gnNoti_DossierArchivos AS DA ON D.DossierID = DA.DossierID
        INNER JOIN dbo.gnNoti_DossierNoticias AS DN ON D.DossierID = DN.DossierID
        INNER JOIN dbo.gnNoti_DossierEstados AS DE ON DE.DossierEstadoID = DA.DossierEstadoID
        WHERE DA.Termino=0 AND D.DossierID = ?
        GROUP BY U.UserName,DA.DossierArchivoID,D.DossierID,D.FechaAlta,D.Nombre,DE.Descripcion
        """
        cursor.execute(query, (dossier_id,))
        results = cursor.fetchall()
        
        # Convertir resultados a lista de diccionarios
        columns = [column[0] for column in cursor.description]
        dossier_data = []
        for row in results:
            dossier_data.append(dict(zip(columns, row)))
        
        conn.close()
        return dossier_data
    except Exception as e:
        logging.error(f"Error buscando dossier {dossier_id}: {str(e)}")
        conn.close()
        return None

def delete_dossier_archives(dossier_archivo_ids, user_name):
    """Eliminar archivos del dossier"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Construir la query de eliminación
        ids_str = ','.join([str(id) for id in dossier_archivo_ids])
        query = f"DELETE FROM dbo.gnNoti_DossierArchivos WHERE DossierArchivoID IN ({ids_str})"
        
        cursor.execute(query)
        conn.commit()
        
        # Log de la operación
        logging.info(f"Usuario: {user_name} eliminó DossierArchivoIDs: {ids_str}")
        
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error eliminando dossier: {str(e)}")
        conn.close()
        return False

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Buscar dossier por ID"""
    dossier_id = request.form.get('dossier_id')
    
    if not dossier_id:
        flash('Por favor ingresa un ID de dossier válido', 'error')
        return redirect(url_for('index'))
    
    try:
        dossier_id = int(dossier_id)
    except ValueError:
        flash('El ID del dossier debe ser un número', 'error')
        return redirect(url_for('index'))
    
    # Buscar información del dossier
    dossier_data = search_dossier(dossier_id)
    
    if not dossier_data:
        flash('No se encontró información para ese ID de dossier o ocurrió un error', 'error')
        return redirect(url_for('index'))
    
    return render_template('confirm.html', dossier_data=dossier_data, dossier_id=dossier_id)

@app.route('/delete', methods=['POST'])
def delete():
    """Eliminar dossier"""
    dossier_id = request.form.get('dossier_id')
    user_name = request.form.get('user_name', 'Usuario no especificado')
    
    if not dossier_id:
        flash('Error: No se especificó el ID del dossier', 'error')
        return redirect(url_for('index'))
    
    # Buscar los DossierArchivoIDs a eliminar
    dossier_data = search_dossier(dossier_id)
    
    if not dossier_data:
        flash('No se encontró el dossier especificado', 'error')
        return redirect(url_for('index'))
    
    # Extraer los IDs de archivo
    archivo_ids = [item['DossierArchivoID'] for item in dossier_data]
    
    # Eliminar archivos
    if delete_dossier_archives(archivo_ids, user_name):
        flash(f'Dossier {dossier_id} eliminado exitosamente', 'success')
        return render_template('success.html', dossier_id=dossier_id, deleted_count=len(archivo_ids))
    else:
        flash('Error al eliminar el dossier', 'error')
        return redirect(url_for('index'))

@app.route('/health')
def health():
    """Endpoint para verificar el estado de la aplicación"""
    return jsonify({'status': 'OK', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # Cambiar host y puerto según sea necesario