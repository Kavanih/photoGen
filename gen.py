import { ethers } from "ethers";

const provider = new ethers.providers.JsonRpcProvider(
  "https://mainnet.hashio.io/api"
);
const contractAddress = "0x4a46705176fac8fd5c8061f94a2c44416e7b20e6"; // Example address

const abi = [
  {
    anonymous: false,
    inputs: [
      {
        indexed: true,
        internalType: "address",
        name: "sender",
        type: "address",
      },
      {
        indexed: false,
        internalType: "uint256",
        name: "amount0In",
        type: "uint256",
      },
      {
        indexed: false,
        internalType: "uint256",
        name: "amount1In",
        type: "uint256",
      },
      {
        indexed: false,
        internalType: "uint256",
        name: "amount0Out",
        type: "uint256",
      },
      {
        indexed: false,
        internalType: "uint256",
        name: "amount1Out",
        type: "uint256",
      },
      {
        indexed: true,
        internalType: "address",
        name: "to",
        type: "address",
      },
    ],
    name: "Swap",
    type: "event",
  },
];

const abiInterfaces = new ethers.utils.Interface(abi); // Corrected access to Interface

async function fetchData() {
  const latestBlock = await provider.getBlockNumber();
  const fromBlock = latestBlock - 1000;

  const filter = {
    address: contractAddress,
    topics: [abiInterfaces.getEvent("Swap").topicHash],
    fromBlock: fromBlock,
    toBlock: latestBlock,
  };

  const logs = await provider.getLogs(filter);
  logs.forEach((log) => {
    const parsedLog = abiInterfaces.parseLog(log);
    const output = `Transaction hash: ${log.transactionHash}, Amount In: ${parsedLog.args.amount0In}, Amount Out: ${parsedLog.args.amount1Out}`;
    console.log(output);
  });
}

fetchData();
