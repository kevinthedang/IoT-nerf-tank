import { useState } from 'react';
import favicon from '/favicon-tank.png'
import './style/style.css'
import Axios from 'axios';

function App() {
  const [current, setCurrent] = useState(0);
  const [connection, setConnection] = useState(false);

  // get currect connection status on render or load
  Axios.get('http://localhost:8080/getStatus').then((response) => {
        setConnection(response.data.connection);
  })

  const validate_and_send = (message) => {
    console.log(`Trying to send: ${message}`);
    Axios.post('http://localhost:8080/sendMessage', {
      command: message
    }).catch((err) => {
      console.log(err);
    })

    // for every command, check if the server is receiving them
    Axios.get('http://localhost:8080/getStatus').then((response) => {
      setConnection(response.data.connection);
    })

    setCurrent(current + 1);
    if (current > 5)
    {
      window.location.reload();
    }
  }

  return (
    <div className="App">
      <h1>Tank Control Interface</h1>

      <div className="main-container">
          <div className="title">
              Tank Movement
          </div>

          <div className="title">
              Controls: { connection ? <span id='active'>Active</span> : <span id='inactive'>Inactive</span> }
          </div>

          <div className="title">
              Turret Controls
          </div>
      </div>

      <div className="controls-layout">
        {/* movement controls */}
        <div className="grid-container">
            <div></div>
            <div className="grid-item" id="forward" onClick={() => {validate_and_send('forward')}}>Forward</div>
            <div></div>
            <div className="grid-item" id="left" onClick={() => {validate_and_send('left')}}>Turn Left</div>
            <div></div>
            <div className="grid-item" id="right" onClick={() => {validate_and_send('right')}}>Turn Right</div>
            <div></div>
            <div className="grid-item" id="reverse" onClick={() => {validate_and_send('reverse')}}>Reverse</div>
            <div></div>
        </div>

        {/* turret controls */}
        <div className="grid-container">
            <div></div>
            <div className="grid-item" id="u-aim" onClick={() => {validate_and_send('up')}}>Aim Up</div>
            <div></div>
            <div className="grid-item" id="l-aim" onClick={() => {validate_and_send('l-aim')}}>Aim Left</div>
            <div className="grid-fire" id="fire" onClick={() => {validate_and_send('fire!')}}>Fire!</div>
            <div className="grid-item" id="r-aim" onClick={() => {validate_and_send('r-aim')}}>Aim Right</div>
            <div></div>
            <div className="grid-item" id="d-aim" onClick={() => {validate_and_send('down')}}>Aim Down</div>
            <div></div>
        </div>
      </div>

      {/* misc buttons container */}
      <div className="main-container">
        {/* Laser container */}
        <div className="grid-container">
          <div className="grid-item" onClick={() => {validate_and_send('laser-off')}}>Laser off</div>
          <div className="grid-item" onClick={() => {validate_and_send('laser-on')}}>Laser On</div>
        </div>

        {/* Connection container */}
        <div className="grid-container">
          <div className="grid-item" onClick={() => {validate_and_send('connect')}}>Connect</div>
          <div className="grid-item" onClick={() => {validate_and_send('disconnect')}}>Disconnect</div>
        </div>
      </div>
    </div>
  )
}

export default App
