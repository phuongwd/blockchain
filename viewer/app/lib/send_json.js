import Status from '../../client/status'

const sendJson = (req, res, next) => {
  res.sendJson = ({ status = Status.Success, data = null }) => {
    return res.status(status.httpCode).json({
      error: status !== Status.Success,
      payload: { status, data: { ...data } },
    })
  }
  return next()
}

export default sendJson
