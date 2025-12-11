// App Scripts - Namespace Pattern for Global Functions
const AppUtils = {
    // Format Currency to Brazilian Real
    formatCurrency: function(value) {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    },

    // Debounce Function for Search and Input Events
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Safe Chart.js Data Wrapper
    validateChartData: function(labels, data) {
        return (
            Array.isArray(labels) && 
            Array.isArray(data) && 
            labels.length > 0 && 
            data.length > 0 &&
            labels.length === data.length
        );
    }
};

// Initialize App on DOM Ready
document.addEventListener('DOMContentLoaded', function () {
    // Force light mode only - no dark mode
    document.body.removeAttribute('data-theme');
    localStorage.removeItem('theme');

    // Toast Notifications
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    const toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl);
    });
    toastList.forEach(toast => toast.show());

    // Loading Spinner
    const forms = document.querySelectorAll('form:not([no-loading])');
    const spinner = document.getElementById('loading-spinner');

    forms.forEach(form => {
        form.addEventListener('submit', function () {
            if (form.checkValidity()) {
                if (spinner) spinner.classList.add('show');
            }
        });
    });

    // Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
});

// Maintain backward compatibility - Global references
function formatCurrency(value) {
    return AppUtils.formatCurrency(value);
}

function debounce(func, wait) {
    return AppUtils.debounce(func, wait);
}
