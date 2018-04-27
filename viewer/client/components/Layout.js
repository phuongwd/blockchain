import React from 'react'
import PropTypes from 'prop-types'

import apply from '../../common/apply'

import '../styles/layout.scss'
import Navigation from './Navigation'

const Layout = ({ children }) => {
  return (
    <>
      <nav>
        <Navigation/>
      </nav>

      <section className="container container-content">
        {
          apply(children, (child, i) => {
            return (
              child
            )
          })
        }
      </section>

      {/*<footer>*/}
      {/*<Footer/>*/}
      {/*</footer>*/}

      {/*language=SCSS*/}
      <style jsx> {`
        //.container-nav {
        //  z-index: 10;
        //}
        //
        //.container-content {
        //  z-index: 100;
        //}
      `}</style>
    </>
  )
}

Layout.propTypes = {
  children: PropTypes.any,
}

export default Layout
