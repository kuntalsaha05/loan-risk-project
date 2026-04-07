// Admin Panel
let charts = {};

const clusterMetrics = [
  { label: 'Low Risk', records: 41823, borrowerShare: 34.85, defaultRate: 11.99 },
  { label: 'Medium Risk', records: 29702, borrowerShare: 24.75, defaultRate: 18.93 },
  { label: 'High Risk', records: 48475, borrowerShare: 40.40, defaultRate: 26.73 },
];

const modelMetrics = [
  { label: 'Logistic Regression', accuracy: 80.56, f1: 8.76 },
  { label: 'Decision Tree', accuracy: 80.17, f1: 14.76 },
  { label: 'Random Forest', accuracy: 80.47, f1: 3.58 },
];

document.addEventListener('DOMContentLoaded', function() {
  setTimeout(() => {
    initializeAdminCharts();
  }, 100);
});

function initializeAdminCharts() {
  drawAdminRiskChart();
  drawLoanStatusChart();
  drawTrendsChart();
}

function drawAdminRiskChart() {
  const canvas = document.getElementById('adminRiskChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.adminRisk = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: clusterMetrics.map(cluster => cluster.label),
      datasets: [
        {
          label: 'Borrower Share (%)',
          data: clusterMetrics.map(cluster => cluster.borrowerShare),
          backgroundColor: 'rgba(75, 120, 168, 0.6)',
          borderColor: 'rgba(75, 120, 168, 1)',
          borderWidth: 2,
          borderRadius: 8
        },
        {
          label: 'Default Rate (%)',
          data: clusterMetrics.map(cluster => cluster.defaultRate),
          borderColor: 'rgba(199, 62, 29, 1)',
          backgroundColor: 'rgba(199, 62, 29, 0.6)',
          borderWidth: 2,
          borderRadius: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            font: { size: 13, weight: '600' },
            color: '#504840',
            padding: 16,
            usePointStyle: true
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            color: '#7a7268',
            font: { size: 12 },
            callback: function(value) {
              return value + '%';
            }
          },
          grid: { color: 'rgba(90, 80, 70, 0.08)' }
        },
        x: {
          ticks: {
            color: '#7a7268',
            font: { size: 12, weight: '600' }
          },
          grid: { display: false }
        }
      }
    }
  });
}

function drawLoanStatusChart() {
  const canvas = document.getElementById('loanStatusChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.loanStatus = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Non-Default', 'Default'],
      datasets: [{
        data: [318357, 77673],
        backgroundColor: [
          'rgba(45, 152, 93, 0.8)',
          'rgba(199, 62, 29, 0.8)'
        ],
        borderColor: [
          'rgba(45, 152, 93, 1)',
          'rgba(199, 62, 29, 1)'
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: { size: 13, weight: '600' },
            color: '#504840',
            padding: 16,
            usePointStyle: true
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.parsed;
              const total = 396030;
              const percentage = ((value / total) * 100).toFixed(2);
              return `${context.label}: ${value.toLocaleString()} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

function drawTrendsChart() {
  const canvas = document.getElementById('trendsChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.trends = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: modelMetrics.map(model => model.label),
      datasets: [
        {
          label: 'Accuracy (%)',
          data: modelMetrics.map(model => model.accuracy),
          backgroundColor: 'rgba(75, 120, 168, 0.6)',
          borderColor: 'rgba(75, 120, 168, 1)',
          borderWidth: 2,
          borderRadius: 8
        },
        {
          label: 'F1 Score (%)',
          data: modelMetrics.map(model => model.f1),
          backgroundColor: 'rgba(232, 177, 74, 0.6)',
          borderColor: 'rgba(232, 177, 74, 1)',
          borderWidth: 2,
          borderRadius: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            font: { size: 13, weight: '600' },
            color: '#504840',
            padding: 16,
            usePointStyle: true
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            color: '#7a7268',
            font: { size: 12 },
            callback: function(value) {
              return value + '%';
            }
          },
          grid: { color: 'rgba(90, 80, 70, 0.08)' }
        },
        x: {
          ticks: {
            color: '#7a7268',
            font: { size: 12, weight: '600' }
          },
          grid: { display: false }
        }
      }
    }
  });
}

// Export functions for admin tasks
window.AdminPanel = {
  exportData: function() {
    LoanRiskApp.showAlert('📊 Data exported successfully', 'success');
  },
  
  generateReport: function() {
    LoanRiskApp.showAlert('📈 Report generated successfully', 'success');
  },
  
  refreshData: function() {
    LoanRiskApp.showAlert('🔄 Data refreshed', 'info');
  }
};
