function buildScoreChart(recs) {
  const canvas = document.getElementById("scoreChart");
  if (!canvas || !recs || recs.length === 0) return;

  const labels = recs.map((r) => r.name);
  const values = recs.map((r) => r.score);

  new Chart(canvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Suitability",
          data: values,
          borderRadius: 6,
          backgroundColor: "rgba(5,102,141,0.75)",
        },
      ],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, max: 100 },
      },
    },
  });
}

function buildInputChart(inputs) {
  const canvas = document.getElementById("inputChart");
  if (!canvas || !inputs) return;

  new Chart(canvas, {
    type: "radar",
    data: {
      labels: ["Distance", "Accessibility", "Elevation", "Water Proximity", "Medical Need"],
      datasets: [
        {
          label: "User Input (numeric mapping)",
          data: [
            inputs.distance || 0,
            inputs.accessibility || 0,
            inputs.elevation || 0,
            inputs.proximity || 0,
            inputs.medical || 0,
          ],
          backgroundColor: "rgba(0,168,150,0.25)",
          borderColor: "rgba(0,168,150,1)",
          pointBackgroundColor: "rgba(0,168,150,1)",
        },
      ],
    },
    options: {
      scales: {
        r: {
          suggestedMin: 0,
          suggestedMax: 10,
          ticks: { stepSize: 2 },
        },
      },
    },
  });
}

function buildMap(recs) {
  const mapNode = document.getElementById("map");
  if (!mapNode || !recs || recs.length === 0) return;

  const map = L.map("map").setView([20.306, 85.820], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  const bounds = [];
  recs.forEach((r) => {
    const marker = L.marker([r.lat, r.lng]).addTo(map);
    marker.bindPopup(
      `<strong>${r.name}</strong><br/>Score: ${r.score}<br/>Distance: ${r.distance} km`
    );
    bounds.push([r.lat, r.lng]);
  });

  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [30, 30] });
  }
}

(() => {
  const data = window.RECOMMENDATION_DATA;
  if (!data) return;
  buildScoreChart(data.recommendations);
  buildInputChart(data.inputs_numeric);
  buildMap(data.recommendations);
})();
