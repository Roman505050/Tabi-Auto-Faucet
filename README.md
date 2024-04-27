![Tabi img](https://miro.medium.com/v2/resize:fit:950/1*SK72e-jRgJTQju2xUKShXg.png)

#   Tabi Auto Faucet

Tabi Auto Faucet is a simple script that automates the process of claiming from the faucet. It is a simple script that uses the `requests` library to send a request to the faucet every 125 seconds. 

The script is designed for multi-account users. To use a proxy and address in a pair to claim tokens from the faucet for specific address with a specific proxy (or without a proxy, if without proxy, then IP machines will be used).

## Instructions for data.txt

The `data.txt` file is used to store the data of the accounts. The data is stored in the following format:

```
ip:port:login:pass:address
ip:port:login:pass:address
none:none:none:none:address 
```

The `none:none:none:none:address` is used to claim tokens without a proxy.
The `ip:port:login:pass:address` is used to claim tokens with a proxy.

## Installation

1. Clone the repository

```bash
git clone https://github.com/Roman505050/Tabi-Auto-Faucet.git
```

2. Install the requirements

```bash
pip install requests
```

## Getting Started

Run the script

```bash
python main.py
```

## Power by Tg Channel - [Coin Artifacts](https://t.me/+7esxWN4fQR5jZTYy)