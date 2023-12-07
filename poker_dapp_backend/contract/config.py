CONTRACT_ADDRESS = "0x69d7d375cdC5037c182a1eCEB5AC4C6EdE3CAD58"
RPC_URL = "https://eth-goerli.g.alchemy.com/v2/uIErl4h1g-xMaro6OjWJqQ_N2l0i-4E0"
CONTRACT_ABI = """
[
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "paymentToken",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "ReentrancyGuardReentrantCall",
      "type": "error"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "player",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        }
      ],
      "name": "JoinedGame",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "creator",
          "type": "address"
        }
      ],
      "name": "TableCreated",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_player",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_playerClientAddy",
          "type": "address"
        }
      ],
      "name": "getMsgHash",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_id",
          "type": "uint256"
        }
      ],
      "name": "getPlayers",
      "outputs": [
        {
          "internalType": "address[10]",
          "name": "",
          "type": "address[10]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address[10]",
          "name": "_players",
          "type": "address[10]"
        },
        {
          "internalType": "uint256[]",
          "name": "_balances",
          "type": "uint256[]"
        }
      ],
      "name": "getStateMsgHash",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_id",
          "type": "uint256"
        }
      ],
      "name": "getTable",
      "outputs": [
        {
          "components": [
            {
              "internalType": "uint256",
              "name": "id",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "minBuyIn",
              "type": "uint256"
            },
            {
              "internalType": "uint8",
              "name": "playerLimit",
              "type": "uint8"
            },
            {
              "internalType": "uint8",
              "name": "playerCount",
              "type": "uint8"
            },
            {
              "internalType": "bool",
              "name": "inPlay",
              "type": "bool"
            },
            {
              "internalType": "address",
              "name": "initiator",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "amountInPlay",
              "type": "uint256"
            },
            {
              "internalType": "address[10]",
              "name": "players",
              "type": "address[10]"
            }
          ],
          "internalType": "struct Poker.Table",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_gameId",
          "type": "uint256"
        }
      ],
      "name": "isAtCapacity",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_addy",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_gameId",
          "type": "uint256"
        }
      ],
      "name": "isInGame",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_gameId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "_clientAddy",
          "type": "address"
        },
        {
          "internalType": "bytes",
          "name": "_sig",
          "type": "bytes"
        },
        {
          "internalType": "uint256",
          "name": "_buyIn",
          "type": "uint256"
        }
      ],
      "name": "joinTable",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_id",
          "type": "uint256"
        },
        {
          "internalType": "bytes[]",
          "name": "_state",
          "type": "bytes[]"
        },
        {
          "internalType": "uint256[]",
          "name": "_balances",
          "type": "uint256[]"
        }
      ],
      "name": "leaveTable",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_msgHash",
          "type": "bytes32"
        },
        {
          "internalType": "bytes",
          "name": "_sig",
          "type": "bytes"
        }
      ],
      "name": "recoverSigner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes",
          "name": "_sig",
          "type": "bytes"
        }
      ],
      "name": "splitSignature",
      "outputs": [
        {
          "internalType": "bytes32",
          "name": "r",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "s",
          "type": "bytes32"
        },
        {
          "internalType": "uint8",
          "name": "v",
          "type": "uint8"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_minBuyIn",
          "type": "uint256"
        },
        {
          "internalType": "uint8",
          "name": "_playerLimit",
          "type": "uint8"
        },
        {
          "internalType": "address",
          "name": "_clientAddy",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_buyIn",
          "type": "uint256"
        },
        {
          "internalType": "bytes",
          "name": "_sig",
          "type": "bytes"
        }
      ],
      "name": "startTable",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "gameId",
          "type": "uint256"
        }
      ],
      "name": "tables",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "minBuyIn",
          "type": "uint256"
        },
        {
          "internalType": "uint8",
          "name": "playerLimit",
          "type": "uint8"
        },
        {
          "internalType": "uint8",
          "name": "playerCount",
          "type": "uint8"
        },
        {
          "internalType": "bool",
          "name": "inPlay",
          "type": "bool"
        },
        {
          "internalType": "address",
          "name": "initiator",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountInPlay",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
]
"""
