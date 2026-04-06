// Loan Form Handler
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('loanForm');
  if (!form) return;

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    calculatePrediction();
  });

  // Add real-time validation
  form.querySelectorAll('input, select').forEach(input => {
    input.addEventListener('change', updateFormStatus);
  });
});

function calculatePrediction() {
  const form = document.getElementById('loanForm');
  const formData = new FormData(form);
  
  const loanAmount = parseFloat(formData.get('loanAmount'));
  const annualIncome = parseFloat(formData.get('annualIncome'));
  const dti = parseFloat(formData.get('dti'));
  const loanTerm = parseInt(formData.get('loanTerm'));
  const employmentType = formData.get('employmentType');
  const existingLoans = parseInt(formData.get('existingLoans'));
  const creditScore = parseFloat(formData.get('creditScore')) || 750;

  // Calculate metrics
  const riskScore = LoanRiskApp.calculateRiskScore(annualIncome, loanAmount, dti, loanTerm, existingLoans, creditScore);
  const riskLevel = LoanRiskApp.getRiskLevel(riskScore);
  const recommendedRate = LoanRiskApp.getRecommendedRate(riskScore);
  const defaultStage = LoanRiskApp.getDefaultStage(dti, annualIncome);
  const monthlyPayment = (loanAmount / loanTerm * 12).toFixed(2);
  const loanToIncome = ((loanAmount / annualIncome) * 100).toFixed(1);

  // Save to storage
  LoanRiskApp.storage.set('lastPrediction', {
    loanAmount, annualIncome, dti, loanTerm, employmentType, existingLoans, creditScore,
    riskScore, riskLevel, recommendedRate, defaultStage, monthlyPayment, loanToIncome
  });

  // Display results
  displayResults({
    riskScore, riskLevel, recommendedRate, defaultStage, 
    loanAmount, annualIncome, dti, loanTerm, monthlyPayment, loanToIncome
  });

  // Scroll to results
  setTimeout(() => {
    LoanRiskApp.smoothScroll('resultsContainer');
  }, 100);
}

function displayResults(data) {
  const resultsContainer = document.getElementById('resultsContainer');
  
  const html = `
    <div style="animation: fadeIn 0.5s ease-out;">
      <div style="text-align: center; margin: 40px 0 20px;">
        <h2>📊 Your Prediction Results</h2>
      </div>

      <div class="grid-2" style="margin-bottom: 40px;">
        <div class="result-card">
          <span class="result-label">Risk Score</span>
          <span class="result-value" id="resultRiskScore">${data.riskScore.toFixed(0)}%</span>
          <span class="badge ${data.riskLevel.badge}" style="margin-top: 8px;">${data.riskLevel.level}</span>
        </div>

        <div class="result-card">
          <span class="result-label">Recommended Interest Rate</span>
          <span class="result-value" id="resultRate">${data.recommendedRate}%</span>
          <p class="result-description">Based on your profile</p>
        </div>
      </div>

      <div class="grid-4" style="margin-bottom: 40px;">
        <div class="stat-box">
          <span class="stat-label">Loan Amount</span>
          <span class="stat-value" style="color: var(--primary);">${LoanRiskApp.formatCurrency(data.loanAmount)}</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Monthly Payment</span>
          <span class="stat-value" style="color: var(--primary);">${LoanRiskApp.formatCurrency(data.monthlyPayment)}</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">DTI Ratio</span>
          <span class="stat-value" style="color: var(--secondary);">${data.dti.toFixed(1)}%</span>
        </div>
        <div class="stat-box">
          <span class="stat-label">Loan-to-Income</span>
          <span class="stat-value" style="color: var(--secondary);">${data.loanToIncome}%</span>
        </div>
      </div>

      <div class="card" style="margin-bottom: 40px;">
        <h2>💡 Detailed Analysis</h2>
        <div class="grid-2">
          <div style="padding: 16px; background: rgba(255, 255, 255, 0.4); border-radius: 12px;">
            <h4>Risk Assessment</h4>
            <p><strong>Score:</strong> ${data.riskScore.toFixed(0)}/100</p>
            <p><strong>Category:</strong> ${data.riskLevel.level}</p>
            <p><strong>Default Stage:</strong> ${data.defaultStage}</p>
          </div>

          <div style="padding: 16px; background: rgba(255, 255, 255, 0.4); border-radius: 12px;">
            <h4>Financial Metrics</h4>
            <p><strong>Annual Income:</strong> ${LoanRiskApp.formatCurrency(data.annualIncome)}</p>
            <p><strong>Monthly Payment:</strong> ${LoanRiskApp.formatCurrency(data.monthlyPayment)}</p>
            <p><strong>Term:</strong> ${data.loanTerm} months</p>
          </div>

          <div style="padding: 16px; background: rgba(255, 255, 255, 0.4); border-radius: 12px;">
            <h4>Bank's Recommendation</h4>
            <p><strong>Interest Rate:</strong> ${data.recommendedRate}%</p>
            <p><strong>Decision:</strong> ${getRiskDecision(data.riskScore)}</p>
            <p><strong>Conditions:</strong> ${getConditions(data.dti)}</p>
          </div>

          <div style="padding: 16px; background: rgba(255, 255, 255, 0.4); border-radius: 12px;">
            <h4>Improvement Tips</h4>
            <p>${getImprovementTips(data.dti, data.loanToIncome)}</p>
          </div>
        </div>
      </div>

      <div class="card" style="margin-bottom: 40px;">
        <h2>📈 Risk Distribution Chart</h2>
        <div class="chart-container">
          <canvas id="resultChart"></canvas>
        </div>
      </div>

      <div style="text-align: center; gap: 12px; display: flex; flex-wrap: wrap; justify-content: center;">
        <a href="simulation.html" class="btn btn-secondary">🎮 Try What-If Simulation</a>
        <a href="expense-manager.html" class="btn btn-outlined">💸 Manage Expenses</a>
        <button onclick="printResults()" class="btn btn-outlined">🖨️ Print Results</button>
      </div>
    </div>
  `;

  resultsContainer.innerHTML = html;
  
  // Draw chart
  setTimeout(() => {
    drawResultChart(data.riskScore);
  }, 100);
}

function drawResultChart(riskScore) {
  const canvas = document.getElementById('resultChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  // Destroy existing chart if any
  if (window.resultChartInstance) {
    window.resultChartInstance.destroy();
  }

  const riskData = [
    riskScore,
    100 - riskScore
  ];

  window.resultChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Your Risk', 'Safe Zone'],
      datasets: [{
        data: riskData,
        backgroundColor: [
          riskScore < 33 ? 'rgba(45, 152, 93, 0.8)' : riskScore < 66 ? 'rgba(232, 177, 74, 0.8)' : 'rgba(199, 62, 29, 0.8)',
          'rgba(200, 200, 200, 0.3)'
        ],
        borderColor: [
          riskScore < 33 ? 'rgba(45, 152, 93, 1)' : riskScore < 66 ? 'rgba(232, 177, 74, 1)' : 'rgba(199, 62, 29, 1)',
          'rgba(150, 150, 150, 1)'
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

function getRiskDecision(score) {
  if (score < 33) return '✅ Approved - Low risk profile';
  if (score < 66) return '⚠️ Conditional Approval - Additional checks recommended';
  return '❌ Likely Rejected - High risk profile';
}

function getConditions(dti) {
  if (dti < 20) return 'Flexible terms available';
  if (dti < 35) return 'Standard terms apply';
  return 'Strict terms required';
}

function getImprovementTips(dti, loanToIncome) {
  let tips = [];
  if (dti > 35) tips.push('💡 Reduce debt obligations to improve DTI');
  if (loanToIncome > 30) tips.push('💡 Reduce loan amount or increase income');
  if (tips.length === 0) tips.push('✅ Your profile is well-balanced');
  return tips.join('<br>');
}

function updateFormStatus() {
  // Can add real-time validation here
}

function printResults() {
  const prediction = LoanRiskApp.storage.get('lastPrediction');
  if (!prediction) {
    LoanRiskApp.showAlert('No prediction found', 'warning');
    return;
  }

  const printWindow = window.open('', '', 'height=600,width=800');
  printWindow.document.write(`
    <html>
      <head>
        <title>Loan Risk Assessment - Prediction Report</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
          h1 { color: #d97a4e; text-align: center; }
          .section { margin: 30px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
          .metric { display: flex; justify-content: space-between; margin: 10px 0; padding: 8px 0; border-bottom: 1px solid #eee; }
          .label { font-weight: bold; }
          .value { color: #d97a4e; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>Loan Risk Assessment Report</h1>
        <div class="section">
          <h2>Risk Results</h2>
          <div class="metric"><span class="label">Risk Score:</span> <span class="value">${prediction.riskScore.toFixed(0)}%</span></div>
          <div class="metric"><span class="label">Risk Level:</span> <span class="value">${prediction.riskLevel.level}</span></div>
          <div class="metric"><span class="label">Interest Rate:</span> <span class="value">${prediction.recommendedRate}%</span></div>
        </div>
        <div class="section">
          <h2>Loan Details</h2>
          <div class="metric"><span class="label">Loan Amount:</span> <span class="value">$${prediction.loanAmount.toLocaleString()}</span></div>
          <div class="metric"><span class="label">Loan Term:</span> <span class="value">${prediction.loanTerm} months</span></div>
          <div class="metric"><span class="label">Monthly Payment:</span> <span class="value">$${prediction.monthlyPayment}</span></div>
        </div>
        <div class="section">
          <h2>Financial Metrics</h2>
          <div class="metric"><span class="label">Annual Income:</span> <span class="value">$${prediction.annualIncome.toLocaleString()}</span></div>
          <div class="metric"><span class="label">DTI Ratio:</span> <span class="value">${prediction.dti.toFixed(1)}%</span></div>
          <div class="metric"><span class="label">Loan-to-Income:</span> <span class="value">${prediction.loanToIncome}%</span></div>
        </div>
      </body>
    </html>
  `);
  printWindow.document.close();
  printWindow.print();
}
