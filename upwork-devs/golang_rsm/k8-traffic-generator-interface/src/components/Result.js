import React from 'react'

function Result(props) {
  return (
    <React.Fragment>
      <td className="border px-4 py-2">{props.result.timeresp}</td>
      <td className="border px-4 py-2">{props.result.status}</td>
      <td className="border px-4 py-2">{props.result.urll}</td>
    </React.Fragment>
  )
}

export default Result
