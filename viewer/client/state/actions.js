const Actions = {
  REFRESH_REQUESTED: 'REFRESH_REQUESTED',
  REFRESH_SUCCEEDED: 'REFRESH_SUCCEEDED',
  REFRESH_FAILED: 'REFRESH_FAILED',

  BLOCK_NEXT: 'BLOCK_NEXT',
  BLOCK_PREV: 'BLOCK_PREV',
  BLOCK_SET: 'BLOCK_SET',

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

  nextBlock: () => {
    return {
      type: Actions.BLOCK_NEXT,
      error: false,
      payload: {},
    }
  },

  prevBlock: () => {
    return {
      type: Actions.BLOCK_PREV,
      error: false,
      payload: {},
    }
  },

  setBlock: (blockIdx) => {
    return {
      type: Actions.BLOCK_SET,
      error: false,
      payload: { data: { blockIdx } },
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
