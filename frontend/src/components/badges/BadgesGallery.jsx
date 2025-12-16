import React from 'react';
import { Award, Zap, Target, TrendingUp } from 'lucide-react';
import './BadgesGallery.css';

const BadgeIcon = ({ type }) => {
  const icons = {
    milestone: Award,
    streak: Zap,
    achievement: Target,
    monthly: TrendingUp,
  };
  
  const Icon = icons[type] || Award;
  return <Icon size={32} />;
};

const BadgesGallery = ({ badges = [] }) => {
  // Mock data if no badges provided
  const displayBadges = badges.length > 0 ? badges : [
    { id: 1, name: 'First Step', badge_type: 'milestone', points: 10 },
    { id: 2, name: '5-Day Streak', badge_type: 'streak', points: 50 },
    { id: 3, name: 'Budget Master', badge_type: 'achievement', points: 100 },
  ];

  return (
    <div className="badges-gallery">
      <h2>🏆 Badges Earned</h2>
      <div className="badges-grid">
        {displayBadges.map((badge) => (
          <div key={badge.id} className={`badge-card ${badge.badge_type}`}>
            <div className="badge-icon">
              <BadgeIcon type={badge.badge_type} />
            </div>
            <h3>{badge.name}</h3>
            <p className="badge-points">{badge.points} pts</p>
            <span className="badge-type">{badge.badge_type}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BadgesGallery;