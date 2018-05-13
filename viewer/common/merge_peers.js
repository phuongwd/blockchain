import merge from './merge'

const mergePeers = (oldPeers, newPeers) => {
  return merge(oldPeers, newPeers, {
    unionBy: 'address',
    orderBy: ['host', 'port', 'address'],
  })
}

export default mergePeers
