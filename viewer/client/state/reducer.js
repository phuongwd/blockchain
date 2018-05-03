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

  case Actions.REFRESH_SUCCEEDED: {
    return {
      ...state,
      updated: true,
      nodes: _.get(action, 'payload.data.nodes', state.nodes),
      blocks: _.get(action, 'payload.data.blocks', state.blocks),
      transactions: _.get(action, 'payload.data.transactions', state.transactions),
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

  case Actions.NODES_SENT: {
    return {
      ...state,
      updated: true,
      nodes: _.get(action, 'payload.data.nodes', state.nodes),
    }
  }

  case Actions.TRANSACTIONS_SENT: {
    return {
      ...state,
      updated: true,
      blocks: _.get(action, 'payload.data.blocks', state.blocks),
    }
  }

  case Actions.BLOCKS_SENT: {
    return {
      ...state,
      updated: true,
      transactions: _.get(action, 'payload.data.transactions', state.transactions),
    }
  }

  default:
    return state
  }
}

export default reducer
