import React from 'react';
import { Award, TrendingUp, Zap } from 'lucide-react';
import './SummaryCards.css';

const SummaryCards = ({ totalPoints = 0, badgeCount = 0, streakDays = 0 }) => {
  return (
    <div className="summary-cards">
      <div className="card points-card">
        <div className="card-icon">
          <Award size={32} />
        </div>
        <div className="card-content">
          <h3>Total Points</h3>
          <p className="card-value">{totalPoints}</p>
        </div>
      </div>

      <div className="card badges-card">
        <div className="card-icon">
          <TrendingUp size={32} />
        </div>
        <div className="card-content">
          <h3>Badges Earned</h3>
          <p className="card-value">{badgeCount}</p>
        </div>
      </div>

      <div className="card streak-card">
        <div className="card-icon">
          <Zap size={32} />
        </div>
        <div className="card-content">
          <h3>Current Streak</h3>
          <p className="card-value">{streakDays}</p>
          <span className="card-label">days</span>
        </div>
      </div>
    </div>
  );
};

export default SummaryCards;