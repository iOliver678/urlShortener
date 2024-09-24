import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
 return(
  <div id="body">
    <header id="title">Create a new link</header>
    <div className='inputBoxes'>
    <input
      type="text"
      id="urlFromUser"
      placeholder='Enter URl'
      />
    <input
      type="text"
      id="aliasFromUser"
      placeholder='Alias'
      />
    <button id="createUrl">Create</button>
    </div>
    <p id="tableHeader">List of URL's:</p>
    <table className='urlTable'>

    <thead>
      <tr className="header-panel">
        <th id="url-table">Url</th>
        <th>Alias</th>
        <th>Link</th>
        <th id='trashCan'></th>
      </tr>
    </thead>
    <tbody>

    </tbody>
    </table>
  </div>
 );
}

export default App
