import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <h1>Waterloo CS Assignment Hub</h1>
        </Link>
        <div className="nav-links">
          {user ? (
            <>
              <Link to="/courses">Courses</Link>
              <span className="user-info">
                {user.username} ({user.identity})
              </span>
              <button onClick={logout} className="btn btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/signup">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};
