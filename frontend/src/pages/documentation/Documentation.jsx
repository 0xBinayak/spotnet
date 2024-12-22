import React, { useEffect } from 'react';
import './documentation.css';
import ScrollButton from 'components/ui/scroll-button/ScrollButton';
import Sections from 'components/layout/sections/Sections';
import Sidebar from 'components/layout/sidebar/Sidebar';

const Documentation = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const tableOfContents = [
    { id: 'Introduction', name: 'Introduction', link: '#introduction' },
    {
      id: 'Overview',
      name: 'Overview',
      link: '#overview',
      subItems: [
        { id: 'cosmos-1', name: 'Cosmos Overview', link: '#cosmos-1' },
        { id: 'cosmos-2', name: 'Cosmos Overview', link: '#cosmos-2' },
        { id: 'cosmos-3', name: 'Cosmos Overview', link: '#cosmos-3' },
        { id: 'cosmos-4', name: 'Cosmos Overview', link: '#cosmos-4' },
      ],
    },
    { id: 'how-it-performs', name: 'How it performs', link: '#how-it-performs' },
    { id: 'getting-started', name: 'Getting Started', link: '#getting-started' },
  ];

  const sectionsData = [
    {
      id: 'introduction',
      title: 'Introduction',
      content: [
        {
          type: 'text',
          value:
            'Welcome to spotnet Documentation \n Spotnet is a decentralized platform designed to [describe purpose, e.g., "empower users to securely manage digital assets and access DeFi tools effortlessly"]. \n This documentation provides a comprehensive guide on using SpotNet and making the most of its features.',
        },
      ],
    },
    {
      id: 'overview',
      title: 'Overview',
      content: [
        {
          type: 'text',
          value:
            'What is [Product Name]?\n[Product Name] is a Web3 platform that leverages blockchain technology to [describe primary functionalities, e.g., "facilitate secure transactions, staking, and asset management without intermediaries"].',
        },
        {
          type: 'text',
          value: 'Core features include:',
        },
        {
          type: 'list',
          items: [
            'Decentralized Finance (DeFi): Access a suite of DeFi services, including lending, borrowing, and yield farming.',
            'Security-First Design: Built on smart contracts to ensure safety and transparency.',
            'Cross-Chain Compatibility: [Product Name] supports multiple blockchains for a seamless user experience.',
          ],
        },
      ],
    },
    {
      id: 'how-it-performs',
      title: 'How it performs',
      content: [
        {
          type: 'text',
          value: 'Spot Leverage Strategy with ZkLend',
        },
        {
          type: 'list',
          items: [
            'You put some ETH collateral into deposit as ZkLend.',
            'Then, we swap your ETH into USDC and use it as collateral for a loan in the ZkLend position.',
            'This process can be repeated 2 to 5 times, depending on the leverage multiplier you choose, to increase your collateral and borrowing capacity.',
          ],
        },
        {
          type: 'text',
          value: 'Once your position is opened, you can view it on the Dashboard page. There, you’ll see:',
        },
        {
          type: 'list',
          items: [
            'Health Factor: A measure of how safe your position is (the higher, the better).',
            'Collateral: The value of your assets in the position.',
            'Borrowed Amount: The total amount you have borrowed.',
          ],
        },
        {
          type: 'text',
          value: 'About position',
        },
        {
          type: 'list',
          items: [
            'If you wish to close your position, simply click on `Reedem` in the Dashboard page. This will allow you to withdraw your collateral and repay the loan.',
            'Currently, Spotnet only allows you to open a single position.',
            'If your health ratio level will be zero, you will be liquidated by ZkLend.',
            'You also have the option to enable notifications on Telegram, so you will be alerted if your health ratio reaches a dangerous level.',
          ],
        },
      ],
    },
    {
      id: 'zk-lend',
      title: 'Zklend Overview - Powering Your DeFi Journey with Security and Simplicity',
      content: [
        {
          type: 'text',
          value: 'Introducing zkLend',
        },
        {
          type: 'text',
          value:
            "Money markets have been a crucial component of financial systems since the Middle Ages, providing short-term funding and liquidity to banks, governments, and corporations. Today, money markets facilitate an estimated $3.2 trillion in daily transactions in the global financial system, making them critical for short-term funding needs. In the context of DeFi, money markets play an essential role in activities such as lending, borrowing, and liquidity provision. At zkLend, our goal is to create a simple, secure, and efficient platform for your liquidity needs. We've built a permissionless lending market where anyone can deposit and borrow digital assets directly from their wallets, at any time. When you deposit assets, you earn interest from borrowers using your funds. You can also use your deposited assets as collateral to borrow other digital assets.",
        },

        {
          type: 'text',
          value:
            "Our Alpha version is now available on the mainnet. Rest assured, we've fully audited the platform with reputable firms like ABDK and Nethermind, and the contracts have been formally specified since April 2023.",
        },

        {
          type: 'text',
          value:
            'With a focus on safety, ease of use, and cutting-edge blockchain technology, we’re confident that zkLend is on its way to becoming a leading platform in the DeFi space. Join us and experience the future of decentralized finance!',
        },
      ],
    },

    {
      id: 'powered-by-starknet',
      title: 'Powered by Starknet',
      content: [
        {
          type: 'text',
          value:
            "At zkLend, we believe zk-rollups are the key to unlocking Ethereum's full potential. By using Starknet's Layer 2 (L2) solution, we’re able to bring the speed and efficiency of zk-rollups together with the security and decentralization that Ethereum is known for. Starknet is one of the first zk-rollup platforms designed for general use. It offers fast transactions, low fees, and cutting-edge blockchain features that far exceed the capabilities of traditional networks. Key innovations like account abstraction, trustless bridging, parallel processing, and advanced proof techniques make Starknet stand out.",
        },

        {
          type: 'text',
          value:
            "With the strong track record of StarkWare and the team behind successful projects like ZCash and StarkEx, Starknet is the perfect platform to power zkLend and ensure we stay ahead of the curve. We're excited to be part of this groundbreaking technology!.",
        },
      ],
    },
    {
      id: 'getting-started',
      title: 'Getting Started',
      content: [
        {
          type: 'text',
          value: 'Setting Up Your Wallet',
        },
        {
          type: 'orderedList',
          items: [
            'Download a compatible Web3 wallet (e.g., MetaMask).',
            'Fund your wallet with the supported cryptocurrency.',
            'Connect your wallet to [Product Name].',
          ],
        },
      ],
    },
  ];

  return (
    <div className="documentation-page">
      <Sidebar title="Table of Contents" items={tableOfContents} />

      <div className="main-content">
        <h1 className="main-title">Spotnet Documentation</h1>
        <Sections sections={sectionsData} />
      </div>

      <ScrollButton />
    </div>
  );
};

export default Documentation;
