import type { Price } from "../types/price";
import {LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid} from "recharts"

interface PriceChartProps {
  prices: Price[]
}

function formatDate(value: string) {
  return new Date(value).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short"
  })
}
function PriceChart({prices}:PriceChartProps){
  const chartData = [...prices].reverse()

  return (
  <section className="card .chart-card">
    <h2>Price History</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" minTickGap={40} tickFormatter={formatDate} />
          <YAxis domain={["auto", "auto"]} tickFormatter={(value) => `$${value}`} />
          <Tooltip />
          <Line dataKey="close" dot={false} type="monotone" name="Close"/>
        </LineChart>
      </ResponsiveContainer>
  </section>
  )
}
export default PriceChart
