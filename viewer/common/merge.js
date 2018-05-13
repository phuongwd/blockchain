import _ from 'lodash'

function merge(oldData, newData, { unionBy = null, orderBy = null }) {
  let mergedData = _.unionBy(oldData, newData, unionBy)

  if(orderBy) {
    mergedData = _.orderBy(mergedData, orderBy)
  }

  return mergedData
}

export default merge
