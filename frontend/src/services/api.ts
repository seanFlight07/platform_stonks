import type {
  Company,
  CompanySearchResult,
} from "../types/company";

import type { Price } from "../types/price";

const API_URL = "http://localhost:8000";

async function getErrorMessage(response: Response) {
  const data = await response.json();
  return data.detail ?? "Request failed";
}

export async function getCompanies(): Promise<Company[]> {
  const response = await fetch(`${API_URL}/companies`);

  if (!response.ok) {
    throw new Error("Failed to fetch companies");
  }

  return response.json();
}

export async function getPrices(code: string): Promise<Price[]> {
  const response = await fetch(
    `${API_URL}/companies/${code}/prices`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch company prices");
  }

  return response.json();
}

export async function searchCompany(
  code: string,
  exchange: string,
  token: string | null
): Promise<CompanySearchResult> {
  const response = await fetch(
    `${API_URL}/companie-search/${code}.${exchange}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  return response.json();
}

export async function addCompany(
  company: CompanySearchResult,
  token: string | null
): Promise<string> {
  const response = await fetch(
    `${API_URL}/companies/load/?code=${company.code}&exchange=${company.exchange}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  const data = await response.json();
  return data.detail;
}

export async function createUser(
  email: string,
  password: string,
  token: string | null
): Promise<string> {
  const response = await fetch(
    `${API_URL}/user/create-user`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        email,
        password,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(await getErrorMessage(response));
  }

  const data = await response.json();
  return data.detail;
}
