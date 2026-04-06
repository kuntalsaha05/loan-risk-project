// Shared utility functions and initialization

// Navigation highlighting
document.addEventListener('DOMContentLoaded', function() {
  const currentLocation = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === currentLocation || 
        (currentLocation === 'home.html' && link.getAttribute('href') === 'home.html')) {
      link.classList.add('active');
    }
  });
});

// Utility function to format currency
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value);
}

// Utility function to format percentage
function formatPercent(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value / 100);
}

// Utility function to calculate risk score
function calculateRiskScore(income, loanAmount, dti, term, existingLoans, creditScore = 750) {
  // Based on the dataset analysis
  let riskScore = 50; // Base score
  
  // DTI is the strongest predictor
  if (dti < 20) riskScore -= 15;
  else if (dti < 35) riskScore -= 5;
  else if (dti > 50) riskScore += 15;
  
  // Income effect
  const loanToIncomeRatio = (loanAmount / income) * 100;
  if (loanToIncomeRatio > 50) riskScore += 15;
  else if (loanToIncomeRatio > 30) riskScore += 8;
  
  // Loan term
  if (term > 50) riskScore += 5;
  
  // Existing loans
  if (existingLoans > 2) riskScore += 10;
  
  // Credit score
  if (creditScore > 750) riskScore -= 10;
  else if (creditScore < 650) riskScore += 15;
  
  // Clamp between 0 and 100
  return Math.max(0, Math.min(100, riskScore));
}

// Utility function to get risk level
function getRiskLevel(score) {
  if (score < 33) return { level: 'Low Risk', badge: 'badge-success' };
  if (score < 66) return { level: 'Medium Risk', badge: 'badge-warning' };
  return { level: 'High Risk', badge: 'badge-danger' };
}

// Utility function to get recommended interest rate
function getRecommendedRate(riskScore) {
  const baseRate = 8; // Base interest rate
  const riskPremium = (riskScore / 100) * 10;
  return (baseRate + riskPremium).toFixed(1);
}

// Utility function to get default stage
function getDefaultStage(dti, income) {
  if (dti < 15) return 'early';
  if (dti < 35) return 'mid';
  return 'late';
}

// Smooth scroll to element
function smoothScroll(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// Animation helper
function animateValue(element, start, end, duration = 1000) {
  const increment = (end - start) / (duration / 16);
  let current = start;
  
  const timer = setInterval(() => {
    current += increment;
    if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
      element.textContent = Math.round(end);
      clearInterval(timer);
    } else {
      element.textContent = Math.round(current);
    }
  }, 16);
}

// Show alert message
function showAlert(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type}`;
  alertDiv.innerHTML = message;
  alertDiv.style.position = 'fixed';
  alertDiv.style.top = '80px';
  alertDiv.style.right = '20px';
  alertDiv.style.maxWidth = '400px';
  alertDiv.style.zIndex = '2001';
  
  document.body.appendChild(alertDiv);
  
  setTimeout(() => {
    alertDiv.remove();
  }, 5000);
}

// Chart.js default options
const chartDefaults = {
  plugins: {
    legend: {
      labels: {
        font: { size: 13, weight: '600' },
        color: '#504840',
        padding: 16,
        usePointStyle: true,
      },
    },
  },
  scales: {
    y: {
      ticks: {
        color: '#7a7268',
        font: { size: 12 },
      },
      grid: { color: 'rgba(90, 80, 70, 0.08)' },
    },
    x: {
      ticks: {
        color: '#7a7268',
        font: { size: 12, weight: '600' },
      },
      grid: { display: false },
    },
  },
};

// Local storage helpers
const storage = {
  set: (key, value) => localStorage.setItem(`loan-risk-${key}`, JSON.stringify(value)),
  get: (key) => {
    const item = localStorage.getItem(`loan-risk-${key}`);
    return item ? JSON.parse(item) : null;
  },
  remove: (key) => localStorage.removeItem(`loan-risk-${key}`),
  clear: () => {
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('loan-risk-')) {
        localStorage.removeItem(key);
      }
    });
  }
};

// Export for use in other scripts
window.LoanRiskApp = {
  calculateRiskScore,
  getRiskLevel,
  getRecommendedRate,
  getDefaultStage,
  formatCurrency,
  formatPercent,
  showAlert,
  storage,
  chartDefaults,
  smoothScroll,
  animateValue
};

console.log('✅ Loan Risk App initialized');
