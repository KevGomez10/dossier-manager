# Configuración para servidor - Global News
# Este archivo contiene configuraciones específicas para producción

import os
import logging
from datetime import datetime

# Configuración de logging para servidor
def setup_server_logging():
    """Configurar logging para ambiente de producción"""
    
    # Crear directorio de logs si no existe
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nombre del archivo de log con fecha
    log_filename = f"{log_dir}/dossier_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configuración avanzada de logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler(),  # También mostrar en consola
        ]
    )
    
    # Log inicial
    logging.info("=" * 60)
    logging.info("GESTOR DE DOSSIERS - GLOBAL NEWS INICIADO")
    logging.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Log file: {log_filename}")
    logging.info("=" * 60)

# Configuración de base de datos para servidor
SERVER_DB_CONFIG = {
    'server': '192.168.1.139',
    'database': '7787_GlobalnewsV2', 
    'username': 'soporte',
    'password': 'T3cn0l0g14',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'timeout': 30,  # Timeout de conexión
    'autocommit': True
}

# Configuración del servidor web
SERVER_CONFIG = {
    'host': '0.0.0.0',  # Permite conexiones desde cualquier IP
    'port': 5000,
    'debug': False,     # IMPORTANTE: False en producción
    'threaded': True,   # Permite múltiples usuarios simultáneos
    'use_reloader': False
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'secret_key': 'global-news-dossier-manager-2025-production-key',  # Cambiar por una clave más segura
    'max_content_length': 16 * 1024 * 1024,  # 16MB max
    'permanent_session_lifetime': 3600  # 1 hora de sesión
}

# Función para verificar estado del servidor
def health_check():
    """Verificar que todos los componentes estén funcionando"""
    checks = {
        'database': False,
        'logs': False,
        'server': False
    }
    
    try:
        # Verificar directorio de logs
        if os.path.exists('logs'):
            checks['logs'] = True
        
        # Verificar conexión a BD (implementar después)
        # checks['database'] = test_db_connection()
        
        checks['server'] = True
        
    except Exception as e:
        logging.error(f"Error en health check: {str(e)}")
    
    return checks

# Función para mostrar información del servidor
def show_server_info():
    """Mostrar información importante del servidor"""
    print("\n" + "="*60)
    print("GESTOR DE DOSSIERS - GLOBAL NEWS")
    print("="*60)
    print(f"Servidor: {SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}")
    print(f"URL de acceso: http://192.168.1.139:{SERVER_CONFIG['port']}")
    print(f"Directorio de logs: ./logs/")
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("📋 INSTRUCCIONES:")
    print("   1. Configura la BD en SERVER_DB_CONFIG")
    print("   2. Accede desde cualquier navegador de la red")
    print("   3. Los logs se guardan automáticamente")
    print("   4. Para detener: Ctrl+C")
    print("="*60)
    
    # Health check
    checks = health_check()
    print("🔍 ESTADO DE COMPONENTES:")
    for component, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component.capitalize()}: {'OK' if status else 'ERROR'}")
    print("="*60)

if __name__ == "__main__":
    show_server_info()