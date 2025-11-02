import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [explanation, setExplanation] = useState('');
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [apiStatus, setApiStatus] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  useEffect(() => {
    // Check API status on mount
    axios.get('/api/status')
      .then(response => setApiStatus(response.data))
      .catch(error => console.error('Status check failed:', error));
  }, []);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResults(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data);
    } catch (error) {
      alert(error.response?.data?.error || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const handleTransactionClick = async (transaction) => {
    setSelectedTransaction(transaction);
    setShowModal(true);
    setExplanation('');
    setLoadingExplanation(true);

    try {
      const response = await axios.post('/api/explain', transaction);
      setExplanation(response.data.explanation);
    } catch (error) {
      setExplanation('Error generating explanation. Please try again.');
    } finally {
      setLoadingExplanation(false);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedTransaction(null);
    setExplanation('');
  };

  const getRiskLevel = (score) => {
    if (score >= 0.8) return { level: 'Critical', color: '#BB0A21' };
    if (score >= 0.6) return { level: 'High', color: '#E63946' };
    if (score >= 0.4) return { level: 'Medium', color: '#F77F00' };
    return { level: 'Low', color: '#06A77D' };
  };

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortedTransactions = () => {
    if (!results || !results.fraudulent_transactions) return [];
    
    const transactions = [...results.fraudulent_transactions];
    
    if (sortConfig.key) {
      transactions.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];
        
        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    
    return transactions;
  };

  const getSortIcon = (key) => {
    if (sortConfig.key !== key) {
      return '↕️';
    }
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  const getTopSuspiciousAccounts = () => {
    if (!results || !results.fraudulent_transactions) return [];
    
    const accountScores = {};
    results.fraudulent_transactions.forEach(transaction => {
      // Use AccountID if available, otherwise fall back to TransactionID
      const id = transaction.AccountID || transaction.TransactionID || `TXN${String(transaction.id + 1).padStart(4, '0')}`;
      if (!accountScores[id]) {
        accountScores[id] = {
          id: id,
          totalScore: 0,
          count: 0,
          avgScore: 0,
          maxScore: 0,
          transactions: []
        };
      }
      accountScores[id].totalScore += transaction.fraud_score;
      accountScores[id].count += 1;
      accountScores[id].avgScore = accountScores[id].totalScore / accountScores[id].count;
      accountScores[id].maxScore = Math.max(accountScores[id].maxScore, transaction.fraud_score);
      accountScores[id].transactions.push(transaction.TransactionID || `TXN${String(transaction.id + 1).padStart(4, '0')}`);
    });
    
    // Sort by average score (descending), then by count (descending), then by ID (ascending)
    return Object.values(accountScores)
      .sort((a, b) => {
        if (Math.abs(b.avgScore - a.avgScore) > 0.001) {
          return b.avgScore - a.avgScore;
        }
        if (b.count !== a.count) {
          return b.count - a.count;
        }
        return a.id.localeCompare(b.id);
      })
      .slice(0, 5);
  };

  const getRiskDistribution = () => {
    if (!results || !results.fraudulent_transactions) return { critical: 0, high: 0, medium: 0, low: 0 };
    
    const distribution = { critical: 0, high: 0, medium: 0, low: 0 };
    results.fraudulent_transactions.forEach(transaction => {
      const risk = getRiskLevel(transaction.fraud_score);
      if (risk.level === 'Critical') distribution.critical++;
      else if (risk.level === 'High') distribution.high++;
      else if (risk.level === 'Medium') distribution.medium++;
      else distribution.low++;
    });
    
    return distribution;
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo">CIMB</div>
            <div className="header-divider"></div>
            <h1>Anti-Scam Dashboard</h1>
          </div>
          {apiStatus && (
            <div className="status-badge">
              {apiStatus.mock_mode ? (
                <span className="badge badge-warning">🧪 Mock Mode</span>
              ) : (
                <span className="badge badge-success">✓ Live</span>
              )}
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Upload Section */}
        <div className="upload-section">
          <div className="upload-card">
            <h2>Upload Transaction Data</h2>
            <p className="upload-description">
              Upload an Excel or CSV file containing transaction records for fraud analysis
            </p>
            
            <div className="file-input-wrapper">
              <input
                type="file"
                id="file-upload"
                accept=".xlsx,.xls,.csv"
                onChange={handleFileChange}
                className="file-input"
              />
              <label htmlFor="file-upload" className="file-label">
                {file ? (
                  <>
                    <span className="file-icon">📄</span>
                    <span className="file-name">{file.name}</span>
                  </>
                ) : (
                  <>
                    <span className="file-icon">📁</span>
                    <span>Choose Excel or CSV File</span>
                  </>
                )}
              </label>
            </div>

            <button
              className="btn btn-primary"
              onClick={handleUpload}
              disabled={!file || loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                'Analyze Transactions'
              )}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results && (
          <div className="results-section">
            {/* Summary Cards */}
            <div className="summary-cards">
              <div className="summary-card">
                <div className="summary-icon">📊</div>
                <div className="summary-content">
                  <div className="summary-value">{results.total_transactions}</div>
                  <div className="summary-label">Total Transactions</div>
                </div>
              </div>
              
              <div className="summary-card alert">
                <div className="summary-icon">🚨</div>
                <div className="summary-content">
                  <div className="summary-value">{results.fraudulent_count}</div>
                  <div className="summary-label">Fraudulent Detected</div>
                </div>
              </div>
              
              <div className="summary-card">
                <div className="summary-icon">✓</div>
                <div className="summary-content">
                  <div className="summary-value">
                    {results.total_transactions - results.fraudulent_count}
                  </div>
                  <div className="summary-label">Legitimate</div>
                </div>
              </div>
            </div>

            {/* Fraudulent Transactions Table */}
            {results.fraudulent_count > 0 ? (
              <>
                {/* Analytics Graphs */}
                <div className="analytics-section">
                  <div className="analytics-card">
                    <h3>🎯 Top 5 Most Suspicious Accounts</h3>
                    <div className="chart-container">
                      {getTopSuspiciousAccounts().map((account, index) => (
                        <div key={account.id} className="chart-bar">
                          <div className="chart-label">
                            <span className="rank">#{index + 1}</span>
                            <span className="account-id">{account.id}</span>
                            <span className="transaction-count">
                              ({account.count} transaction{account.count > 1 ? 's' : ''})
                            </span>
                          </div>
                          <div className="bar-wrapper">
                            <div 
                              className="bar-fill" 
                              style={{ 
                                width: `${account.avgScore * 100}%`,
                                backgroundColor: getRiskLevel(account.avgScore).color
                              }}
                              title={`Transactions: ${account.transactions.join(', ')}`}
                            >
                              <span className="bar-label">{(account.avgScore * 100).toFixed(1)}%</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="analytics-card">
                    <h3>📊 Risk Level Distribution</h3>
                    <div className="risk-distribution">
                      {Object.entries(getRiskDistribution()).map(([level, count]) => {
                        const levelConfig = {
                          critical: { label: 'Critical', color: '#BB0A21' },
                          high: { label: 'High', color: '#E63946' },
                          medium: { label: 'Medium', color: '#F77F00' },
                          low: { label: 'Low', color: '#06A77D' }
                        };
                        const config = levelConfig[level];
                        const percentage = results.fraudulent_count > 0 
                          ? (count / results.fraudulent_count * 100).toFixed(1) 
                          : 0;
                        
                        return count > 0 ? (
                          <div key={level} className="risk-item">
                            <div className="risk-header">
                              <span className="risk-label" style={{ color: config.color }}>
                                {config.label}
                              </span>
                              <span className="risk-count">{count}</span>
                            </div>
                            <div className="risk-bar-wrapper">
                              <div 
                                className="risk-bar-fill" 
                                style={{ 
                                  width: `${percentage}%`,
                                  backgroundColor: config.color
                                }}
                              />
                            </div>
                            <div className="risk-percentage">{percentage}%</div>
                          </div>
                        ) : null;
                      })}
                    </div>
                  </div>
                </div>

                <div className="transactions-card">
                  <h2>🚨 Fraudulent Transactions</h2>
                  <p className="transactions-subtitle">
                    Click on any transaction to view detailed fraud analysis. Click column headers to sort.
                  </p>
                  
                  <div className="table-container">
                    <table className="transactions-table">
                      <thead>
                        <tr>
                          <th onClick={() => handleSort('AccountID')} className="sortable">
                            Account ID {getSortIcon('AccountID')}
                          </th>
                          <th onClick={() => handleSort('TransactionID')} className="sortable">
                            Transaction ID {getSortIcon('TransactionID')}
                          </th>
                          <th onClick={() => handleSort('TransactionAmount')} className="sortable">
                            Amount (RM) {getSortIcon('TransactionAmount')}
                          </th>
                          <th onClick={() => handleSort('TransactionDuration')} className="sortable">
                            Duration (s) {getSortIcon('TransactionDuration')}
                          </th>
                          <th onClick={() => handleSort('LoginAttempts')} className="sortable">
                            Login Attempts {getSortIcon('LoginAttempts')}
                          </th>
                          <th onClick={() => handleSort('AccountBalance')} className="sortable">
                            Balance (RM) {getSortIcon('AccountBalance')}
                          </th>
                          <th onClick={() => handleSort('CustomerAge')} className="sortable">
                            Age {getSortIcon('CustomerAge')}
                          </th>
                          <th onClick={() => handleSort('fraud_score')} className="sortable">
                            Risk Score {getSortIcon('fraud_score')}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {getSortedTransactions().map((transaction) => {
                          const risk = getRiskLevel(transaction.fraud_score);
                          const displayTransactionId = transaction.TransactionID || `TXN${String(transaction.id + 1).padStart(4, '0')}`;
                          const displayAccountId = transaction.AccountID || displayTransactionId;
                          return (
                            <tr
                              key={transaction.id}
                              onClick={() => handleTransactionClick(transaction)}
                              className="transaction-row"
                            >
                              <td className="account-id">{displayAccountId}</td>
                              <td className="transaction-id">{displayTransactionId}</td>
                              <td className="amount">
                                {transaction.TransactionAmount.toLocaleString('en-MY', {
                                  minimumFractionDigits: 2,
                                  maximumFractionDigits: 2
                                })}
                              </td>
                              <td>{transaction.TransactionDuration}</td>
                              <td className="login-attempts">
                                {transaction.LoginAttempts}
                              </td>
                              <td>
                                {transaction.AccountBalance.toLocaleString('en-MY', {
                                  minimumFractionDigits: 2,
                                  maximumFractionDigits: 2
                                })}
                              </td>
                              <td>{transaction.CustomerAge}</td>
                              <td>
                                <div className="risk-score">
                                  <span
                                    className="risk-badge"
                                    style={{ backgroundColor: risk.color }}
                                    title={risk.level}
                                  >
                                    {(transaction.fraud_score * 100).toFixed(1)}%
                                  </span>
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            ) : (
              <div className="no-fraud-card">
                <div className="success-icon">✓</div>
                <h3>No Fraudulent Transactions Detected</h3>
                <p>All transactions appear legitimate</p>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Fraud Analysis</h2>
              <button className="close-btn" onClick={closeModal}>×</button>
            </div>
            
            <div className="modal-content">
              {selectedTransaction && (
                <>
                  <div className="transaction-details">
                    <h3>Transaction Details</h3>
                    <div className="details-grid">
                      <div className="detail-item">
                        <span className="detail-label">Account ID:</span>
                        <span className="detail-value">
                          {selectedTransaction.AccountID || selectedTransaction.TransactionID || `TXN${String(selectedTransaction.id + 1).padStart(4, '0')}`}
                        </span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Transaction ID:</span>
                        <span className="detail-value">
                          {selectedTransaction.TransactionID || `TXN${String(selectedTransaction.id + 1).padStart(4, '0')}`}
                        </span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Amount:</span>
                        <span className="detail-value amount">
                          RM {selectedTransaction.TransactionAmount.toLocaleString('en-MY', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                          })}
                        </span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Duration:</span>
                        <span className="detail-value">
                          {selectedTransaction.TransactionDuration}s
                        </span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Login Attempts:</span>
                        <span className="detail-value">
                          {selectedTransaction.LoginAttempts}
                        </span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Account Balance:</span>
                        <span className="detail-value">
                          RM {selectedTransaction.AccountBalance.toLocaleString('en-MY', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                          })}
                        </span>
                      </div>
                      <div className="detail-item">
                        <span className="detail-label">Customer Age:</span>
                        <span className="detail-value">
                          {selectedTransaction.CustomerAge}
                        </span>
                      </div>
                    </div>
                    
                    <div className="fraud-score-display">
                      <span className="detail-label">Risk Score:</span>
                      <span
                        className="score-badge"
                        style={{
                          backgroundColor: getRiskLevel(selectedTransaction.fraud_score).color
                        }}
                      >
                        {(selectedTransaction.fraud_score * 100).toFixed(2)}% - {getRiskLevel(selectedTransaction.fraud_score).level} Risk
                      </span>
                    </div>
                  </div>

                  <div className="explanation-section">
                    <h3>AI Analysis</h3>
                    {loadingExplanation ? (
                      <div className="loading-explanation">
                        <span className="spinner"></span>
                        <span>Generating fraud analysis...</span>
                      </div>
                    ) : (
                      <div className="explanation-text markdown-content">
                        <ReactMarkdown>{explanation}</ReactMarkdown>
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <p>Built for CIMB × Microsoft Hackathon | Fraud Detection Dashboard</p>
      </footer>
    </div>
  );
}

export default App;
