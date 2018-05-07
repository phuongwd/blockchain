import React from 'react'

import { CSSTransition, TransitionGroup } from 'react-transition-group'

const Content = ({ Component, pageProps, route }) => {
  return (
    <TransitionGroup>
      <CSSTransition
        key={`${route}-csstransition`}
        classNames='fade'
        timeout={1000}
      >
        <div className={'fill'} key={`${route}-div`}>
          <Component {...pageProps} />
        </div>
      </CSSTransition>
    </TransitionGroup>
  )
}

export default Content
