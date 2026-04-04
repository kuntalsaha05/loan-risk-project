// Admin Panel
let charts = {};

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
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [
        {
          label: 'Low Risk',
          data: [45, 48, 50, 52, 51, 54, 56, 55, 57, 58, 60, 62],
          borderColor: 'rgba(45, 152, 93, 1)',
          backgroundColor: 'rgba(45, 152, 93, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          fill: true
        },
        {
          label: 'Medium Risk',
          data: [30, 28, 27, 25, 26, 24, 22, 23, 21, 20, 19, 18],
          borderColor: 'rgba(232, 177, 74, 1)',
          backgroundColor: 'rgba(232, 177, 74, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          fill: true
        },
        {
          label: 'High Risk',
          data: [25, 24, 23, 23, 23, 22, 22, 22, 22, 22, 21, 20],
          borderColor: 'rgba(199, 62, 29, 1)',
          backgroundColor: 'rgba(199, 62, 29, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          fill: true
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
            font: { size: 12 }
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
      labels: ['Active', 'Paid Off', 'Defaulted', 'In Process'],
      datasets: [{
        data: [60, 25, 10, 5],
        backgroundColor: [
          'rgba(45, 152, 93, 0.8)',
          'rgba(75, 120, 168, 0.8)',
          'rgba(199, 62, 29, 0.8)',
          'rgba(232, 177, 74, 0.8)'
        ],
        borderColor: [
          'rgba(45, 152, 93, 1)',
          'rgba(75, 120, 168, 1)',
          'rgba(199, 62, 29, 1)',
          'rgba(232, 177, 74, 1)'
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
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      datasets: [
        {
          label: 'Approvals',
          data: [850, 920, 1100, 1450],
          backgroundColor: 'rgba(45, 152, 93, 0.6)',
          borderColor: 'rgba(45, 152, 93, 1)',
          borderWidth: 2,
          borderRadius: 8
        },
        {
          label: 'Defaults',
          data: [120, 145, 180, 220],
          backgroundColor: 'rgba(199, 62, 29, 0.6)',
          borderColor: 'rgba(199, 62, 29, 1)',
          borderWidth: 2,
          borderRadius: 8
        },
        {
          label: 'Disputes',
          data: [45, 52, 68, 95],
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
          ticks: {
            color: '#7a7268',
            font: { size: 12 },
            callback: function(value) {
              return value.toLocaleString();
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
