import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <nav className="navbar navbar-expand-lg navbar-light" style={{ background: 'white', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
      <div className="container">
        <Link className="navbar-brand fw-bold" to="/" style={{ color: '#667eea' }}>
          AI Interview System
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/">
                Dashboard
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/interview">
                Interview
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/coding">
                Coding
              </Link>
            </li>
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                {user.full_name}
              </a>
              <ul className="dropdown-menu">
                <li><span className="dropdown-item-text">{user.email}</span></li>
                <li><hr className="dropdown-divider" /></li>
                <li><button className="dropdown-item" onClick={logout}>Logout</button></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
