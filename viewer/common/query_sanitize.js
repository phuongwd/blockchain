import _ from 'lodash'
import is from 'is_js'

export default function querySanitize(query) {
  return _.mapValues(query, (val) => {
    if(is.array(val)) {
      return _.uniq(val.sort())
    }
    return val
  })
}
