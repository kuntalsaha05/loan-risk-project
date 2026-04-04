// Expense Manager
let charts = {};

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('expenseForm');
  if (form) {
    form.addEventListener('submit', calculateExpenses);
    
    // Load saved expenses
    const savedExpenses = LoanRiskApp.storage.get('expenses');
    if (savedExpenses) {
      Object.keys(savedExpenses).forEach(key => {
        const input = form.elements[key];
        if (input) input.value = savedExpenses[key];
      });
    }
    
    // Initial calculation
    calculateExpenses();
  }

  setTimeout(() => {
    initializeCharts();
  }, 100);
});

function calculateExpenses(e) {
  if (e) e.preventDefault();

  const form = document.getElementById('expenseForm');
  const formData = new FormData(form);

  const monthlyIncome = parseFloat(formData.get('monthlyIncome'));
  const rent = parseFloat(formData.get('rent'));
  const food = parseFloat(formData.get('food'));
  const transport = parseFloat(formData.get('transport'));
  const emi = parseFloat(formData.get('emi'));
  const utilities = parseFloat(formData.get('utilities'));
  const entertainment = parseFloat(formData.get('entertainment'));
  const others = parseFloat(formData.get('others'));

  // Save to storage
  const expenses = {
    monthlyIncome, rent, food, transport, emi, utilities, entertainment, others
  };
  LoanRiskApp.storage.set('expenses', expenses);

  // Calculate totals
  const totalExpenses = rent + food + transport + emi + utilities + entertainment + others;
  const monthlySavings = monthlyIncome - totalExpenses;
  const savingsRate = (monthlySavings / monthlyIncome) * 100;
  const annualSavings = monthlySavings * 12;

  // Calculate health score
  const healthScore = calculateHealthScore(monthlyIncome, totalExpenses, emi, rent);

  // Update displays
  document.getElementById('displayIncome').textContent = LoanRiskApp.formatCurrency(monthlyIncome);
  document.getElementById('totalExpenses').textContent = LoanRiskApp.formatCurrency(totalExpenses);
  document.getElementById('monthlySavings').textContent = LoanRiskApp.formatCurrency(monthlySavings);
  document.getElementById('savingsRate').textContent = savingsRate.toFixed(0) + '%';
  document.getElementById('healthScore').textContent = Math.round(healthScore) + '/100';
  document.getElementById('annualSavings').textContent = LoanRiskApp.formatCurrency(annualSavings);

  // Update percentages
  document.getElementById('rentPercent').textContent = ((rent / monthlyIncome) * 100).toFixed(1);
  document.getElementById('foodPercent').textContent = ((food / monthlyIncome) * 100).toFixed(1);
  document.getElementById('transportPercent').textContent = ((transport / monthlyIncome) * 100).toFixed(1);
  document.getElementById('emiPercent').textContent = ((emi / monthlyIncome) * 100).toFixed(1);

  // Update displays
  document.getElementById('rentDisplay').textContent = LoanRiskApp.formatCurrency(rent);
  document.getElementById('foodDisplay').textContent = LoanRiskApp.formatCurrency(food);
  document.getElementById('transportDisplay').textContent = LoanRiskApp.formatCurrency(transport);
  document.getElementById('emiDisplay').textContent = LoanRiskApp.formatCurrency(emi);

  // Update charts
  if (charts.expense) {
    charts.expense.data.datasets[0].data = [rent, food, transport, emi, utilities, entertainment, others];
    charts.expense.update();
  }

  if (charts.savings) {
    const expensePercentage = (totalExpenses / monthlyIncome) * 100;
    charts.savings.data.datasets[0].data = [expensePercentage, savingsRate];
    charts.savings.update();
  }
}

function calculateHealthScore(income, expenses, emi, rent) {
  let score = 100;

  // Housing ratio (should be < 30%)
  const housingRatio = (rent / income) * 100;
  if (housingRatio > 40) score -= 20;
  else if (housingRatio > 30) score -= 10;
  else if (housingRatio < 20) score += 5;

  // Debt ratio (should be < 20%)
  const debtRatio = (emi / income) * 100;
  if (debtRatio > 30) score -= 25;
  else if (debtRatio > 20) score -= 15;
  else if (debtRatio < 10) score += 5;

  // Savings rate (should be > 20%)
  const expenseRatio = (expenses / income) * 100;
  const savingsRate = 100 - expenseRatio;
  if (savingsRate < 10) score -= 15;
  else if (savingsRate > 30) score += 10;

  return Math.max(0, Math.min(100, score));
}

function initializeCharts() {
  drawExpenseChart();
  drawSavingsChart();
}

function drawExpenseChart() {
  const canvas = document.getElementById('expenseChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.expense = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Rent', 'Food', 'Transport', 'EMI', 'Utilities', 'Entertainment', 'Others'],
      datasets: [{
        data: [1200, 400, 300, 600, 150, 250, 200],
        backgroundColor: [
          'rgba(217, 122, 78, 0.8)',
          'rgba(43, 95, 87, 0.8)',
          'rgba(232, 177, 74, 0.8)',
          'rgba(199, 62, 29, 0.8)',
          'rgba(45, 152, 93, 0.8)',
          'rgba(75, 120, 168, 0.8)',
          'rgba(160, 120, 168, 0.8)'
        ],
        borderColor: [
          'rgba(217, 122, 78, 1)',
          'rgba(43, 95, 87, 1)',
          'rgba(232, 177, 74, 1)',
          'rgba(199, 62, 29, 1)',
          'rgba(45, 152, 93, 1)',
          'rgba(75, 120, 168, 1)',
          'rgba(160, 120, 168, 1)'
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
            font: { size: 12, weight: '600' },
            color: '#504840',
            padding: 12,
            usePointStyle: true
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.parsed;
              return `${label}: ${LoanRiskApp.formatCurrency(value)}`;
            }
          }
        }
      }
    }
  });
}

function drawSavingsChart() {
  const canvas = document.getElementById('savingsChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  charts.savings = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Expenses', 'Savings'],
      datasets: [{
        data: [69, 31],
        backgroundColor: [
          'rgba(199, 62, 29, 0.8)',
          'rgba(45, 152, 93, 0.8)'
        ],
        borderColor: [
          'rgba(199, 62, 29, 1)',
          'rgba(45, 152, 93, 1)'
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
            font: { size: 12, weight: '600' },
            color: '#504840',
            padding: 12,
            usePointStyle: true
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const percentage = context.parsed || 0;
              return `${label}: ${percentage.toFixed(1)}%`;
            }
          }
        }
      }
    }
  });
}
