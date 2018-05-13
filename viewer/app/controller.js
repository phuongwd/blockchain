import _ from 'lodash'

import Actions from '../client/state/actions'

import mergeTransactions from '../common/merge_transactions'
import mergeBlocks from '../common/merge_blocks'
import mergePeers from '../common/merge_peers'


class BlockchainController {
  constructor() {
    this._wss = null
    this._rpcClient = null
    this._peers = []
    this._transactions = []
    this._blocks = []
  }

  setRpcClient = (rpcClient) => { this._rpcClient = rpcClient }

  // setWebsocketServer = (wss) => { this._wss = wss }

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

  // _broadcastThrottled = (data) => {
  //   _.throttle(() => this._wss.broadcast(data), 1000)()
  // }

  addPeers = (peers) => {
    peers = peers.map((peer) => {
      const address = peer.address.toString('hex')

      return {
        ...peer,
        address,
      }
    })

    // const oldLen = this._peers.length
    this._peers = mergePeers(this._peers, peers)
    // const newLen = this._peers.length
    // console.log('addPeers       : ', oldLen, ' -> ', newLen)
    // this._broadcastThrottled(Actions.nodes(peers))
  }

  addBlocks = (blocks) => {
    blocks = blocks.map(this._convertBlock)

    // const oldLen = this._blocks.length
    this._blocks = mergeBlocks(this._blocks, blocks)
    // const newLen = this._blocks.length
    // console.log('addBlocks      : ', oldLen, ' -> ', newLen)
    // this._broadcastThrottled(Actions.blocks(blocks))
  }

  _convertBlock = (block) => {
    const hash = block.hash.toString('hex')
    const hash_prev = block.hash_prev.toString('hex')
    const merkle_root = block.merkle_root.toString('hex')
    const transactions = block.transactions.map(this._convertTransaction)

    return {
      ...block,
      hash,
      hash_prev,
      merkle_root,
      transactions,
    }
  }

  _convertTransaction = (transaction) => {
    const hash = transaction.hash.toString('hex')

    return {
      ...transaction,
      hash,
    }
  }

  addTransactions = (transactions) => {
    transactions = transactions.map(this._convertTransaction)
    // const oldLen = this._transactions.length
    this._transactions = mergeTransactions(this._transactions, transactions)
    // const newLen = this._transactions.length
    // console.log('addTransactions: ', oldLen, ' -> ', newLen)
    // this._broadcastThrottled(Actions.transactions(transactions))
  }
}

export default BlockchainController

