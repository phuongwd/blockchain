const Actions = {
  REFRESH_REQUESTED: 'REFRESH_REQUESTED',
  REFRESH_SUCCEEDED: 'REFRESH_SUCCEEDED',
  REFRESH_FAILED: 'REFRESH_FAILED',

  NODES_SENT: 'NODES_SENT',
  TRANSACTIONS_SENT: 'TRANSACTIONS_SENT',
  BLOCKS_SENT: 'BLOCKS_SENT',

  refresh: () => {
    return {
      type: Actions.REFRESH_REQUESTED,
      error: false,
      payload: {},
    }
  },

  nodes: (nodes) => {
    return {
      type: Actions.NODES_SENT,
      error: false,
      payload: { data: { nodes } },
    }
  },

  transactions: (transactions) => {
    return {
      type: Actions.TRANSACTIONS_SENT,
      error: false,
      payload: { data: { transactions } },
    }
  },

  blocks: (blocks) => {
    return {
      type: Actions.BLOCKS_SENT,
      error: false,
      payload: { data: { blocks } },
    }
  },
}

export default Actions
