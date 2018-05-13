import merge from './merge'

const mergeBlocks = (oldBlocks, newBlocks) => {
  return merge(oldBlocks, newBlocks, {
    unionBy: 'hash',
    orderBy: ['hash', 'hash_prev', 'difficulty', 'nonce'],
  })
}

export default mergeBlocks
