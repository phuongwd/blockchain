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
    const oldLen = this._peers.length
    this._peers = merge(this._peers, peers)
    const newLen = this._peers.length
    console.log('addPeers       : ', oldLen, ' -> ', newLen)
    this._broadcastThrottled(Actions.nodes(peers))
  }

  addBlocks = (blocks) => {
    const oldLen = this._blocks.length
    this._blocks = merge(this._blocks, blocks)
    const newLen = this._blocks.length
    console.log('addBlocks      : ', oldLen, ' -> ', newLen)
    this._broadcastThrottled(Actions.blocks(blocks))
  }

  addTransactions = (transactions) => {
    const oldLen = this._transactions.length
    this._transactions = merge(this._transactions, transactions)
    const newLen = this._transactions.length
    console.log('addTransactions: ', oldLen, ' -> ', newLen)
    this._broadcastThrottled(Actions.transactions(transactions))
  }
}

export default BlockchainController

