import is from 'is_js'

export default function isXHr(req, res, next) {
  if(is.not.existy(req.xhr)) {
    req.xhr = (req.headers['X-Requested-With'] === 'XMLHttpRequest')
  }
  return next()
}
