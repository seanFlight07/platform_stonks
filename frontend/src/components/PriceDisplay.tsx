import type { Price } from "../types/price";

interface PriceDisplayProps {
  prices: Price[]
}

function PriceDisplay({prices}: PriceDisplayProps){
  if (prices.length === 0){
    return <p>No data has been loaded.</p>
  }
  const latestPrice = prices[0]

  return (
    <>
    <p> Date: {latestPrice.date}</p>
    <p> Open: ${latestPrice.open} </p>
    <p> High: ${latestPrice.high}</p>
    <p> Low: ${latestPrice.low}</p>
    <p> Close: ${latestPrice.close}</p>
    <p> Change $: ${latestPrice.change_dollar}</p>
    <p> Change %: {latestPrice.change_pct}%</p>
    <p> Volume: {latestPrice.volume}</p>
  </>
  )

}

export default PriceDisplay
