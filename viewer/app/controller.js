import _ from 'lodash'

import Actions from '../client/state/actions'

class BlockchainController {
  constructor() {
    this.wss = null
    this.rpcClient = null
  }

  setRpcClient = (rpcClient) => { this.rpcClient = rpcClient }

  setWebsocketServer = (wss) => { this.wss = wss }

  peers = () => {
    return this._model.peers()
  }

  addPeers = (peers) => {
    console.log(peers)
    this.wss.broadcast(Actions.nodes(peers))
  }

  blocks = () => {
    return this._model.blocks()
  }

  addBlocks = (blocks) => {

  }

  transactions = () => {
    return this._model.transactions()
  }

  addTransactions = (transactions) => {

  }
}

export default BlockchainController

