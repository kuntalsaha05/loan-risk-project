// Visualizations Dashboard
let charts = {};

document.addEventListener('DOMContentLoaded', function() {
  setTimeout(() => {
    initializeCharts();
  }, 100);
});

function initializeCharts() {
  drawModelChart();
  drawRiskDistributionChart();
  drawClusterChart();
  drawDefaultRateChart();
  drawFeaturesChart();
}

function drawModelChart() {
  const canvas = document.getElementById('modelChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.model = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Logistic Regression', 'Decision Tree', 'Random Forest'],
      datasets: [
        {
          label: 'F1 Score',
          data: [0.0876, 0.1476, 0.0358],
          backgroundColor: 'rgba(217, 122, 78, 0.6)',
          borderColor: 'rgba(217, 122, 78, 1)',
          borderWidth: 2,
          borderRadius: 8
        },
        {
          label: 'Accuracy',
          data: [0.8056, 0.8017, 0.8047],
          backgroundColor: 'rgba(43, 95, 87, 0.6)',
          borderColor: 'rgba(43, 95, 87, 1)',
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
          max: 1,
          ticks: {
            color: '#7a7268',
            font: { size: 12 },
            callback: function(value) {
              return (value * 100).toFixed(0) + '%';
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

function drawRiskDistributionChart() {
  const canvas = document.getElementById('riskDistributionChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.riskDist = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Low Risk Cluster', 'Medium Risk Cluster', 'High Risk Cluster'],
      datasets: [{
        data: [34.9, 24.8, 40.4],
        backgroundColor: [
          'rgba(45, 152, 93, 0.8)',
          'rgba(232, 177, 74, 0.8)',
          'rgba(199, 62, 29, 0.8)'
        ],
        borderColor: [
          'rgba(45, 152, 93, 1)',
          'rgba(232, 177, 74, 1)',
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
        }
      }
    }
  });
}

function drawClusterChart() {
  const canvas = document.getElementById('clusterChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const totalBorrowers = 120000;
  
  charts.cluster = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Low Risk', 'Medium Risk', 'High Risk'],
      datasets: [{
        data: [41823, 29702, 48475],
        backgroundColor: [
          'rgba(212, 240, 224, 0.8)',
          'rgba(253, 232, 197, 0.8)',
          'rgba(255, 212, 206, 0.8)'
        ],
        borderColor: [
          'rgba(29, 92, 62, 1)',
          'rgba(139, 90, 0, 1)',
          'rgba(140, 44, 31, 1)'
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
              const label = context.label || '';
              const value = context.parsed;
              const percentage = ((value / totalBorrowers) * 100).toFixed(1);
              return `${label}: ${value.toLocaleString()} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

function drawDefaultRateChart() {
  const canvas = document.getElementById('defaultRateChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.defaultRate = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Low Risk', 'Medium Risk', 'High Risk'],
      datasets: [{
        label: 'Default Rate (%)',
        data: [11.99, 18.93, 26.73],
        backgroundColor: [
          'rgba(45, 152, 93, 0.6)',
          'rgba(232, 177, 74, 0.6)',
          'rgba(199, 62, 29, 0.6)'
        ],
        borderColor: [
          'rgba(45, 152, 93, 1)',
          'rgba(232, 177, 74, 1)',
          'rgba(199, 62, 29, 1)'
        ],
        borderWidth: 2,
        borderRadius: 8
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

function drawFeaturesChart() {
  const canvas = document.getElementById('featuresChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.features = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
      labels: ['DTI Ratio', 'Income', 'Loan Amount', 'Credit Score', 'Employment', 'Existing Loans'],
      datasets: [{
        label: 'Feature Importance (%)',
        data: [35, 28, 18, 12, 5, 2],
        backgroundColor: 'rgba(217, 122, 78, 0.6)',
        borderColor: 'rgba(217, 122, 78, 1)',
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 40,
          ticks: {
            color: '#7a7268',
            font: { size: 12 },
            callback: function(value) {
              return value + '%';
            }
          },
          grid: { color: 'rgba(90, 80, 70, 0.08)' }
        },
        y: {
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
