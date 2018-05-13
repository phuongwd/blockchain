import _ from 'lodash'

import Actions from './actions'
import mergePeers from '../../common/merge_peers'
import mergeBlocks from '../../common/merge_blocks'
import mergeTransactions from '../../common/merge_transactions'

const stateDefault = {
  blockIdx: 0,
  nodes: [],
  blocks: [],
  transactions: [],
}

const mergeNewData = (state, action, fieldName, merger) => {
  const oldData = _.get(state, fieldName, [])
  const newData = _.get(action, `payload.data.${fieldName}`, [])
  return merger(oldData, newData)
}

const restrictTo = (value, from, to) => {
  if(to <= from) {
    return from
  }

  if(from >= to) {
    return to
  }

  return Math.min(to, Math.max(from, value))
}

const reducer = (state = stateDefault, action) => {
  // console.log(action)

  switch(action.type) {

  case Actions.REFRESH_REQUESTED: {
    return {
      ...state,
      updated: false,
    }
  }

  case Actions.BLOCK_NEXT: {
    const blockIdx = restrictTo(state.blockIdx + 1, 0, state.blocks.length - 1)
    return {
      ...state,
      blockIdx,
    }
  }

  case Actions.BLOCK_PREV: {
    const blockIdx = restrictTo(state.blockIdx - 1, 0, state.blocks.length - 1)
    return {
      ...state,
      blockIdx,
    }
  }

  case Actions.BLOCK_SET: {
    let blockIdx = _.get(action, 'payload.data.blockIdx', state.blockIdx)
    blockIdx = restrictTo(blockIdx, 0, state.blocks.length - 1)

    return {
      ...state,
      blockIdx,
    }
  }

  case Actions.NODES_SENT:
  case Actions.TRANSACTIONS_SENT:
  case Actions.BLOCKS_SENT:
  case Actions.REFRESH_SUCCEEDED: {
    const nodes = mergeNewData(state, action, 'nodes', mergePeers)
    const blocks = mergeNewData(state, action, 'blocks', mergeBlocks)
    const transactions = mergeNewData(state, action, 'transactions', mergeTransactions)

    console.log(action)

    return {
      ...state,
      updated: true,
      nodes,
      blocks,
      transactions,
    }
  }

  case Actions.REFRESH_FAILED: {
    return {
      ...state,
      updated: true,
      err: _.get(action, 'payload.status', {}),
      user: null,
    }
  }

  default:
    return state
  }
}

export default reducer
