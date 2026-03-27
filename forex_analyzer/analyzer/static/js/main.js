// Forex Analyzer Main JavaScript

const API_BASE = '/api';

/**
 * Add a new forex pair
 */
function addNewPair() {
    const fromCurrency = document.getElementById('fromCurrency').value.trim();
    const toCurrency = document.getElementById('toCurrency').value.trim();
    
    if (!fromCurrency || !toCurrency) {
        showAlert('Please enter both currencies', 'warning');
        return;
    }
    
    if (fromCurrency.length !== 3 || toCurrency.length !== 3) {
        showAlert('Currency codes must be 3 letters (e.g., EUR, USD)', 'warning');
        return;
    }
    
    showLoading('Adding new pair...');
    
    fetch(`${API_BASE}/create-pair/?from=${fromCurrency}&to=${toCurrency}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(`Successfully added ${data.symbol}!`, 'success');
                document.getElementById('fromCurrency').value = '';
                document.getElementById('toCurrency').value = '';
                
                // Reload page after 1 second
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert(data.error || 'Failed to add pair', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error adding pair: ' + error.message, 'danger');
        })
        .finally(() => hideLoading());
}

/**
 * Refresh data for a specific pair
 */
function refreshPair(event, pairId) {
    event.preventDefault();
    event.stopPropagation();
    
    const button = event.target.closest('button');
    const originalHTML = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    fetch(`/pair/${pairId}/refresh/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert(data.error || 'Failed to refresh', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error refreshing pair', 'danger');
        })
        .finally(() => {
            button.disabled = false;
            button.innerHTML = originalHTML;
        });
}

/**
 * Load and display chart data
 */
function loadChartData(pairId) {
    fetch(`${API_BASE}/pair/${pairId}/data/`)
        .then(response => response.json())
        .then(data => {
            if (data.data_points && data.data_points.length > 0) {
                renderChart(data);
            }
        })
        .catch(error => console.error('Error loading chart data:', error));
}

/**
 * Render chart using Chart.js
 */
function renderChart(data) {
    const ctx = document.getElementById('priceChart');
    if (!ctx) return;
    
    const timestamps = data.data_points.map(p => new Date(p.timestamp).toLocaleDateString());
    const prices = data.data_points.map(p => p.close);
    const rsiValues = data.data_points.map(p => p.rsi || 0);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: 'Price',
                    data: prices,
                    borderColor: '#00d97e',
                    backgroundColor: 'rgba(0, 217, 126, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    yAxisID: 'y'
                },
                {
                    label: 'RSI',
                    data: rsiValues,
                    borderColor: '#ffd93d',
                    backgroundColor: 'rgba(255, 217, 61, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#fff',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                title: {
                    color: '#fff'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Price',
                        color: '#00d97e'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'RSI',
                        color: '#ffd93d'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 4000);
    }
}

/**
 * Show loading indicator
 */
function showLoading(message = 'Loading...') {
    const modal = document.createElement('div');
    modal.id = 'loadingModal';
    modal.className = 'modal fade show';
    modal.setAttribute('data-bs-backdrop', 'static');
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content bg-dark border-success">
                <div class="modal-body text-center">
                    <div class="spinner-border text-success mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="text-white">${message}</p>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        modal.remove();
    }
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return parseFloat(value).toFixed(5);
}

/**
 * Get badge class for greed level
 */
function getGreedBadgeClass(greedLevel) {
    const classes = {
        'extreme_greed': 'badge-extreme-greed',
        'greed': 'badge-greed',
        'neutral': 'badge-neutral',
        'fear': 'badge-fear',
        'extreme_fear': 'badge-extreme-fear'
    };
    return classes[greedLevel] || 'badge-neutral';
}

/**
 * Get signal class for trading signal
 */
function getSignalClass(signalType) {
    const classes = {
        'BUY': 'signal-buy',
        'SELL': 'signal-sell',
        'HOLD': 'signal-hold'
    };
    return classes[signalType] || 'signal-hold';
}

/**
 * Color code RSI value
 */
function getRSIColor(rsi) {
    if (rsi > 70) return 'text-danger-glow';
    if (rsi > 60) return 'text-warning';
    if (rsi < 30) return 'text-success-glow';
    if (rsi < 40) return 'text-info';
    return 'text-warning-glow';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Load Chart.js library
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
    document.head.appendChild(script);
});
