import is from 'is_js'

export function splitAndTakeFirst(str, symbol) {
  if(is.not.string(str) || is.not.string(symbol)) {
    return null
  }

  const splits = str.split('@')
  if(splits.length > 0) {
    return splits[0]
  }
  return null
}

export function splitAndTakeLast(str, symbol) {
  if(is.not.string(str) || is.not.string(symbol)) {
    return null
  }

  const splits = str.split('@')
  if(splits.length > 0) {
    return splits[splits.length - 1]
  }
  return null
}

export function hostFromEmail(email) {
  const host = splitAndTakeLast(email, '@')
  if(is.empty(host)) {
    return ''
  }
  return `http://${host}`
}
