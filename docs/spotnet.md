# Spotnet functionality documentation

## Overview
Spotnet is a dApp designed for increasing of initial collateral deposit by utilizing lending 
protocols and AMMs for borrowing tokens, swapping them and redepositing up to x4 of starting capital(as for now).

## Spotnet Smart Contract
Smart contract consists of a constructor and three methods for public use.

### Constructor
Constructor of our contract receives three parameters(ekubo_core and zk_market are serialized to Dispatcher types for starknet::interfaces):
* `owner`: ContractAddress
* `ekubo_core`: ContractAddress
* `zk_market`: ContractAddress
Onwer address is an account address of the user who deploys it, only owner can deposit funds and close position on lending protocol.

### loop_liquidity
The `loop_liquidity` method is responsible for deposit of collateral token. For now only one position can be opened, to create the new you need to close old one.
For validating the identity of the caller is used an address of account initiated a transaction instead of a caller for testing purposes.
This method has next parameters:
* `deposit_data`: DepositData - Object of internal type which stores main deposit information.
* `pool_key`: PoolKey - Ekubo type for obtaining info about the pool and swapping tokens.
* `ekubo_limits`: EkuboSlippageLimits - Object of internal type which represents upper and lower sqrt_ratio values on Ekubo. Used to control slippage while swapping.
* `pool_price`: felt252 - Price of `deposit` token in terms of `debt` token(so for ex. 2400000000 USDC for ETH when depositing ETH).

It's flow can be described as follows:

```
assertions

constants & dispatchers created

tokens transferred to contract from user

enabling token as collateral on lending protocol

approve & deposit initial amount

while total_deposited < initial_amount * multiplier {
    calculate borrow amount

    borrow

    swap on AMM to deposit token

    approve & deposit
}

emit event
```

### close_position
The `close_position` method is responsible for repaying debts and withdrawing all tokens from zklend. Can be called only if there is active position. For validating the 
identity of the caller is used an address of account initiated a transaction instead of a caller for testing purposes.
The method has next parameters:
* `supply_token`: ContractAddress - Address of the token used as collateral.
* `debt_token`: ContractAddress - Address of the token used as borrowing.
* `pool_key`: PoolKey - Ekubo type for obtaining info about the pool and swapping tokens.
* `ekubo_limits`: EkuboSlippageLimits - Object of internal type which represents upper and lower sqrt_ratio values on Ekubo. Used to control slippage while swapping.
* `supply_price`: TokenPrice - Price of `supply` token in terms of `debt` token(so for ex. 2400000000 USDC for ETH).
* `debt_price`: TokenPrice - Price of `debt` token in terms of `supply` token(for ex. 410000000000000 ETH for USDC).

It's flow can be described as follows:
```
assertions

constants & dispatchers created

while debt != 0 {
    calculate amount available for withdraw

    withdraw

    swap to debt token

    repay
}
transfer tokens to user

disable collateral token

emit event
```

### claim_reward
The `claim_reward` method claims airdrop reward accumulated by the contract that deposited into zkLend. Claim only possible if position is currently open.
This method has next parameters:
* `claim_data`: Claim - contains data about claim operation
* `proof`: Span<felt252> - proof used to validate the claim
* `airdrop_addr`: ContractAddress - address of a contract responsible for claim

Ir's flow can be described as follow
```
assertions

airdrop claim

transfer half of reward to the treasury
```

## Important types, events and constants
### Types
```
struct DepositData {
    token: ContractAddress,
    amount: TokenAmount,
    multiplier: u32
}
```

### Events
```
struct LiquidityLooped {
    initial_amount: TokenAmount,
    deposited: TokenAmount,
    token_deposit: ContractAddress,
    borrowed: TokenAmount,
    token_borrowed: ContractAddress
}
```
```
struct PositionClosed {
    deposit_token: ContractAddress,
    debt_token: ContractAddress,
    withdrawn_amount: TokenAmount,
    repaid_amount: TokenAmount
}
```

### Constants
* ZK_SCALE_DECIMALS is used for scaling down values obtained by multiplying on zklend collateral and borrow factors.
