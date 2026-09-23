import {useState} from 'react';
import { useAuth } from '../context/AuthContext';


function AddCompany() {
  const [code, setCode] = useState("");
  const [exchange, setExchange] = useState("");
  const [company, setCompany] = useState<Company | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>){
    event.preventDefault();
    setMessage("");
    setError("");
    setCompany(null);
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/companie-search/${code}.${exchange}`,
        {
          method: "POST",
          headers:{
            Authorization: `Bearer ${token}`,
          },
        });
      const data = await response.json();
    
      if (!response.ok){
        setError(data.detail);
        return;
      }
    setCompany(data);

    }catch{
      setError("Unable to connect to server");
    }finally{
      setLoading(false);
    }
  }

  async function handleAddCompany(){
    if(!company){
      return;
    }
    setMessage("");
    setError("");
    setLoading(true);
    try{
      const response = await fetch(
        `http://localhost:8000/companies/load/?code=${company.code}&exchange=${company.exchange}`,
        {method: "POST",}
      );
      const data = await response.json();
    
      if(!response.ok){
        setError(data.detail);
        return;
      }
      setMessage(data.detail);
    }catch {
      setError("Unable to connect to server");
    }finally{
      setLoading(false);
    }
  }


interface Company {
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


  return (
    <div>
      <h2>Add Company</h2>

      <form onSubmit={handleSubmit}>
        <label>
          Company code
          <input type="text" 
          value={code}
          onChange={(event) => setCode(event.target.value)}
          />
        </label>

        <label>
          Exchange
          <input type="text" 
          value={exchange}
          onChange={(event) => setExchange(event.target.value)}/>
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Searching...": "Search"}
        </button>
      </form>
      {company && (
      <div>
        <h3>{company.long_name}</h3>
          <p>{company.code}.{company.exchange}</p>
          <p>Sector: {company.sector}</p>
          <p>Previous close: {company.previous_close}</p>
          
          <button type='button' onClick={handleAddCompany} disabled={loading}>
            {loading ? "Adding...": "Add Company"}
          </button>
      </div>
      )}
      {message &&(
        <p>{message}</p>
      )}
      {error &&(
        <p>{error}</p>
      )}
    </div>
  );
}

export default AddCompany;
