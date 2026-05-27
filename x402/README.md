<div style="margin: 0; padding: 0; text-align: center; border: none;">
<a href="https://quantlet.com" target="_blank" style="text-decoration: none; border: none;">
<img src="https://github.com/StefanGam/test-repo/blob/main/quantlet_design.png?raw=true" alt="Header Image" width="100%" style="margin: 0; padding: 0; display: block; border: none;" />
</a>
</div>

```
Name of Quantlet: x402 Payment Protocol — Internet-Native USDC Micropayments over HTTP

Published in: DEDA-HUB-Quantlets

Description: Full-stack local demo of the x402 payment protocol: the dormant HTTP 402 status
code repurposed for machine-native, gasless USDC micropayments. Implements a seven-service
Docker stack — Anvil EVM blockchain (chain-id 8453), MockUSDC smart contract (EIP-3009
transferWithAuthorization), a Facilitator that verifies EIP-712 signatures and settles
on-chain, a FastAPI resource server protected by an @x402_gate decorator (three paywalled
endpoints at $0.001–$0.01 USDC), a pure-Python buyer client that signs and pays autonomously
without a browser or MetaMask, and a Streamlit dashboard for live monitoring of wallet
balances and AuthorizationUsed events. Demonstrates the complete x402 v2 protocol flow:
402 challenge → EIP-712 signing → PAYMENT-SIGNATURE retry → facilitator settlement →
200 OK resource delivery.

Keywords: x402, HTTP 402, micropayments, USDC, stablecoin, EIP-712, EIP-3009,
transferWithAuthorization, blockchain, Base, Ethereum, Solidity, smart contract, FastAPI,
Python, Docker, Anvil, Foundry, Coinbase, AI agents, machine payments, internet payments,
cryptography, digital signatures, DeFi, Web3, MCP, payment protocol

Author: Wolfgang Karl Härdle, Pavel Shibaev

Submitted: 2026-05-27 by Pavel Shibaev

Email: shibaev.media@gmail.com

Institution: Humboldt University of Berlin

Code: python/server.py, python/client.py, python/x402.py, facilitator/main.py,
      blockchain/src/MockUSDC.sol, blockchain/deploy.sh, dashboard/app.py, docker-compose.yml

```

<div align="center">
<img src="https://raw.githubusercontent.com/QuantLet/DEDA-HUB-Quantlets/main/x402/x402-protocol-flow.svg" alt="x402 Protocol Flow" />
</div>
