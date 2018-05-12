import _ from 'lodash'

import Actions from './actions'
import merge from '../../common/merge'

const stateDefault = {
  nodes: [],
  blocks: [],
  transactions: [],
}

const mergeNewData = (state, action, fieldName, orderBy) => {
  const oldData = _.get(state, fieldName, [])
  const newData = _.get(action, `payload.data.${fieldName}`, [])
  return merge(oldData, newData, orderBy)
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

  case Actions.NODES_SENT:
  case Actions.TRANSACTIONS_SENT:
  case Actions.BLOCKS_SENT:
  case Actions.REFRESH_SUCCEEDED: {
    const nodes = mergeNewData(state, action, 'nodes', ['host', 'port', 'address', 'type'])
    const blocks = mergeNewData(state, action, 'blocks', [])
    const transactions = mergeNewData(state, action, 'transactions', [])

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
