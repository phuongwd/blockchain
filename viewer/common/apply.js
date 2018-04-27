import is from 'is_js'

export default function apply(arr, f) {
  if(is.array(arr)) {
    return arr.map(f)
  }

  return [f(arr, 0)]
}
