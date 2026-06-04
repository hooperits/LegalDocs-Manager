/**
 * LegalDocs Manager - Custom Executive Dashboard Controller
 * 
 * Fetches dashboard statistics dynamically from the API and renders
 * beautiful metric cards, interactive charts, and deadline lists.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Only run if we are on the Executive Dashboard page
    const dashboardContainer = document.getElementById('dashboard-metrics-container');
    if (!dashboardContainer) {
        return;
    }

    // Helper function to translate a key
    function gettext(key, defaultValue) {
        if (window.DashboardTranslations && window.DashboardTranslations[key] !== undefined) {
            return window.DashboardTranslations[key];
        }
        return defaultValue || key;
    }

    // Set translation mapping for statuses
    const statusLabels = {
        'en_proceso': gettext('en_proceso', 'En Proceso'),
        'pendiente_documentos': gettext('pendiente_documentos', 'Pendiente Documentos'),
        'en_revision': gettext('en_revision', 'En Revisión'),
        'cerrado': gettext('cerrado', 'Cerrado')
    };

    // Set translation mapping for case types
    const caseTypeLabels = {
        'civil': gettext('civil', 'Civil'),
        'penal': gettext('penal', 'Penal'),
        'laboral': gettext('laboral', 'Laboral'),
        'mercantil': gettext('mercantil', 'Mercantil'),
        'familia': gettext('familia', 'Familia')
    };

    // Load statistics from the backend dashboard API
    fetch('/api/v1/dashboard/')
        .then(response => {
            if (!response.ok) {
                throw new Error(gettext('error_fetch', 'No se pudieron cargar las estadísticas del servidor.'));
            }
            return response.json();
        })
        .then(stats => {
            populateMetrics(stats);
            renderCharts(stats);
            renderUpcomingDeadlines(stats.upcoming_deadlines || []);
            renderRecentCases(stats.recent_cases || []);
        })
        .catch(error => {
            console.error('Error fetching dashboard stats:', error);
            showErrorMessage(error.message);
        });

    /**
     * Populate the four executive KPI cards at the top
     */
    function populateMetrics(stats) {
        // Calculate total cases and active cases
        const statusCounts = stats.cases_by_status || {};
        let totalCases = 0;
        let activeCases = 0;

        for (const [status, count] of Object.entries(statusCounts)) {
            totalCases += count;
            if (status !== 'cerrado') {
                activeCases += count;
            }
        }

        // Active Cases Card
        document.getElementById('metric-active-cases').textContent = activeCases;
        document.getElementById('metric-total-cases').textContent = totalCases;

        // Pending Documents Card
        const pendingDocs = statusCounts['pendiente_documentos'] || 0;
        document.getElementById('metric-pending-docs').textContent = pendingDocs;

        // Active Clients Card
        document.getElementById('metric-active-clients').textContent = stats.active_clients || 0;
        document.getElementById('metric-total-clients').textContent = stats.total_clients || 0;

        // Total Documents Card
        const docCounts = stats.documents_by_type || {};
        const totalDocs = Object.values(docCounts).reduce((sum, current) => sum + current, 0);
        document.getElementById('metric-total-docs').textContent = totalDocs;
    }

    /**
     * Render the charts using Chart.js
     */
    function renderCharts(stats) {
        if (typeof Chart === 'undefined') {
            console.warn('Chart.js is not loaded. Cannot display charts.');
            return;
        }

        // 1. Cases by Status Chart (Doughnut)
        const statusCtx = document.getElementById('chart-cases-status');
        if (statusCtx) {
            const statusCounts = stats.cases_by_status || {};
            const labels = [];
            const data = [];
            const backgroundColors = [];

            // Define color mapping matching our CSS status badges
            const colorMapping = {
                'en_proceso': 'rgba(14, 116, 144, 0.85)',       /* Teal */
                'pendiente_documentos': 'rgba(249, 115, 22, 0.85)', /* Orange */
                'en_revision': 'rgba(168, 85, 247, 0.85)',      /* Purple */
                'cerrado': 'rgba(16, 185, 129, 0.85)'          /* Green */
            };

            for (const [status, count] of Object.entries(statusCounts)) {
                labels.push(statusLabels[status] || status);
                data.push(count);
                backgroundColors.push(colorMapping[status] || 'rgba(148, 163, 184, 0.85)');
            }

            new Chart(statusCtx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: backgroundColors,
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                boxWidth: 12,
                                font: {
                                    family: "'Outfit', sans-serif",
                                    size: 11
                                },
                                color: '#475569'
                            }
                        }
                    },
                    cutout: '70%'
                }
            });
        }

        // 2. Cases by Type Chart (Bar)
        const typeCtx = document.getElementById('chart-cases-type');
        if (typeCtx) {
            const typeCounts = stats.cases_by_type || {};
            const labels = [];
            const data = [];

            for (const [type, count] of Object.entries(typeCounts)) {
                labels.push(caseTypeLabels[type] || type);
                data.push(count);
            }

            new Chart(typeCtx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: gettext('cases_dataset', 'Casos'),
                        data: data,
                        backgroundColor: 'rgba(14, 116, 144, 0.8)',
                        borderRadius: 6,
                        maxBarThickness: 32
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0,
                                font: {
                                    family: "'Inter', sans-serif"
                                }
                            },
                            grid: {
                                color: 'rgba(241, 245, 249, 0.8)'
                            }
                        },
                        x: {
                            ticks: {
                                font: {
                                    family: "'Outfit', sans-serif",
                                    weight: 500
                                }
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
    }

    /**
     * Render the upcoming deadlines list (alarm panel)
     */
    function renderUpcomingDeadlines(deadlines) {
        const container = document.getElementById('upcoming-deadlines-container');
        const countBadge = document.getElementById('deadline-count');
        
        if (!container) return;
        
        container.innerHTML = '';
        countBadge.textContent = deadlines.length;

        if (deadlines.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5 text-muted">
                    <i class="far fa-calendar-check fa-3x mb-2 text-success"></i><br>
                    <p class="m-0 font-weight-500">${gettext('no_deadlines', 'No hay vencimientos programados para los próximos 7 días.')}</p>
                </div>
            `;
            countBadge.classList.replace('badge-danger', 'badge-success');
            return;
        }

        deadlines.forEach(item => {
            // Determine urgency theme based on remaining days
            let urgencyClass = 'urgency-low';
            if (item.days_remaining <= 3) {
                urgencyClass = 'urgency-high';
            } else if (item.days_remaining <= 5) {
                urgencyClass = 'urgency-medium';
            }

            const itemHtml = `
                <div class="deadline-item ${urgencyClass}">
                    <div class="deadline-info">
                        <div class="deadline-title">
                            <a href="/admin/cases/case/${item.id}/change/" class="text-slate-900 font-weight-600">${item.title}</a>
                        </div>
                        <div class="deadline-meta">
                            <span><i class="fas fa-briefcase mr-1 text-xs"></i> ${item.case_number}</span>
                            <span><i class="fas fa-user mr-1 text-xs"></i> ${item.client_name}</span>
                        </div>
                    </div>
                    <div class="deadline-days">
                        ${item.days_remaining} ${item.days_remaining === 1 ? gettext('day', 'día') : gettext('days', 'días')}
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', itemHtml);
        });
    }

    /**
     * Render the recent cases table rows
     */
    function renderRecentCases(recentCases) {
        const tbody = document.getElementById('recent-cases-table-body');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (recentCases.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center py-4 text-muted">
                        ${gettext('no_cases', 'No hay casos registrados recientemente.')}
                    </td>
                </tr>
            `;
            return;
        }

        recentCases.forEach(item => {
            const statusText = statusLabels[item.status] || item.status;
            
            const rowHtml = `
                <tr>
                    <td>
                        <a href="/admin/cases/case/${item.id}/change/" class="font-weight-600">${item.case_number}</a>
                    </td>
                    <td>${item.title}</td>
                    <td>${item.client_name}</td>
                    <td>
                        <span class="badge badge-status-${item.status}">${statusText}</span>
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML('beforeend', rowHtml);
        });
    }

    /**
     * Show a clean error notification on the dashboard
     */
    function showErrorMessage(message) {
        const row = dashboardContainer.querySelector('.row');
        if (row) {
            row.insertAdjacentHTML('beforebegin', `
                <div class="alert alert-danger alert-dismissible fade show" role="alert" style="border-radius: 12px; margin-bottom: 24px;">
                    <h5><i class="icon fas fa-ban mr-2"></i> ${gettext('error_title', 'Error de Conexión')}</h5>
                    ${message} ${gettext('error_check', 'Por favor, verifique que los servicios y la base de datos estén activos.')}
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close" style="color: white; opacity: 0.8;">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            `);
        }
    }
});
