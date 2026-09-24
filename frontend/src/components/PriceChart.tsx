import type { Price } from "../types/price";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

interface PriceChartProps {
  prices: Price[];
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
  });
}

function PriceChart({ prices }: PriceChartProps) {
  if (prices.length === 0) {
    return null;
  }

  const chartData = [...prices].reverse();

  return (
    <section className="card chart-card">
      <div className="chart-header">
        <div>
          <h2>Price History</h2>
          <p>Closing price over the last two years.</p>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="date"
              minTickGap={40}
              tickFormatter={formatDate}
            />

            <YAxis
              domain={["auto", "auto"]}
              tickFormatter={(value) => `$${value}`}
            />

            <Tooltip
              labelFormatter={(value) => formatDate(String(value))}
              formatter={(value) => [
                `$${Number(value).toFixed(2)}`,
                "Close",
              ]}
            />

            <Line
              dataKey="close"
              dot={false}
              type="monotone"
              name="Close"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default PriceChart;
