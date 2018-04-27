import React from 'react'
import { InteractiveForceGraph, ForceGraphNode, ForceGraphLink } from 'react-vis-force'


const ForceGraph = (props) => {
  return (
    <div className={'container'}>

      <InteractiveForceGraph
        simulationOptions={{ height: 300, width: 300 }}
        labelAttr="label"
        onSelectNode={(node) => console.log(node)}
        highlightDependencies
      >
        <ForceGraphNode node={{ id: 'first-node', label: 'First node' }} fill="red" />
        <ForceGraphNode node={{ id: 'second-node', label: 'Second node' }} fill="blue" />
        <ForceGraphLink link={{ source: 'first-node', target: 'second-node' }} />
      </InteractiveForceGraph>

      {/*language=CSS*/}
      <style jsx> {`
        .container {
          background-color: #eeeeee;
        }
      `}</style>
    </div>
  )
}

export default ForceGraph
