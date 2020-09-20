import React, { useState } from 'react'
import Loader from '../components/Loader'
import Result from '../components/Result'
import axios from 'axios'
import BarChart from '../components/BarChart'

function Home() {
 const url = 'http://localhost:10000/api'
  const [results, setResults] = useState({
    loading: false,
    data: null,
    error: false
  })

  const startTest = () => {
    setResults({
      loading: true,
      data: null,
      error: false
    })
    axios.get(url)
      .then(response => {
        setResults({
          loading: false,
          data: response.data,
          error: false
        })
      })
      .catch(error => {
        setResults({
          loading: false,
          data: null,
          error: true
        })
      })
  }

  let loader = null
  let content = null
  let chartContent = {}

  if (results.loading) {
    loader = <Loader></Loader>
  }

  if (results.data) {
    content =
      results.data.map((result, index) => 
        <tr key={index}>
            <Result result={result}/>
        </tr>
      )
    
    chartContent = {
      labels: results.data.map(result => result.urll),
      datasets: [
        {
          label: 'Time Response (ms)',
          data: results.data.map(result => parseFloat(result.timeresp)),
          borderColor: results.data.map(() => 'rgba(54, 162, 235, 0.2)'),
          backgroundColor: results.data.map(() => 'rgba(54, 162, 235, 0.2)')
        }
      ]
    }
  }

  return (
    <div className="text-center">
      <h1 className="font-bold text-2xl">Generate Tests</h1>
      <div className="my-3">
        <button 
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline"
          onClick={() => startTest()}
          disabled={content}
        >
          Generate Test
        </button>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full ml-3 focus:outline-none focus:shadow-outline"
          onClick={() => setResults({...results, data: null})}
          disabled={!content}
        >
          Clear Results
        </button>
      </div>
      <hr/>
      <span style={{display: content ? 'none' : ''}}>Please click on Generate Test to start the test</span>
      {loader}
      <div style={{display: content ? '' : 'none'}}>
        <div className="mt-3">
          <div className="font-bold text-2xl">
            Results:
          </div>
          <table className="table-auto w-full" >
            <thead>
              <tr>
                <th className="px-4 py-2">Response Time</th>
                <th className="px-4 py-2">Status</th>
                <th className="px-4 py-2">Url</th>
              </tr>
            </thead>
            <tbody>
              {content}
            </tbody>
          </table>
        </div>
        <hr/>
        <div className="mt-3">
          <BarChart chartData={chartContent} />
        </div>
      </div>
    </div>
  )
}

export default Home
