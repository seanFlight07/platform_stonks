import type { Price } from "../types/price";
import {LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer} from "recharts"

interface PriceChartProps {
  prices: Price[]
}

function PriceChart({prices}:PriceChartProps){
  const chartData = [...prices].reverse()

  return (
  <section>
    <h2>Price History</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <XAxis dataKey="date"/>
          <YAxis />
          <Tooltip />
          <Line dataKey="close" dot={false} />
        </LineChart>
      </ResponsiveContainer>
  </section>
  )
}
export default PriceChart
