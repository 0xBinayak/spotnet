import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ReactComponent as Star } from 'assets/particles/star.svg';
import { ReactComponent as CollateralIcon } from 'assets/icons/collateral.svg';
import { ReactComponent as EthIcon } from 'assets/icons/ethereum.svg';
import { ReactComponent as UsdIcon } from 'assets/icons/usd_coin.svg';
import { ReactComponent as BorrowIcon } from 'assets/icons/borrow.svg';
import { ReactComponent as StrkIcon } from 'assets/icons/strk.svg';
import { closePosition } from 'utils/transaction';
import { ZETH_ADDRESS } from 'utils/constants';
import Spinner from 'components/spinner/Spinner';
import './dashboard.css';

const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://0.0.0.0:8000';

const fetchCardData = async ({ walletId }) => {
  if (!walletId) {
    console.error('fetchCardData: walletId is undefined');
    return null;
  }
  try {
    const response = await axios.get(`${backendUrl}/api/dashboard?wallet_id=${walletId}`);
    return response.data;
  } catch (error) {
    console.error('Error during getting the data from API', error);
    return null;
  }
};

const DashboardCard = ({ card }) => (
  <div className="card card-custom-styles d-flex flex-column align-item-center card-shadow">
    <header className="card-header bg-custom-color text-light text-center">
      <div className="d-flex align-items-center justify-content-center">
        <card.icon className="card-icons" />
        <h2 className="ms-2 icon-text-gap mb-0 text-style" style={{
          color: card.title === 'Borrow' ? 'var(--borrow-color)' : 'var(--collateral-color)',
        }}>
          {card.title}
        </h2>
      </div>
    </header>
    <div className="card-body card-body-custom">
      <div className="d-flex flex-column align-items-center bg-custom-color rounded p-3">
        <div className="d-flex align-items-center mb-3">
          <card.currencyIcon className="card-icons" />
          <span className="ms-2 icon-text-gap text-style">{card.currencyName}</span>
        </div>
        <div className="d-flex align-items-center">
          <span className="dashboard-text-color balance-text-size">Balance:</span>
          <span className="ms-2 icon-text-gap text-style" style={{
            color: card.title === 'Borrow' ? 'var(--borrow-color)' : 'var(--collateral-color)',
          }}>
            {card.balance}
          </span>
        </div>
      </div>
    </div>
  </div>
);

const Dashboard = ({ walletId }) => {
  const [cardData, setCardData] = useState([
    {
      title: 'Collateral & Earnings',
      icon: CollateralIcon,
      balance: '0.00',
      currencyName: 'Ethereum',
      currencyIcon: EthIcon,
    },
    {
      title: 'Borrow',
      icon: BorrowIcon,
      balance: '0.00',
      currencyName: 'USD Coin',
      currencyIcon: UsdIcon,
    },
  ]);
  const [healthFactor, setHealthFactor] = useState('0.00');
  const [loading, setLoading] = useState(true);

  const starData = [
    { top: 1, left: 0, size: 1.5 },
    { top: 75, left: 35, size: 2.5 },
    { top: -2, left: 94, size: 5.5 },
  ];

  const closePositionEvent = async () => {
    if (!walletId) {
      console.error('closePositionEvent: walletId is undefined');
      return;
    }
    try {
      const response = await axios.get(`${backendUrl}/api/get-repay-data?supply_token=ETH&wallet_id=${walletId}`);
      await closePosition(response.data);
      await axios.get(`${backendUrl}/api/close-position?position_id=${response.data.position_id}`);
    } catch (e) {
      console.error('Error during closePositionEvent', e);
    }
  };

  useEffect(() => {
    const getData = async () => {
      if (!walletId) {
        console.error('getData: walletId is undefined');
        setLoading(false);
        return;
      }

      const data = await fetchCardData({ walletId });
      if (data && data.zklend_position && data.zklend_position.products) {
        const positions = data.zklend_position.products[0].positions || [];
        const healthRatio = data.zklend_position.products[0].health_ratio;
        console.log('Positions:', positions);

        const cardData = positions.map((position, index) => {
          const isFirstCard = index === 0;
          const tokenAddress = position.tokenAddress;

          if (isFirstCard) {
            const isEthereum = tokenAddress === ZETH_ADDRESS;
            return {
              title: 'Collateral & Earnings',
              icon: CollateralIcon,
              balance: position.totalBalances[Object.keys(position.totalBalances)[0]],
              currencyName: isEthereum ? 'Ethereum' : 'STRK',
              currencyIcon: isEthereum ? EthIcon : StrkIcon,
            };
          }

          return {
            title: 'Borrow',
            icon: BorrowIcon,
            balance: position.totalBalances[Object.keys(position.totalBalances)[0]],
            currencyName: 'USD Coin',
            currencyIcon: UsdIcon,
          };
        });

        setCardData(cardData);
        setHealthFactor(healthRatio);
      } else {
        console.error('Data is missing or incorrectly formatted');
      }
      setLoading(false);
    };

    getData();
  }, [walletId]);

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-container container">
        {loading && <Spinner loading={loading} />}

        {starData.map((star, index) => (
          <Star
            key={index}
            className="dashboard-star"
            style={{
              '--star-top': `${star.top}%`,
              '--star-left': `${star.left}%`,
              '--star-size': `${star.size}%`,
            }}
          />
        ))}
        
        <div className="background-effects">
          <div className="background-gradient"></div>
          <div className="background-gradient"></div>
        </div>

        <h1 className="text-white text-center zkLend-text">zkLend Position</h1>

        <div className="health-factor-wrapper">
          <div className="card card-health-factor mx-auto d-flex flex-column align-items-center justify-content-center card-shadow">
            <div className="bg-custom-health d-flex align-items-center rounded bg-card-health">
              <span className="dashboard-text-color health-text-size">Health factor:</span>
              <span className="text-white text-style">{healthFactor}</span>
            </div>
          </div>
        </div>

        <div className="dashboard-cards">
          {cardData.map((card, index) => (
            <DashboardCard key={index} card={card} index={index} />
          ))}
        </div>

        <div className="redeem-button-wrapper">
          <button className="btn redeem-btn border-0" onClick={closePositionEvent}>
            Redeem
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;