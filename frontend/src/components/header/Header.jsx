import React from 'react';
import './header.css'
import { ReactComponent as Logo } from "../../assets/images/logo.svg";
import { Link } from 'react-router-dom';
import TelegramLogin from '../Telegram/TelegramLogin';

function Header({ walletId, onConnectWallet, onLogout, tgUser, setTgUser }) {
  return (
      <nav>
          <div className='list-items'>
              <div className='logo'>
                <Link to="/">
                    <Logo/>
                </Link>
              </div>
              <div className='nav-items'>
                  <a href="/">Home</a>
                  <Link to="/dashboard">Dashboard</Link>
              </div>
              <div className='wallet-section'>
                <TelegramLogin user={tgUser} onLogin={setTgUser} />
                  {walletId ? (
                      <div className='wallet-container'>
                          <div className='wallet-id'>
                              {`${walletId.slice(0, 4)}...${walletId.slice(-4)}`}
                          </div>
                          <button className='gradient-button'
                              onClick={onLogout}
                          >
                              Log Out
                          </button>
                      </div>
                  ) : (
                      <button className='gradient-button'
                          onClick={onConnectWallet}
                      >
                          <span>Connect Wallet</span>
                      </button>
                  )}
              </div>
          </div>
      </nav>
  );
}

export default Header;
