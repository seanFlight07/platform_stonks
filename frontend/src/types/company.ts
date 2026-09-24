export interface Company{
  code: string
  name: string
  exchange: string
  active: boolean
}

export interface CompanySearchResult {
  code: string;
  exchange: string;
  long_name: string;
  sector: string;
  timezone: string;
  open: number;
  day_high: number;
  day_low: number;
  previous_close: number;
}
