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
  { name: "Logistic Regression", accuracy: "0.8056", f1: "0.0876" },
  { name: "Decision Tree", accuracy: "0.8017", f1: "0.1476" },
  { name: "Random Forest", accuracy: "0.8047", f1: "0.0358" },
];

const clusters = [
  { name: "low_risk", records: "64,794", defaultFlag: "0.0000" },
  { name: "medium_risk", records: "32,769", defaultFlag: "0.0354" },
  { name: "high_risk", records: "22,437", defaultFlag: "0.9997" },
];

function riskClass(name) {
  if (name.includes("low")) return "risk-low";
  if (name.includes("medium")) return "risk-medium";
  return "risk-high";
}

function renderStats() {
  const root = document.getElementById("stats-grid");
  root.innerHTML = stats
    .map(
      (item) => `
        <article class="stat-tile">
          <span class="tile-label">${item.label}</span>
          <strong>${item.value}</strong>
        </article>
      `
    )
    .join("");
}

function renderPrediction() {
  const root = document.getElementById("prediction-grid");
  root.innerHTML = `
    <article class="prediction-tile">
      <span class="tile-label">Default Probability</span>
      <strong>${prediction.defaultProbability}</strong>
    </article>
    <article class="prediction-tile">
      <span class="tile-label">Default Stage</span>
      <strong>${prediction.defaultStage}</strong>
    </article>
    <article class="prediction-tile">
      <span class="tile-label">Risk Cluster</span>
      <strong><span class="risk-pill ${riskClass(prediction.riskCluster)}">${prediction.riskCluster}</span></strong>
    </article>
    <article class="prediction-tile">
      <span class="tile-label">Recommended Interest</span>
      <strong>${prediction.recommendedInterestRate}</strong>
    </article>
  `;
}

function renderSimulation() {
  const body = document.getElementById("simulation-body");
  body.innerHTML = simulationRows
    .map(
      (row) => `
        <tr>
          <td>${row[0]}</td>
          <td>${row[1]}</td>
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
        <article class="model-item">
          <span class="tile-label">${model.name}</span>
          <strong>F1 ${model.f1}</strong>
          <p>Accuracy ${model.accuracy}</p>
        </article>
      `
    )
    .join("");
}

function renderClusters() {
  const root = document.getElementById("cluster-list");
  root.innerHTML = clusters
    .map(
      (cluster) => `
        <article class="cluster-item">
          <span class="risk-pill ${riskClass(cluster.name)}">${cluster.name}</span>
          <strong>${cluster.records} borrowers</strong>
          <p>Avg default flag ${cluster.defaultFlag}</p>
        </article>
      `
    )
    .join("");
}

renderStats();
renderPrediction();
renderSimulation();
renderModels();
renderClusters();
