import _ from 'lodash'

import Actions from '../client/state/actions'

class BlockchainController {
  constructor() {
    this._wss = null
    this._rpcClient = null
    this._peers = []
    this._transactions = []
    this._blocks = []
  }

  setRpcClient = (rpcClient) => { this._rpcClient = rpcClient }

  setWebsocketServer = (wss) => { this._wss = wss }

  peers = () => {
    return this._peers
  }

  addPeers = (peers) => {
    this._wss.broadcast(Actions.nodes(peers))
  }

  blocks = () => {
    return this._blocks
  }

  addBlocks = (blocks) => {

  }

  transactions = () => {
    return this._transactions
  }

  addTransactions = (transactions) => {

  }
}

export default BlockchainController

