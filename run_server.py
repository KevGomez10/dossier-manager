#!/usr/bin/env python3
"""
Gestor de Dossiers - Global News
Script para ejecutar en servidor de producción
Desarrollado por: Kevin Gómez
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Importar configuraciones de servidor
    from server_config import setup_server_logging, show_server_info, SERVER_CONFIG, SECURITY_CONFIG
    
    # Configurar logging antes que nada
    setup_server_logging()
    
    # Importar la aplicación principal
    from app import app
    
    # Aplicar configuraciones de seguridad
    app.config.update(SECURITY_CONFIG)
    
    def main():
        """Función principal para ejecutar el servidor"""
        print("\nIniciando Gestor de Dossiers...")
        
        # Mostrar información del servidor
        show_server_info()
        
        try:
            # Iniciar servidor
            app.run(**SERVER_CONFIG)
            
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario")
        except Exception as e:
            print(f"\nError al iniciar servidor: {str(e)}")
            input("Presiona Enter para continuar...")
        finally:
            print("¡Hasta luego!")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Error de importación: {str(e)}")
    print("Asegúrate de que todos los archivos estén en el mismo directorio")
    input("Presiona Enter para continuar...")
except Exception as e:
    print(f"Error inesperado: {str(e)}")
    input("Presiona Enter para continuar...")