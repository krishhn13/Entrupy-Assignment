import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function App() {

  const [summary, setSummary] = useState(null);
  const [products, setProducts] = useState([]);
  const [history, setHistory] = useState(null);

  const headers = { "x-api-key": "test-key-123" };

  useEffect(() => {

    axios.get("http://127.0.0.1:8000/analytics/summary", { headers })
      .then(res => setSummary(res.data));

    axios.get("http://127.0.0.1:8000/products?page=1&limit=20", { headers })
      .then(res => setProducts(res.data.data));

  }, []);

  const loadHistory = (productId) => {

    axios.get(
      `http://127.0.0.1:8000/products/${productId}/history`,
      { headers }
    ).then(res => setHistory(res.data.history));

  };

  if (!summary) return <div>Loading dashboard...</div>;

  const chartData = history ? {
    labels: history.map(h => new Date(h.recorded_at).toLocaleDateString()),
    datasets: [
      {
        label: "Price Over Time",
        data: history.map(h => h.price)
      }
    ]
  } : null;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Price Monitoring Dashboard</h1>

      <h2>Total Products: {summary.total_products}</h2>

      <h3>Products by Source</h3>
      <pre>{JSON.stringify(summary.products_by_source, null, 2)}</pre>

      <h3>Average Price by Category</h3>
      <pre>{JSON.stringify(summary.avg_price_by_category, null, 2)}</pre>

      <h2>Product List</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Brand</th>
            <th>Model</th>
            <th>Category</th>
            <th>Source</th>
            <th>Latest Price</th>
            <th>History</th>
          </tr>
        </thead>

        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.brand}</td>
              <td>{p.model}</td>
              <td>{p.category}</td>
              <td>{p.source}</td>
              <td>${p.latest_price}</td>
              <td>
                <button onClick={() => loadHistory(p.id)}>
                  View History
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {chartData && (
        <>
          <h2>Price History Chart</h2>
          <Line data={chartData} />
        </>
      )}

    </div>
  );
}

export default App;