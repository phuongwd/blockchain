import _ from 'lodash'

import Actions from '../client/state/actions'
import merge from '../common/merge'

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

  all = () => {
    return {
      nodes: this.peers(),
      blocks: this.blocks(),
      transactions: this.transactions(),
    }
  }

  peers = () => this._peers

  blocks = () => this._blocks

  transactions = () => this._transactions

  _broadcastThrottled = (data) => {
    _.throttle(() => this._wss.broadcast(data), 1000)()
  }

  addPeers = (peers) => {
    this._peers = merge(this._peers, peers)
    this._broadcastThrottled(Actions.nodes(peers))
  }

  addBlocks = (blocks) => {
    this._blocks = merge(this._blocks, blocks)
    this._broadcastThrottled(Actions.blocks(blocks))
  }

  addTransactions = (transactions) => {
    this._transactions = merge(this._transactions, transactions)
    this._broadcastThrottled(Actions.transactions(transactions))
  }
}

export default BlockchainController

