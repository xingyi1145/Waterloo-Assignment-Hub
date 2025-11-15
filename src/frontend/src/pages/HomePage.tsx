import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export const HomePage = () => {
  const { user } = useAuth();

  return (
    <div className="home-container">
      <div className="hero">
        <h1>Waterloo CS Assignment Hub</h1>
        <p className="hero-subtitle">
          Practice, solve, and share programming problems from University of Waterloo CS courses
        </p>
        
        {user ? (
          <div className="hero-actions">
            <Link to="/courses" className="btn btn-primary btn-large">
              Browse Courses
            </Link>
          </div>
        ) : (
          <div className="hero-actions">
            <Link to="/signup" className="btn btn-primary btn-large">
              Get Started
            </Link>
            <Link to="/login" className="btn btn-secondary btn-large">
              Login
            </Link>
          </div>
        )}
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>📚 Course Library</h3>
          <p>Browse assignments and problems from various Waterloo CS courses</p>
        </div>
        <div className="feature-card">
          <h3>💻 Code Solutions</h3>
          <p>Submit your solutions and see how others approached the same problems</p>
        </div>
        <div className="feature-card">
          <h3>👥 Collaborate</h3>
          <p>Like and comment on solutions to learn from your peers</p>
        </div>
        <div className="feature-card">
          <h3>👨‍🏫 For Professors</h3>
          <p>Create courses, assignments, and questions for your students</p>
        </div>
      </div>
    </div>
  );
};
