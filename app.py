from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pyodbc
from datetime import datetime
import logging
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar por una clave más segura

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dossier_operations.log'),
        logging.StreamHandler()
    ]
)

# Configuración de base de datos (completar con tus datos)
DB_CONFIG = {
    'server': '192.168.1.210',
    'database': '7787_GlobalnewsV2',
    'username': 'soporte',
    'password': 'T3cn0l0g14',
    'driver': '{ODBC Driver 17 for SQL Server}'  # o el driver que tengas disponible
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

def get_all_dossiers_in_queue():
    """Obtener todos los dossiers en cola (Termino=0)"""
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
        WHERE DA.Termino=0
        GROUP BY U.UserName,DA.DossierArchivoID,D.DossierID,D.FechaAlta,D.Nombre,DE.Descripcion
        ORDER BY D.FechaAlta DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Convertir resultados a lista de diccionarios
        columns = [column[0] for column in cursor.description]
        dossier_data = []
        for row in results:
            dossier_data.append(dict(zip(columns, row)))
        
        conn.close()
        return dossier_data
    except Exception as e:
        logging.error(f"Error obteniendo dossiers en cola: {str(e)}")
        conn.close()
        return None

def search_dossier_archivo(dossier_archivo_id):
    """Buscar información del dossier archivo específico antes de eliminarlo"""
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
        WHERE DA.Termino=0 AND DA.DossierArchivoID = ?
        GROUP BY U.UserName,DA.DossierArchivoID,D.DossierID,D.FechaAlta,D.Nombre,DE.Descripcion
        """
        cursor.execute(query, (dossier_archivo_id,))
        results = cursor.fetchall()
        
        # Convertir resultados a lista de diccionarios
        columns = [column[0] for column in cursor.description]
        dossier_data = []
        for row in results:
            dossier_data.append(dict(zip(columns, row)))
        
        conn.close()
        return dossier_data
    except Exception as e:
        logging.error(f"Error buscando dossier archivo {dossier_archivo_id}: {str(e)}")
        conn.close()
        return None

def delete_dossier_archivo(dossier_archivo_id, user_name):
    """Eliminar archivo específico del dossier"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Eliminar el registro específico
        query = "DELETE FROM dbo.gnNoti_DossierArchivos WHERE DossierArchivoID = ?"
        
        cursor.execute(query, (dossier_archivo_id,))
        conn.commit()
        
        # Verificar que se eliminó algo
        if cursor.rowcount == 0:
            logging.warning(f"No se encontró el DossierArchivoID: {dossier_archivo_id}")
            conn.close()
            return False
        
        # Log de la operación
        logging.info(f"Usuario: {user_name} eliminó DossierArchivoID: {dossier_archivo_id}")
        
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error eliminando dossier archivo: {str(e)}")
        conn.close()
        return False

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
    """Página principal con tabla de dossiers en cola"""
    # Obtener todos los dossiers en cola
    dossiers_en_cola = get_all_dossiers_in_queue()
    return render_template('index.html', dossiers_en_cola=dossiers_en_cola)

@app.route('/search', methods=['POST'])
def search():
    """Buscar dossier archivo por ID"""
    dossier_archivo_id = request.form.get('dossier_archivo_id')
    
    if not dossier_archivo_id:
        flash('Por favor ingresa un ID de dossier archivo válido', 'error')
        return redirect(url_for('index'))
    
    try:
        dossier_archivo_id = int(dossier_archivo_id)
    except ValueError:
        flash('El ID del dossier archivo debe ser un número', 'error')
        return redirect(url_for('index'))
    
    # Buscar información del dossier archivo
    dossier_data = search_dossier_archivo(dossier_archivo_id)
    
    if not dossier_data:
        flash('No se encontró información para ese ID de dossier archivo o ocurrió un error', 'error')
        return redirect(url_for('index'))
    
    return render_template('confirm.html', dossier_data=dossier_data, dossier_archivo_id=dossier_archivo_id)

@app.route('/delete', methods=['POST'])
def delete():
    """Eliminar dossier archivo"""
    dossier_archivo_id = request.form.get('dossier_archivo_id')
    user_name = request.form.get('user_name', 'Usuario no especificado')
    
    if not dossier_archivo_id:
        flash('Error: No se especificó el ID del dossier archivo', 'error')
        return redirect(url_for('index'))
    
    try:
        dossier_archivo_id = int(dossier_archivo_id)
    except ValueError:
        flash('El ID del dossier archivo debe ser un número válido', 'error')
        return redirect(url_for('index'))
    
    # Eliminar el archivo
    if delete_dossier_archivo(dossier_archivo_id, user_name):
        flash(f'Dossier Archivo {dossier_archivo_id} eliminado exitosamente', 'success')
        return render_template('success.html', dossier_archivo_id=dossier_archivo_id)
    else:
        flash('Error al eliminar el dossier archivo', 'error')
        return redirect(url_for('index'))

@app.route('/health')
def health():
    """Endpoint para verificar el estado de la aplicación"""
    return jsonify({'status': 'OK', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.174', port=5000)