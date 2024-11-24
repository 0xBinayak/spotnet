import React, { useState } from 'react';
import { ReactComponent as ETH } from 'assets/icons/ethereum.svg';
import { ReactComponent as USDC } from 'assets/icons/borrow_usdc.svg';
import { ReactComponent as STRK } from 'assets/icons/strk.svg';
import { ReactComponent as DAI } from 'assets/icons/dai.svg';

const Tokens = [
  { id: 'ethOption', component: <ETH />, label: 'ETH' },
  { id: 'usdcOption', component: <USDC />, label: 'USDC' },
  { id: 'strkOption', component: <STRK />, label: 'STRK' },
  { id: 'daiOption', component: <DAI />, label: 'DAI' },
];

const TokenSelector = ({ setSelectedToken }) => {
  const [tokenSelect, setTokenSelect] = useState('STRK');
  const handleSelectedToken = (token) => {
    setTokenSelect(token);
    setSelectedToken(token);
  }
  return (
    <div className="form-token">
      {Tokens.map((token) => (
        <div className="token-card flex" key={token.id}>
          <input
            type="radio"
            id={token.id}
            name="token-options"
            value={token.label}
            onChange={() => handleSelectedToken(token.label)}
          />
          <label htmlFor={token.id} className={token.label === tokenSelect ? 'strk-token' : ''}>
            <h5>
              <span className='token'>{token.component}</span> {token.label}
            </h5>
          </label>
        </div>
      ))}
    </div>
  )
};

export default TokenSelector;