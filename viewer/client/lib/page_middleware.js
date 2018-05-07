import { connect } from 'react-redux'
import withReduxSaga from 'next-redux-saga'
import { reduxForm } from 'redux-form'

const pageMiddleware = (
  page,
  {
    mapStateToProps = (state) => state,
    mapDispatchToProps = undefined,
    mergeProps = undefined,
    connectOptions = undefined,
    reduxFormOptions = undefined,
  } = {},
) => {

  let result = page

  if(reduxFormOptions) {
    result = reduxForm(reduxFormOptions)(result)
  }

  result = withReduxSaga({ async: false })(result)

  result = connect(mapStateToProps, mapDispatchToProps, mergeProps, connectOptions)(result)

  return result
}

// reduxForm({ form: page.getDisplayName() })(page),

export default pageMiddleware
