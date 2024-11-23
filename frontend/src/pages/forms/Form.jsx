import { useQuery } from '@tanstack/react-query';
import { ReactComponent as AlertHexagon } from 'assets/icons/alert_hexagon.svg';
import axios from 'axios';
import BalanceCards from 'components/BalanceCards';
import CardGradients from 'components/CardGradients';
import CongratulationsModal from 'components/congratulationsModal/CongratulationsModal';
import ClosePositionModal from 'components/modals/ClosePositionModal';
import MultiplierSelector from 'components/MultiplierSelector';
import Spinner from 'components/spinner/Spinner';
import StarMaker from 'components/StarMaker';
import TokenSelector from 'components/TokenSelector';
import useLockBodyScroll from 'hooks/useLockBodyScroll';
import { useState } from 'react';
import { createPortal } from 'react-dom';
import { useNavigate } from 'react-router-dom';
import { handleTransaction } from 'services/transaction';
import { connectWallet } from 'services/wallet';
import './form.css';

const Form = ({ walletId, setWalletId }) => {
  const starData = [
    { top: 35, left: 12, size: 12 },
    { top: 90, left: 7, size: 7 },
    { top: 40, left: 80, size: 7 },
    { top: 75, left: 90, size: 9 },
  ];
  const [tokenAmount, setTokenAmount] = useState('');
  const [selectedToken, setSelectedToken] = useState('');
  const [selectedMultiplier, setSelectedMultiplier] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [successful, setSuccessful] = useState(false);
  const [positionModal, setPositionModal] = useState(false);

  const { data: positionData, refetch: refetchPosition } = useQuery({
    queryKey: ['hasOpenPosition', walletId],
    queryFn: async () => {
      if (!walletId) return { has_opened_position: false };
      const { data } = await axios.get('/api/has-user-opened-position', {
        params: { wallet_id: walletId },
      });
      return data;
    },
    enabled: !!walletId,
  });

  const navigate = useNavigate();
  useLockBodyScroll(successful);

  const connectWalletHandler = async () => {
    try {
      setError(null);
      const address = await connectWallet();
      if (address) {
        setWalletId(address);
        console.log('Wallet successfully connected. Address:', address);
        return address;
      } else {
        setError('Failed to connect wallet. Please try again.');
        console.error('Wallet connection flag is false after enabling');
      }
    } catch (error) {
      console.error('Wallet connection failed:', error);
      setError('Failed to connect wallet. Please try again.');
    }
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let connectedWalletId = walletId;
    if (!connectedWalletId) {
      connectedWalletId = await connectWalletHandler();
    }

    await refetchPosition();
    if (positionData?.has_opened_position) {
      setPositionModal(true);
      return;
    }

    if (tokenAmount === '' || selectedToken === '' || selectedMultiplier === '') {
      setAlertMessage('Please fill the form');
    } else {
      setAlertMessage('');
    }

    if (connectedWalletId) {
      const formData = {
        wallet_id: connectedWalletId,
        token_symbol: selectedToken,
        amount: tokenAmount,
        multiplier: selectedMultiplier,
      };
      await handleTransaction(connectedWalletId, formData, setError, setTokenAmount, setLoading, setSuccessful);
    }
  };

  const closePosition = () => {
    setPositionModal(false);
    navigate('/dashboard');
  };

  return (
    <div className="form-container container">
      {successful && createPortal(<CongratulationsModal />, document.body)}
      {/* The rest of the UI stays largely unchanged */}
      <BalanceCards walletId={walletId} />
      <form onSubmit={handleSubmit}>
        <div className="form-wrapper">
          <div className="form-title">
            <h1>Submit your leverage details</h1>
          </div>
          {alertMessage && (
            <p className="error-message form-alert">
              {alertMessage} <AlertHexagon className="form-alert-hex" />
            </p>
          )}
          <label>Select Token</label>
          <TokenSelector setSelectedToken={setSelectedToken} />
          <h5>Select Multiplier</h5>
          <MultiplierSelector
            setSelectedMultiplier={setSelectedMultiplier}
            selectedToken={selectedToken}
            sliderValue={selectedMultiplier}
          />
          <div className="token-label">
            <label>Token Amount</label>
            {error && <p className="error-message">{error}</p>}
            <input
              type="number"
              placeholder="Enter Token Amount"
              value={tokenAmount}
              onChange={(e) => setTokenAmount(e.target.value)}
              className={error ? 'error' : ''}
            />
          </div>
          <div>
            <button type="submit" className="form-button">
              Submit
            </button>
          </div>
          <CardGradients additionalClassName={'forms-gradient'} />
          <StarMaker starData={starData} />
          <ClosePositionModal
            text={
              " You have already opened a position. Please close active position to open a new one. Click the 'Close Active Position' button to continue."
            }
            actionText={'  Do you want to open new a position?'}
            header={'Open New Position'}
            isOpen={positionModal}
            onClose={() => setPositionModal(false)}
            closePosition={closePosition}
          />
        </div>
      </form>
      <Spinner loading={loading} />
    </div>
  );
};

export default Form;
