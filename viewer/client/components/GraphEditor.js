import React from 'react'

import { Graph } from 'react-d3-graph'


class GraphEditor extends React.Component {
  constructor(props, context) {
    super(props, context)

    this.state = {
      graphData: {
        nodes: [{ id: 'Harry' }, { id: 'Sally' }, { id: 'Alice' }],
        links: [{ source: 'Harry', target: 'Sally' }, {
          source: 'Harry',
          target: 'Alice',
        }],
      },
    }
  }

  onClickNode = (nodeId) => {
    console.log('Clicked node ${nodeId}')
  }

  onMouseOverNode = (nodeId) => {
    console.log(`Mouse over node ${nodeId}`)
  }

  onMouseOutNode = (nodeId) => {
    console.log(`Mouse out node ${nodeId}`)
  }

  onClickLink = (source, target) => {
    console.log(`Clicked link between ${source} and ${target}`)
  }

  onMouseOverLink = (source, target) => {
    console.log(`Mouse over in link between ${source} and ${target}`)
  }

  onMouseOutLink = (source, target) => {
    console.log(`Mouse out link between ${source} and ${target}`)
  }

  render = () => {
    const { graphData } = this.state

    const graphConfig = {
      nodeHighlightBehavior: true,
      node: {
        color: '#bcc6e8',
        highlightStrokeColor: '#38bf2d',
        size: 350,
      },
      link: {
        color: '#bfbcbb',
        highlightColor: '#35bfa7',
        highlightStrokeColor: '#35bfa7',
      },
    }

    return (
      <div>
        <div>

          <Graph
            id='graph-id'
            data={graphData}
            config={graphConfig}
            onClickNode={this.onClickNode}
            onClickLink={this.onClickLink}
            onMouseOverNode={this.onMouseOverNode}
            onMouseOutNode={this.onMouseOutNode}
            onMouseOverLink={this.onMouseOverLink}
            onMouseOutLink={this.onMouseOutLink}
          />


        </div>
        {/*language=CSS*/}
        <style jsx> {`
          .foo {

          }
        `}</style>
      </div>
    )
  }
}

export default GraphEditor
