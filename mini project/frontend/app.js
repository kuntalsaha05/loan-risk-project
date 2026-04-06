// Data
const stats = [
  { label: "Processed Rows", value: "396,030" },
  { label: "Selected Features", value: "24" },
  { label: "Best Classifier", value: "Decision Tree" },
  { label: "Database Table", value: "loan_records" },
];

const prediction = {
  defaultProbability: "0.081",
  defaultStage: "non_default",
  riskCluster: "low_risk",
  recommendedInterestRate: "10.5%",
};

const simulationRows = [
  ["base_case", "12,000", "18.4", "36", "0.081", "non_default", "low_risk"],
  ["lower_loan_amount", "10,200", "18.4", "36", "0.081", "non_default", "low_risk"],
  ["lower_dti", "12,000", "13.4", "36", "0.0838", "non_default", "low_risk"],
  ["shorter_term", "12,000", "18.4", "36", "0.081", "non_default", "low_risk"],
];

const models = [
  { name: "Logistic Regression", accuracy: 0.8056, f1: 0.0876 },
  { name: "Decision Tree", accuracy: 0.8017, f1: 0.1476 },
  { name: "Random Forest", accuracy: 0.8047, f1: 0.0358 },
];

const clusters = [
  { name: "low_risk", records: "64,794", defaultFlag: 0.0000 },
  { name: "medium_risk", records: "32,769", defaultFlag: 0.0354 },
  { name: "high_risk", records: "22,437", defaultFlag: 0.9997 },
];

// Utility Functions
function riskClass(name) {
  if (name.includes("low")) return "risk-low";
  if (name.includes("medium")) return "risk-medium";
  return "risk-high";
}

function formatNumber(num) {
  return new Intl.NumberFormat('en-US').format(num);
}

// Render Functions
function renderStats() {
  const root = document.getElementById("stats-grid");
  root.innerHTML = stats
    .map(
      (item) => `
        <article class="stat-tile" data-value="${item.value}">
          <span class="tile-label">${item.label}</span>
          <strong>${item.value}</strong>
        </article>
      `
    )
    .join("");
  animateTiles(".stat-tile");
}

function renderPrediction() {
  const root = document.getElementById("prediction-grid");
  root.innerHTML = `
    <article class="prediction-tile" data-value="${prediction.defaultProbability}">
      <span class="tile-label">Default Probability</span>
      <strong>${prediction.defaultProbability}</strong>
    </article>
    <article class="prediction-tile" data-value="${prediction.defaultStage}">
      <span class="tile-label">Default Stage</span>
      <strong>${prediction.defaultStage}</strong>
    </article>
    <article class="prediction-tile" data-value="${prediction.riskCluster}">
      <span class="tile-label">Risk Cluster</span>
      <strong><span class="risk-pill ${riskClass(prediction.riskCluster)}">${prediction.riskCluster}</span></strong>
    </article>
    <article class="prediction-tile" data-value="${prediction.recommendedInterestRate}">
      <span class="tile-label">Recommended Interest</span>
      <strong>${prediction.recommendedInterestRate}</strong>
    </article>
  `;
  animateTiles(".prediction-tile");
}

function renderSimulation() {
  const body = document.getElementById("simulation-body");
  body.innerHTML = simulationRows
    .map(
      (row, index) => `
        <tr style="animation-delay: ${index * 0.1}s">
          <td>${row[0].replace(/_/g, " ")}</td>
          <td>$${row[1]}</td>
          <td>${row[2]}</td>
          <td>${row[3]}</td>
          <td>${row[4]}</td>
          <td>${row[5]}</td>
          <td><span class="risk-pill ${riskClass(row[6])}">${row[6]}</span></td>
        </tr>
      `
    )
    .join("");
}

function renderModels() {
  const root = document.getElementById("model-list");
  root.innerHTML = models
    .map(
      (model) => `
        <article class="model-item" data-model="${model.name}">
          <span class="tile-label">${model.name}</span>
          <strong>F1 ${model.f1.toFixed(4)}</strong>
          <p>Accuracy ${(model.accuracy * 100).toFixed(2)}%</p>
        </article>
      `
    )
    .join("");
  animateTiles(".model-item");
}

function renderClusters() {
  const root = document.getElementById("cluster-list");
  root.innerHTML = clusters
    .map(
      (cluster) => `
        <article class="cluster-item" data-cluster="${cluster.name}">
          <span class="risk-pill ${riskClass(cluster.name)}">${cluster.name}</span>
          <strong>${formatNumber(cluster.records)} borrowers</strong>
          <p>Avg default rate ${(cluster.defaultFlag * 100).toFixed(2)}%</p>
        </article>
      `
    )
    .join("");
  animateTiles(".cluster-item");
}

// Chart.js Visualizations
function initModelsChart() {
  const ctx = document.getElementById("models-chart");
  if (!ctx) return;

  const chartConfig = {
    type: "bar",
    data: {
      labels: models.map(m => m.name),
      datasets: [
        {
          label: "F1 Score",
          data: models.map(m => m.f1),
          backgroundColor: "rgba(217, 122, 78, 0.6)",
          borderColor: "rgba(217, 122, 78, 1)",
          borderWidth: 2,
          borderRadius: 8,
        },
        {
          label: "Accuracy",
          data: models.map(m => m.accuracy),
          backgroundColor: "rgba(43, 95, 87, 0.6)",
          borderColor: "rgba(43, 95, 87, 1)",
          borderWidth: 2,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            font: { size: 13, weight: "600" },
            color: "#504840",
            padding: 16,
            usePointStyle: true,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 1,
          ticks: {
            color: "#7a7268",
            font: { size: 12 },
            callback: function(value) {
              return (value * 100).toFixed(0) + "%";
            },
          },
          grid: { color: "rgba(90, 80, 70, 0.08)" },
        },
        x: {
          ticks: {
            color: "#7a7268",
            font: { size: 12, weight: "600" },
          },
          grid: { display: false },
        },
      },
    },
  };

  new Chart(ctx, chartConfig);
}

function initClustersChart() {
  const ctx = document.getElementById("clusters-chart");
  if (!ctx) return;

  const totalBorrowers = clusters.reduce((sum, c) => sum + parseInt(c.records.replace(/,/g, "")), 0);
  const clusterData = clusters.map(c => parseInt(c.records.replace(/,/g, "")));

  const chartConfig = {
    type: "doughnut",
    data: {
      labels: clusters.map(c => c.name.replace(/_/g, " ")),
      datasets: [
        {
          data: clusterData,
          backgroundColor: [
            "rgba(212, 240, 224, 0.8)",
            "rgba(253, 232, 197, 0.8)",
            "rgba(255, 212, 206, 0.8)",
          ],
          borderColor: [
            "rgba(29, 92, 62, 1)",
            "rgba(139, 90, 0, 1)",
            "rgba(140, 44, 31, 1)",
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            font: { size: 13, weight: "600" },
            color: "#504840",
            padding: 16,
            usePointStyle: true,
          },
          display: true,
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || "";
              const value = context.parsed;
              const percentage = ((value / totalBorrowers) * 100).toFixed(1);
              return `${label}: ${formatNumber(value)} (${percentage}%)`;
            },
          },
        },
      },
    },
  };

  new Chart(ctx, chartConfig);
}

// Animation Functions
function animateTiles(selector) {
  const tiles = document.querySelectorAll(selector);
  tiles.forEach((tile, index) => {
    tile.style.animation = `fadeInUp 0.6s ease-out ${index * 0.1}s both`;
  });
}

// Add animation keyframes
function addAnimationStyles() {
  const style = document.createElement("style");
  style.textContent = `
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(16px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  `;
  document.head.appendChild(style);
}

// Initialize
document.addEventListener("DOMContentLoaded", function() {
  addAnimationStyles();
  renderStats();
  renderPrediction();
  renderSimulation();
  renderModels();
  renderClusters();

  // Initialize charts after a small delay to ensure Chart.js is loaded
  setTimeout(() => {
    initModelsChart();
    initClustersChart();
  }, 100);

  // Add smooth scrolling behavior for better UX
  document.querySelectorAll("a[href^='#']").forEach((anchor) => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Log initialization
  console.log("Dashboard initialized successfully", {
    models: models.length,
    clusters: clusters.length,
    stats: stats.length,
  });
});
