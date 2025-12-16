import React, { useState } from 'react';
import SummaryCards from './components/dashboard/SummaryCards';
import SpendingChart from './components/charts/SpendingChart';
import './App.css';

function App() {
  const [stats] = useState({
    totalPoints: 125,
    badgeCount: 3,
    streakDays: 5
  });

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <h1>💰 Spending Coach</h1>
          <p>Track your spending, earn rewards, achieve your goals</p>
        </div>
      </header>

      <main className="app-main container">
        <SummaryCards 
          totalPoints={stats.totalPoints}
          badgeCount={stats.badgeCount}
          streakDays={stats.streakDays}
        />
        <SpendingChart />
      </main>
    </div>
  );
}

export default App;
