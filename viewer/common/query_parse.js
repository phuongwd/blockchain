import _ from 'lodash'
import is from 'is_js'
import qs from 'qs'

export default function parseQuery(url) {
  const urlSplit = url.split('?')
  if(urlSplit.length < 2) {
    return {}
  }

  const query = urlSplit[1]

  // Refuse to parse if query is not a string or too sort or too long
  if(is.not.string(query) || is.empty(query) || query.length > 1024) {
    return {}
  }

  // Parse, using the most basic setup
  return qs.parse(query, {
    parseArrays: true,
    arrayLimit: 32,
    depth: 1,
    parameterLimit: 64,
  })
}
