// Gestor de Dossiers - JavaScript (Versión 2.0 - DossierArchivoID)
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Gestor de Dossiers v2.0 cargado correctamente');
    
    // Inicializar funcionalidades
    initializeFormValidation();
    initializeConfirmationPage();
    initializeFlashMessages();
    initializeAnimations();
    initializeTableFeatures();
});

// Nueva función para funcionalidades de tabla
function initializeTableFeatures() {
    const queueTable = document.querySelector('.queue-table');
    
    if (queueTable) {
        // Hacer filas clicables
        const rows = queueTable.querySelectorAll('.queue-row');
        rows.forEach(row => {
            row.addEventListener('click', function() {
                const archivoId = this.getAttribute('data-archivo-id');
                copyToInput(archivoId);
                highlightRow(this);
            });
            
            // Efecto hover
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#e3f2fd';
                this.style.cursor = 'pointer';
            });
            
            row.addEventListener('mouseleave', function() {
                if (!this.classList.contains('selected')) {
                    this.style.backgroundColor = '';
                }
            });
        });
        
        // Búsqueda en tiempo real en la tabla
        addTableSearch();
        
        // Ordenamiento de columnas
        addTableSorting();
    }
}

// Copiar ID al formulario
function copyToInput(archivoId) {
    const input = document.querySelector('#dossier_archivo_id');
    if (input) {
        input.value = archivoId;
        input.focus();
        
        // Animación de éxito
        input.style.backgroundColor = '#d4edda';
        setTimeout(() => {
            input.style.backgroundColor = '';
        }, 1000);
        
        showAlert(`ID ${archivoId} copiado al formulario`, 'success');
    }
}

// Resaltar fila seleccionada
function highlightRow(row) {
    // Remover selección anterior
    const previousSelected = document.querySelector('.queue-row.selected');
    if (previousSelected) {
        previousSelected.classList.remove('selected');
        previousSelected.style.backgroundColor = '';
    }
    
    // Agregar selección a la nueva fila
    row.classList.add('selected');
    row.style.backgroundColor = '#e8f5e8';
}

// Agregar búsqueda en la tabla
function addTableSearch() {
    const tableCard = document.querySelector('.queue-table-card');
    if (!tableCard) return;
    
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = '🔍 Buscar en la tabla...';
    searchInput.className = 'table-search-input';
    searchInput.style.cssText = `
        width: 100%;
        padding: 0.75rem;
        margin: 1rem;
        border: 2px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
        box-sizing: border-box;
    `;
    
    const tableContainer = tableCard.querySelector('.table-container');
    tableContainer.insertBefore(searchInput, tableContainer.firstChild);
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('.queue-row');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

// Agregar ordenamiento a las columnas
function addTableSorting() {
    const headers = document.querySelectorAll('.queue-table th');
    
    headers.forEach((header, index) => {
        if (index < headers.length - 1) { // No agregar sort a la columna de acción
            header.style.cursor = 'pointer';
            header.title = 'Click para ordenar';
            
            header.addEventListener('click', function() {
                sortTable(index);
                updateSortIndicators(this);
            });
        }
    });
}

// Función para ordenar tabla
function sortTable(columnIndex) {
    const table = document.querySelector('.queue-table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const isNumeric = columnIndex === 0 || columnIndex === 5 || columnIndex === 6; // ArchivoID, DossierID, Cantidad
    
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        if (isNumeric) {
            return parseInt(aText) - parseInt(bText);
        } else {
            return aText.localeCompare(bText);
        }
    });
    
    // Re-agregar filas ordenadas
    rows.forEach(row => tbody.appendChild(row));
}

// Actualizar indicadores de ordenamiento
function updateSortIndicators(clickedHeader) {
    const headers = document.querySelectorAll('.queue-table th');
    
    // Remover indicadores previos
    headers.forEach(header => {
        header.classList.remove('sorted-asc', 'sorted-desc');
    });
    
    // Agregar indicador al header clickeado
    clickedHeader.classList.add('sorted-asc');
}

// Validación de formularios
function initializeFormValidation() {
    const searchForm = document.querySelector('.search-form');
    const confirmationForm = document.querySelector('.confirmation-form');
    
    // Validación del formulario de búsqueda
    if (searchForm) {
        const dossierInput = searchForm.querySelector('#dossier_archivo_id'); // ← CORREGIDO
        
        if (dossierInput) {
            dossierInput.addEventListener('input', function() {
                validateDossierInput(this);
            });
            
            searchForm.addEventListener('submit', function(e) {
                if (!validateDossierInput(dossierInput)) {
                    e.preventDefault();
                    showAlert('Por favor ingresa un ID de dossier archivo válido', 'error');
                }
            });
        }
    }
    
    // Validación del formulario de confirmación
    if (confirmationForm) {
        setupConfirmationValidation(confirmationForm);
    }
}

// Validar input del dossier ID
function validateDossierInput(input) {
    const value = input.value.trim();
    const isValid = value !== '' && !isNaN(value) && parseInt(value) > 0;
    
    // Cambiar estilo visual según validación
    if (value === '') {
        input.classList.remove('valid', 'invalid');
    } else if (isValid) {
        input.classList.remove('invalid');
        input.classList.add('valid');
    } else {
        input.classList.remove('valid');
        input.classList.add('invalid');
    }
    
    return isValid || value === '';
}

// Configurar validación del formulario de confirmación
function setupConfirmationValidation(form) {
    const checkbox = form.querySelector('#confirm_deletion');
    const deleteBtn = form.querySelector('#delete-btn');
    const userNameInput = form.querySelector('#user_name');
    
    function updateDeleteButton() {
        const isChecked = checkbox.checked;
        const hasUserName = userNameInput.value.trim().length >= 2;
        
        deleteBtn.disabled = !(isChecked && hasUserName);
        
        if (deleteBtn.disabled) {
            deleteBtn.style.cursor = 'not-allowed';
            deleteBtn.style.opacity = '0.6';
        } else {
            deleteBtn.style.cursor = 'pointer';
            deleteBtn.style.opacity = '1';
        }
    }
    
    // Eventos para validación en tiempo real
    checkbox.addEventListener('change', updateDeleteButton);
    userNameInput.addEventListener('input', updateDeleteButton);
    
    // Validación inicial
    updateDeleteButton();
    
    // Confirmación adicional antes de enviar
    form.addEventListener('submit', function(e) {
        if (!confirm('¿Estás absolutamente seguro de que deseas eliminar este dossier? Esta acción NO se puede deshacer.')) {
            e.preventDefault();
        } else {
            // Mostrar loading
            showLoadingState(deleteBtn);
        }
    });
}

// Inicializar página de confirmación
function initializeConfirmationPage() {
    const warningCard = document.querySelector('.warning-card');
    
    if (warningCard) {
        // Animación de entrada para la advertencia
        setTimeout(() => {
            warningCard.style.animation = 'pulse 2s ease-in-out infinite';
        }, 1000);
        
        // Agregar efectos de hover a la tabla
        const tableRows = document.querySelectorAll('tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#e8f4f8';
                this.style.transform = 'scale(1.02)';
                this.style.transition = 'all 0.2s ease';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
                this.style.transform = 'scale(1)';
            });
        });
    }
}

// Manejar mensajes flash
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert');
    
    flashMessages.forEach(message => {
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
        
        // Permitir cerrar manualmente
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.cssText = `
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            margin-left: auto;
            padding: 0 0.5rem;
        `;
        
        closeBtn.addEventListener('click', () => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(() => message.remove(), 300);
        });
        
        message.appendChild(closeBtn);
    });
}

// Inicializar animaciones
function initializeAnimations() {
    // Animación de entrada para las cards
    const cards = document.querySelectorAll('.search-card, .info-card, .dossier-info-card');
    
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Efecto de typing para el título
    const title = document.querySelector('.header h1');
    if (title && title.textContent === 'Gestor de Dossiers') {
        animateTyping(title, title.textContent);
    }
}

// Animación de escritura
function animateTyping(element, text) {
    element.textContent = '';
    let i = 0;
    
    const typing = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(typing);
        }
    }, 100);
}

// Mostrar estado de carga en botón
function showLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Eliminando...';
    button.disabled = true;
    
    // Simulación de proceso (en caso de que la eliminación sea muy rápida)
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Procesando...';
    }, 1000);
}

// Mostrar alertas personalizadas
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.flash-messages') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    
    const icon = type === 'success' ? 'check-circle' : 
                 type === 'error' ? 'exclamation-triangle' : 
                 'info-circle';
    
    alert.innerHTML = `
        <i class="fas fa-${icon}"></i>
        ${message}
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remover después de 4 segundos
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => alert.remove(), 300);
    }, 4000);
}

// Crear contenedor de alertas si no existe
function createAlertContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(container, mainContent.firstChild);
    
    return container;
}

// Utilidades para mejorar UX
function addTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #2c3e50;
                color: white;
                padding: 0.5rem;
                border-radius: 4px;
                font-size: 0.8rem;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 10) + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Función para imprimir comprobante (página de éxito)
function setupPrintFunction() {
    const printBtn = document.querySelector('[onclick="window.print()"]');
    if (printBtn) {
        printBtn.removeAttribute('onclick');
        printBtn.addEventListener('click', function() {
            // Crear versión para imprimir
            const printContent = generatePrintableContent();
            const printWindow = window.open('', '_blank');
            printWindow.document.write(printContent);
            printWindow.document.close();
            printWindow.print();
            printWindow.close();
        });
    }
}

// Generar contenido imprimible
function generatePrintableContent() {
    const dossierInfo = document.querySelector('.success-details');
    const currentDate = new Date().toLocaleString('es-CO');
    
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Comprobante de Eliminación - Global News</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2rem; }
                .header { text-align: center; border-bottom: 2px solid #ccc; padding-bottom: 1rem; margin-bottom: 2rem; }
                .content { margin: 1rem 0; }
                .footer { margin-top: 3rem; text-align: center; font-size: 0.9rem; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Global News</h1>
                <h2>Comprobante de Eliminación de Dossier</h2>
                <p>Fecha de generación: ${currentDate}</p>
            </div>
            <div class="content">
                ${dossierInfo ? dossierInfo.innerHTML : ''}
            </div>
            <div class="footer">
                <p>Este documento fue generado automáticamente por el Sistema Gestor de Dossiers</p>
                <p>Desarrollado por Kevin Gómez - Global News</p>
            </div>
        </body>
        </html>
    `;
}

// Inicializar todas las funcionalidades adicionales
setTimeout(() => {
    addTooltips();
    setupPrintFunction();
}, 1000);

// Manejar errores globalmente
window.addEventListener('error', function(e) {
    console.error('Error en la aplicación:', e.error);
    showAlert('Ha ocurrido un error inesperado. Por favor, recarga la página.', 'error');
});

// Función de utilidad para debugging (solo en desarrollo)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.debugApp = {
        showAlert: showAlert,
                validateInput: validateDossierInput
            };
        }