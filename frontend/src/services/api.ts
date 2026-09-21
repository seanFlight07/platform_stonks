import type {Company} from "../types/company"
import type { Price } from "../types/price"

const API_URL = "http://localhost:8000"

export async function getCompanies(): Promise<Company[]>{
  const response = await fetch(`${API_URL}/companies`)

  if(!response.ok){
    throw new Error("Failed to fetch companies")
  }
  const data: Company[] = await response.json()
  return data
}

export async function getPrices(code: string): Promise<Price[]>{
  const response = await fetch(`${API_URL}/companies/${code}/prices`)

  if(!response.ok){
    throw new Error("Failed to fetch company prices")
  }

  const data: Price[] = await response.json()
  return data
}
