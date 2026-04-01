import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

function App() {

  const [summary, setSummary] = useState(null);
  const [products, setProducts] = useState([]);
  const [history, setHistory] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);

  /*
    Stable headers object
  */
  const headers = useMemo(() => ({
    "x-api-key": process.env.REACT_APP_API_KEY
  }), []);

  /*
    Initial dashboard load
  */
  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/analytics/summary", { headers })
      .then(res => setSummary(res.data));

    axios
      .get("http://127.0.0.1:8000/products?page=1&limit=20", { headers })
      .then(res => setProducts(res.data.data));

  }, [headers]);


  /*
    Load price history for chart
  */
  const loadHistory = (productId, brand, model) => {

    setSelectedProduct(`${brand} ${model}`);

    axios
      .get(
        `http://127.0.0.1:8000/products/${productId}/history`,
        { headers }
      )
      .then(res => setHistory(res.data.history));

  };


  /*
    Detect price trend indicator
  */
  const getPriceTrend = (product) => {

    if (!product.previous_price) {
      return "—";
    }

    if (product.latest_price > product.previous_price) {
      return "▲";
    }

    if (product.latest_price < product.previous_price) {
      return "▼";
    }

    return "—";
  };


  /*
    Loading state
  */
  if (!summary) {
    return <div style={{ padding: 20 }}>Loading dashboard...</div>;
  }


  /*
    Chart formatting
  */
  const chartData = history ? {
    labels: history.map(h =>
      new Date(h.recorded_at).toLocaleDateString()
    ),
    datasets: [
      {
        label: "Price Over Time",
        data: history.map(h => h.price),
        tension: 0.3
      }
    ]
  } : null;


  return (
    <div style={{ padding: 30, fontFamily: "Arial" }}>

      <h1>Price Monitoring Dashboard</h1>


      {/* KPI CARDS */}

      <div style={{
        display: "flex",
        gap: "20px",
        marginBottom: "30px"
      }}>

        <div style={cardStyle}>
          <h3>Total Products</h3>
          <p>{summary.total_products}</p>
        </div>

        <div style={cardStyle}>
          <h3>Sources Covered</h3>
          <p>{Object.keys(summary.products_by_source).length}</p>
        </div>

        <div style={cardStyle}>
          <h3>Categories</h3>
          <p>{Object.keys(summary.avg_price_by_category).length}</p>
        </div>

      </div>


      {/* SOURCE BREAKDOWN */}

      <h2>Products by Source</h2>

      <ul>
        {Object.entries(summary.products_by_source).map(
          ([source, count]) => (
            <li key={source}>
              {source}: {count}
            </li>
          )
        )}
      </ul>


      {/* CATEGORY PRICE SUMMARY */}

      <h2>Average Price by Category</h2>

      <ul>
        {Object.entries(summary.avg_price_by_category).map(
          ([category, price]) => (
            <li key={category}>
              {category}: ${price.toFixed(2)}
            </li>
          )
        )}
      </ul>


      {/* PRODUCT TABLE */}

      <h2 style={{ marginTop: 40 }}>Product List</h2>

      <table
        border="1"
        cellPadding="10"
        style={{
          borderCollapse: "collapse",
          width: "100%"
        }}
      >

        <thead>
          <tr>
            <th>Brand</th>
            <th>Model</th>
            <th>Category</th>
            <th>Source</th>
            <th>Latest Price</th>
            <th>Trend</th>
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

              <td style={{
                fontSize: "20px",
                color:
                  getPriceTrend(p) === "▲"
                    ? "green"
                    : getPriceTrend(p) === "▼"
                    ? "red"
                    : "gray"
              }}>
                {getPriceTrend(p)}
              </td>

              <td>
                <button
                  onClick={() =>
                    loadHistory(p.id, p.brand, p.model)
                  }
                >
                  View History
                </button>
              </td>

            </tr>

          ))}

        </tbody>

      </table>


      {/* HISTORY CHART */}

      {chartData && (

        <div style={{ marginTop: 50 }}>

          <h2>
            Price History: {selectedProduct}
          </h2>

          <Line data={chartData} />

        </div>

      )}

    </div>
  );
}


/*
  KPI card styling
*/

const cardStyle = {
  padding: "20px",
  borderRadius: "10px",
  border: "1px solid #ddd",
  minWidth: "180px",
  textAlign: "center",
  boxShadow: "0px 2px 6px rgba(0,0,0,0.05)"
};


export default App;