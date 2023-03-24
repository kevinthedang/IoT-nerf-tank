import { useState } from 'react'
import favicon from '/favicon-tank.png'
import './style/style.css'
import Axios from 'axios';

function App() {

  const validate_and_send = () => {
    Axios.post('https://localhost:8080/sendMessage', {
      
    })
  }

  return (
    <div className="App">
      <h1>Tank Control Interface</h1>

      <div class="main-container">
          <div class="title">
              Tank Movement
          </div>

          <div class="title">
              Turret Controls
          </div>
      </div>

      <div class="controls-layout">
        {/* movement controls */}
        <div class="grid-container">
            <div></div>
            <div class="grid-item" id="foward" onClick={}>Foward</div>
            <div></div>
            <div class="grid-item" id="left">Turn Left</div>
            <div></div>
            <div class="grid-item" id="right">Turn Right</div>
            <div></div>
            <div class="grid-item" id="reverse">Reverse</div>
            <div></div>
        </div>

        {/* turret controls */}
        <div class="grid-container">
            <div></div>
            <div class="grid-item" id="u-aim">Up</div>
            <div></div>
            <div class="grid-item" id="l-aim">Turn Left</div>
            <div class="grid-fire" id="fire">Fire!</div>
            <div class="grid-item" id="r-aim">Turn Right</div>
            <div></div>
            <div class="grid-item" id="d-aim">Down</div>
            <div></div>
        </div>
      </div>
    </div>
  )
}

export default App
