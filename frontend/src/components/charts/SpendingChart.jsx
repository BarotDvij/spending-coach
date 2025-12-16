import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './SpendingChart.css';

const SpendingChart = ({ transactions = [] }) => {
  const [timeRange, setTimeRange] = useState('1M');

  // Mock data for demo
  const mockData = [
    { date: 'Dec 1', amount: 45 },
    { date: 'Dec 3', amount: 120 },
    { date: 'Dec 5', amount: 85 },
    { date: 'Dec 7', amount: 65 },
    { date: 'Dec 10', amount: 150 },
    { date: 'Dec 12', amount: 95 },
    { date: 'Dec 15', amount: 110 },
  ];

  return (
    <div className="spending-chart">
      <div className="chart-header">
        <h2>📊 Spending Over Time</h2>
        <div className="time-range-selector">
          {['1M', '3M', '6M'].map(range => (
            <button
              key={range}
              className={timeRange === range ? 'active' : ''}
              onClick={() => setTimeRange(range)}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={mockData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" stroke="#6b7280" style={{ fontSize: '0.875rem' }} />
          <YAxis stroke="#6b7280" style={{ fontSize: '0.875rem' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '0.875rem',
            }}
            formatter={(value) => [`$${value}`, 'Amount']}
          />
          <Line
            type="monotone"
            dataKey="amount"
            stroke="#667eea"
            strokeWidth={3}
            dot={{ fill: '#667eea', r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SpendingChart;