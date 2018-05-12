import React from 'react'

import App, { Container } from 'next/app'
import { Provider } from 'react-redux'
import withRedux from 'next-redux-wrapper'
import withReduxSaga from 'next-redux-saga'

import initStore from '../state/init_store'

import Content from '../components/Content'
import Navigation from '../components/Navigation'

import '../styles/layout.scss'

class MyApp extends App {
  static async getInitialProps({ Component, ctx }) {
    let pageProps = {}

    if(Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx)
    }

    return { pageProps }
  }

  render() {
    const { Component, pageProps, router, store } = this.props
    return (
      <Container>
        <Provider store={store}>
          <>
            <nav className={'nav'}>
              <Navigation/>
            </nav>

            <section className={'content'}>
              <Content
                Component={Component}
                pageProps={pageProps}
                route={router.route}
              />
            </section>
          </>
        </Provider>
      </Container>
    )
  }
}

export default withRedux(initStore)(withReduxSaga(MyApp))
