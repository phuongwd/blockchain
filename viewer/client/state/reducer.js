import _ from 'lodash'

import Actions from './actions'

const stateDefault = {
  nodes: [],
  blocks: [],
  transactions: [],
}

const reducer = (state = stateDefault, action) => {
  console.log(action)

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
    let nodes = _.get(action, 'payload.data.nodes', state.nodes)
    let blocks = _.get(action, 'payload.data.blocks', state.blocks)
    let transactions = _.get(action, 'payload.data.transactions', state.transactions)

    nodes = _.merge([], nodes, state.nodes)
    nodes = _.sortBy(nodes, ['host', 'port', 'address', 'type'])

    blocks = _.merge([], blocks, state.blocks)
    transactions = _.merge([], transactions, state.transactions)

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
