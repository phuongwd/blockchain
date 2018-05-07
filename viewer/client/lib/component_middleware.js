import { connect } from 'react-redux'

const componentMiddleware = (
  component,
  {
    mapStateToProps = (state) => state,
    mapDispatchToProps = undefined,
    mergeProps = undefined,
    connectOptions = undefined,
  } = {},
) => {
  return connect(mapStateToProps, mapDispatchToProps, mergeProps, connectOptions)(component)
}

export default componentMiddleware
