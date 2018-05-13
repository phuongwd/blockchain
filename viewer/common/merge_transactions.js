import merge from './merge'

const mergeTransactions = (oldTxs, newTxs) => {
  return merge(oldTxs, newTxs, {
    unionBy: 'hash',
    orderBy: ['hash'],
  })
}

export default mergeTransactions
