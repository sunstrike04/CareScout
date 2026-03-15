import React, { useState } from "react";
import { INSURANCES } from "./insurances";

function App() {
  const [address, setAddress] = useState("");
  const [insurance, setInsurance] = useState("");
  const [filteredInsurances, setFilteredInsurances] = useState([]);
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // AUTOCOMPLETE HANDLER
  const handleInsuranceChange = (e) => {
    const value = e.target.value;
    setInsurance(value);

    if (value.trim() === "") {
      setFilteredInsurances([]);
      return;
    }

    // filter insurance list
    const matches = INSURANCES.filter((ins) =>
      ins.toLowerCase().includes(value.toLowerCase())
    );

    setFilteredInsurances(matches.slice(0, 8)); // show max 8 suggestions
  };

  // USER SELECTS A SUGGESTION
  const handleSelectInsurance = (name) => {
    setInsurance(name);
    setFilteredInsurances([]); // hide suggestions
  };

  // SEARCH BUTTON HANDLER
  const handleSearch = async () => {
    setResults([]);
    setIsLoading(true);

    const userInfo = [address, insurance];

    try {
      const response = await fetch("http://127.0.0.1:5000/filter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ userInfo })
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
    setIsLoading(false);
  }
};
  
  const hospitals = results?.[0] || [];
  const foundHospitalsWithInsurance = typeof results?.[1] === "boolean" ? results[1] : null;


  return (
    <div style={{ padding: "40px", maxWidth: "600px", margin: "auto" }}>
      <h1>CareScout Hospital Finder</h1>

      {/* ADDRESS INPUT */}
      <label style={{ display: "block", marginTop: "20px" }}>Enter User Address:</label>
      <input
        type="text"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="e.g. Buffalo Grove, IL"
        style={{ width: "100%", padding: "10px", marginTop: "5px" }}
      />

      {/* INSURANCE INPUT WITH AUTOCOMPLETE */}
      <label style={{ display: "block", marginTop: "20px" }}>Enter User Health Insurance:</label>
      <input
        type="text"
        value={insurance}
        onChange={handleInsuranceChange}
        placeholder="Type your insurance..."
        style={{ width: "100%", padding: "10px", marginTop: "5px" }}
      />

      {/* AUTOCOMPLETE DROPDOWN */}
      {filteredInsurances.length > 0 && (
        <div
          style={{
            border: "1px solid #ccc",
            background: "white",
            maxHeight: "160px",
            overflowY: "scroll",
            marginTop: "5px",
            borderRadius: "4px",
          }}
        >
          {filteredInsurances.map((ins, index) => (
            <div
              key={index}
              onClick={() => handleSelectInsurance(ins)}
              style={{
                padding: "10px",
                cursor: "pointer",
                borderBottom: "1px solid #eee",
              }}
            >
              {ins}
            </div>
          ))}
        </div>
      )}

      {/* SEARCH BUTTON */}
      <button
        onClick={handleSearch}
        style={{
          marginTop: "25px",
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Search Hospitals
      </button>

      {/* RESULTS */}
      <h2 style={{ marginTop: "30px" }}>Results</h2>

      {isLoading && (
        <p style={{ marginTop: "20px", fontWeight: "bold", color: "#555" }}>
          Searching hospitals...
        </p>
      )}

      {/* Message if we do NOT find hospitals accepting insurance */}
      {foundHospitalsWithInsurance === false && (
        <p style={{ marginTop: "20px", fontWeight: "bold", color: "#a00" }}>
          Could not find hospitals accepting insurance, but here are the nearest
          hospitals by location:
        </p>
      )}

      <ul>
        {hospitals.map((item, idx) => (
          <li key={idx}>
            {Array.isArray(item)
              ? `${item[0]} — ${item[1]} — ${item[2].toFixed(2)} miles`
              : JSON.stringify(item)}
          </li>
        ))}
      </ul>

    </div>
  );
}

export default App;