import type {Company} from "../types/company"

const API_URL = "http://localhost:8000"

export async function getCompanies(): Promise<Company[]>{
  const response = await fetch(`${API_URL}/companies`)

  if(!response.ok){
    throw new Error("Failed to fetch companies")
  }
  const data: Company[] = await response.json()
  return data
}
