import mergeTransactions from '../common/merge_transactions'
import mergeBlocks from '../common/merge_blocks'
import mergePeers from '../common/merge_peers'


class BlockchainController {
  constructor() {
    this._peers = []
    this._transactions = []
    this._blocks = []
  }

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

  addPeers = (peers) => {
    peers = peers.map((peer) => {
      const address = peer.address.toString('hex')

      return {
        ...peer,
        address,
      }
    })

    this._peers = mergePeers(this._peers, peers)
  }

  addBlocks = (blocks) => {
    blocks = blocks.map(this._convertBlock)
    this._blocks = mergeBlocks(this._blocks, blocks)
  }

  addTransactions = (transactions) => {
    transactions = transactions.map(this._convertTransaction)
    this._transactions = mergeTransactions(this._transactions, transactions)
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
    const inputs = transaction.inputs.map(this._convertInput)
    const outputs = transaction.outputs.map(this._convertOutput)

    return {
      ...transaction,
      hash,
      inputs,
      outputs,
    }
  }

  _convertInput = (input) => {
    const src_hash = input.src_hash.toString('hex')
    const signature = input.signature.toString('hex')
    const key = input.key.toString('hex')

    return {
      ...input,
      src_hash,
      signature,
      key,
    }
  }

  _convertOutput = (input) => {
    const key = input.key.toString('hex')

    return {
      ...input,
      key,
    }
  }
}

export default BlockchainController

