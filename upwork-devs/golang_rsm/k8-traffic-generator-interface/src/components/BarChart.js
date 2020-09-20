import React from 'react'
import { Bar } from 'react-chartjs-2'

function BarChart (props) {
  const options = {
    title: {
      display: true,
      text: 'Time Response Results'
    },
    responsive: true
  }
  return <Bar data={props.chartData} options={options} />
}

export default BarChart