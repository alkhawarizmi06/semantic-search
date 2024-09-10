import React, { useState } from 'react';
import './SearchComponent.css'; 

const SearchComponent = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        try {
            const response = await fetch(`http://localhost:5001/search?query=${query}&topK=5`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setResults(data.documents);
            setError(null);
        } catch (err) {
            setError('Error fetching results');
        }
    };

    return (
        <div className="search-container">
            <h1>Search Articles</h1>
            <div>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter search query"
                />
                
                <button onClick={handleSearch}>Search</button>
            </div>

            {error && <p className="error-message">{error}</p>}

            <ul className="result-list">
                {results.map((result, index) => (
                    <li key={index}>
                        <a href={result.url} target="_blank" rel="noopener noreferrer">
                            {result.title}
                        </a>
                        <p>Score: {result.score}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchComponent;
