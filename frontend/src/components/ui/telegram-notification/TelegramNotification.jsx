import React, { useState } from 'react';
import TelegramIcon from '@/assets/icons/telegram_dashboard.svg?react';
import { ActionModal } from '@/components/ui/action-modal';
import { Button } from '@/components/ui/custom-button/Button';
import useTelegramNotification from '@/hooks/useTelegramNotification';
import { useWalletStore } from '@/stores/useWalletStore';

export function TelegramNotification({ telegramId }) {
  const [showModal, setShowModal] = useState(false);
  const { walletId } = useWalletStore();
  const { subscribe } = useTelegramNotification();

  const handleOpen = () => setShowModal(true);
  const handleClose = () => setShowModal(false);
  const handleSubscribe = () => {
    subscribe({ telegramId, walletId });
    handleClose();
  };

  return (
    <div className="hidden md:flex">
      <Button
        variant="secondary"
        size="lg"
        className="w-full max-w-[642px] h-[60px]  md:flex items-center justify-center gap-2"
        onClick={handleOpen}
      >
        <span className="flex items-center justify-center gap-2">
          <TelegramIcon className="w-6 h-6" />
          Enable telegram notification bot
        </span>
      </Button>
      {showModal && (
        <ActionModal
          isOpen={showModal}
          title="Telegram Notification"
          subTitle="Do you want to enable telegram notification bot?"
          content={[
            'This will allow you to receive quick notifications on your telegram line in realtime. You can disable this setting anytime.',
          ]}
          cancelLabel="Cancel"
          submitLabel="Yes, Sure"
          submitAction={handleSubscribe}
          cancelAction={handleClose}
        />
      )}
    </div>
  );
}
