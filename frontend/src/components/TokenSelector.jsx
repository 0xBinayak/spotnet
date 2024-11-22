import React from 'react';
import { ReactComponent as ETH } from 'assets/icons/ethereum.svg';
import { ReactComponent as USDC } from 'assets/icons/borrow_usdc.svg';
import { ReactComponent as STRK } from 'assets/icons/strk.svg';
import { ReactComponent as DAI } from 'assets/icons/dai.svg';
import { useMatchMedia } from 'hooks/useMatchMedia';
import StarMaker from './StarMaker';

const Tokens = [
  { id: 'ethOption', component: <ETH />, label: 'ETH' },
  { id: 'usdcOption', component: <USDC />, label: 'USDC' },
  { id: 'strkOption', component: <STRK />, label: 'STRK' },
  { id: 'daiOption', component: <DAI />, label: 'DAI' },
];
const starData = [
  { top: 43, left: 28, size: 7 },
];


const TokenSelector = ({ setSelectedToken }) => {
  const isMobile = useMatchMedia('(max-width: 768px)');
  
  return <div className='form-token'>
    {Tokens.map((token) => (
      <div className='token-card' key={token.id}>
        <div className="token-container">
        <input
          type='radio'
          id={token.id}
          name='token-options'
          value={token.label}
          onChange={() => setSelectedToken(token.label)}
        />
          <label htmlFor={token.id}>
            <h5>
              <span className="token-icon">{token.component}</span> {token.label}
            </h5>
          </label>
          { isMobile && <StarMaker starData={starData} />}
        </div>
      </div>
    ))}
  </div>
};

export default TokenSelector;
