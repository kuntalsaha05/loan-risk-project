// What-If Simulation Handler
let comparisonChart = null;
let simulationData = {
  baseIncome: 50000,
  baseLoanAmount: 12000,
  baseTerm: 36,
  baseDTI: 18.4
};

document.addEventListener('DOMContentLoaded', function() {
  initializeSimulation();
  initComparisonChart();
  setupSliders();
});

function initializeSimulation() {
  simulationData = {
    baseIncome: 50000,
    baseLoanAmount: 12000,
    baseTerm: 36,
    baseDTI: 18.4
  };
  
  updateAllValues();
}

function setupSliders() {
  const incomeSlider = document.getElementById('incomeSlider');
  const loanAmountSlider = document.getElementById('loanAmountSlider');
  const termSlider = document.getElementById('termSlider');
  const dtiSlider = document.getElementById('dtiSlider');

  if (incomeSlider) incomeSlider.addEventListener('input', handleIncomeChange);
  if (loanAmountSlider) loanAmountSlider.addEventListener('input', handleLoanAmountChange);
  if (termSlider) termSlider.addEventListener('input', handleTermChange);
  if (dtiSlider) dtiSlider.addEventListener('input', handleDTIChange);
}

function handleIncomeChange(e) {
  simulationData.baseIncome = parseFloat(e.target.value);
  updateAllValues();
}

function handleLoanAmountChange(e) {
  simulationData.baseLoanAmount = parseFloat(e.target.value);
  updateAllValues();
}

function handleTermChange(e) {
  simulationData.baseTerm = parseFloat(e.target.value);
  updateAllValues();
}

function handleDTIChange(e) {
  simulationData.baseDTI = parseFloat(e.target.value);
  updateAllValues();
}

function updateAllValues() {
  // Update slider displays
  const incomeSlider = document.getElementById('incomeSlider');
  const loanSlider = document.getElementById('loanAmountSlider');
  const termSlider = document.getElementById('termSlider');
  const dtiSlider = document.getElementById('dtiSlider');

  if (incomeSlider) document.getElementById('incomeValue').textContent = LoanRiskApp.formatCurrency(simulationData.baseIncome);
  if (loanSlider) document.getElementById('loanAmountValue').textContent = LoanRiskApp.formatCurrency(simulationData.baseLoanAmount);
  if (termSlider) document.getElementById('termValue').textContent = simulationData.baseTerm + ' months';
  if (dtiSlider) document.getElementById('dtiValue').textContent = simulationData.baseDTI.toFixed(1) + '%';

  // Calculate metrics
  const baseRiskScore = 35; // Base from stored data
  const currentRiskScore = LoanRiskApp.calculateRiskScore(
    simulationData.baseIncome,
    simulationData.baseLoanAmount,
    simulationData.baseDTI,
    simulationData.baseTerm,
    1,
    750
  );

  const riskLevel = LoanRiskApp.getRiskLevel(currentRiskScore);
  const recommendedRate = LoanRiskApp.getRecommendedRate(currentRiskScore);
  const loanToIncome = ((simulationData.baseLoanAmount / simulationData.baseIncome) * 100).toFixed(1);

  // Update displays
  document.getElementById('currentRisk').textContent = currentRiskScore.toFixed(0) + '%';
  document.getElementById('riskBadge').className = 'badge ' + riskLevel.badge;
  document.getElementById('riskBadge').textContent = riskLevel.level;
  document.getElementById('currentDTI').textContent = simulationData.baseDTI.toFixed(1) + '%';
  document.getElementById('currentRate').textContent = recommendedRate + '%';
  document.getElementById('currentLTI').textContent = loanToIncome + '%';

  // Calculate risk change
  const riskChange = baseRiskScore - currentRiskScore;
  document.getElementById('riskReduction').textContent = (riskChange > 0 ? '↓ ' : '↑ ') + Math.abs(riskChange.toFixed(0)) + '%';

  // Update chart
  if (comparisonChart) {
    comparisonChart.data.datasets[0].data = [baseRiskScore, currentRiskScore];
    comparisonChart.update();
  }
}

function initComparisonChart() {
  const canvas = document.getElementById('comparisonChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  comparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Base Scenario', 'Your Scenario'],
      datasets: [{
        label: 'Risk Score (%)',
        data: [35, 35],
        backgroundColor: ['rgba(232, 177, 74, 0.6)', 'rgba(45, 152, 93, 0.6)'],
        borderColor: ['rgba(232, 177, 74, 1)', 'rgba(45, 152, 93, 1)'],
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

// Show recommendations
function showRecommendation(type) {
  let message = '';
  
  if (type === 'income') {
    message = '💡 <strong>Increase Income:</strong> Raising your income will significantly improve your debt-to-income ratio and reduce risk.';
  } else if (type === 'loan') {
    message = '💡 <strong>Reduce Loan Amount:</strong> A smaller loan amount will decrease your loan-to-income ratio and improve approval chances.';
  } else if (type === 'term') {
    message = '💡 <strong>Extend Term:</strong> A longer term reduces monthly obligations but increases total interest paid.';
  }
  
  LoanRiskApp.showAlert(message, 'info');
}
