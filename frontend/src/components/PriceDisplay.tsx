import type { Price } from "../types/price";

interface PriceDisplayProps {
  prices: Price[]
}

function PriceDisplay({prices}: PriceDisplayProps){
  if (prices.length === 0) {
    return (
      <section className="card empty-state">
        <p>Select a company to view its latest market data.</p>
      </section>
    );
  }
  const latestPrice = prices[0]
  const changeClass = latestPrice.change_pct >= 0 ? "positive" : "negative"
  return (
  <section className="card">
    <div className="price-header">
      <h2>Latest Price</h2>
      <span>{latestPrice.date}</span>
    </div>

    <div className="price-grid">
      <div className="metric">
        <span>Close</span>
        <strong>${latestPrice.close.toFixed(2)}</strong>
      </div>

      <div className="metric">
        <span>Change</span>
        <strong className={changeClass}>{latestPrice.change_pct.toFixed(2)}%</strong>
      </div>

      <div className="metric">
        <span>Open</span>
        <strong>${latestPrice.open.toFixed(2)}</strong>
      </div>

      <div className="metric">
        <span>High</span>
        <strong>${latestPrice.high.toFixed(2)}</strong>
      </div>

      <div className="metric">
        <span>Low</span>
        <strong>${latestPrice.low.toFixed(2)}</strong>
      </div>

      <div className="metric">
        <span>Volume</span>
        <strong>{latestPrice.volume.toLocaleString()}</strong>
      </div>
    </div>
  </section>
)
}

export default PriceDisplay
