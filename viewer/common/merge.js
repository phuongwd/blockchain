import _ from 'lodash'

function merge(oldData, newData, orderBy = null) {
  let mergedData = [...oldData, ...newData]

  if(orderBy) {
    mergedData = _.orderBy(mergedData, orderBy)
  }

  mergedData = _.uniqWith(mergedData, _.isEqual)
  return mergedData
}

export default merge
