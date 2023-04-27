import { useState } from 'react';
import favicon from '/favicon-tank.png'
import './style/style.css'
import UpArrow from './style/images/up-arrow.png';
import DownArrow from './style/images/down-arrow.png';
import LeftArrow from './style/images/left-arrow.png';
import RightArrow from './style/images/right-arrow.png';
import UpDouble from './style/images/up-double.png';
import DownDouble from './style/images/down-double.png';
import LeftDouble from './style/images/left-double.png';
import RightDouble from './style/images/right-double.png';
import BulletSingle from './style/images/bullet-single.png';
import BulletBurst from './style/images/bullet-burst.png';
import OffSwitch from './style/images/switch-off.png';
import OnSwitch from './style/images/switch-on.png';
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
              Control Status: { connection ? <span id='active'>Active</span> : <span id='inactive'>Inactive</span> }
          </div>

          <div className="title">
              Turret Controls
          </div>
      </div>

      <div className="controls-layout">
        {/* movement controls */}
        <div className="grid-container">
            <div></div>
            <div className="grid-item" id="forward" onClick={() => {validate_and_send('forward')}}><img src={UpArrow} width="80%" height="80%" class="center"/></div>
            <div></div>
            <div className="grid-item" id="left" onClick={() => {validate_and_send('left')}}><img src={LeftArrow} width="80%" height="80%" class="center"/></div>
            <div></div>
            <div className="grid-item" id="right" onClick={() => {validate_and_send('right')}}><img src={RightArrow} width="80%" height="80%" class="center"/></div>
            <div></div>
            <div className="grid-item" id="reverse" onClick={() => {validate_and_send('reverse')}}><img src={DownArrow} width="80%" height="80%" class="center"/></div>
            <div></div>
        </div>

        <div className="video-feed">

        </div>

        {/* turret controls */}
        <div className="grid-container">
            <div></div>
            <div className="grid-item" id="u-aim" onClick={() => {validate_and_send('up')}}><img src={UpDouble} width="80%" height="80%" class="center"/></div>
            <div></div>
            <div className="grid-item" id="l-aim" onClick={() => {validate_and_send('l-aim')}}><img src={LeftDouble} width="80%" height="80%" class="center"/></div>
            <div className="grid-fire" id="fire" onClick={() => {validate_and_send('fire!')}}><img src={BulletSingle} width="80%" height="80%" class="center"/></div>
            <div className="grid-item" id="r-aim" onClick={() => {validate_and_send('r-aim')}}><img src={RightDouble} width="80%" height="80%" class="center"/></div>
            <div></div>
            <div className="grid-item" id="d-aim" onClick={() => {validate_and_send('down')}}><img src={DownDouble} width="80%" height="80%" class="center"/></div>
            <div className="grid-fire" id="burst" onClick={() => {validate_and_send('burst')}}><img src={BulletBurst} width="80%" height="80%" class="center"/></div>
        </div>
      </div>
      
      {/* misc buttons container */}
      <div className="main-container">
        
        {/* Connection container */}
        <div className="block-container">
          <div className="small-title">Connection</div>
          <div className="secondary-grid-container">
            <div className="rectangle-buttons" onClick={() => {validate_and_send('connect')}}><img src={OnSwitch} width="60%" height="100%" class="center"/></div>
            <div className="rectangle-buttons" onClick={() => {validate_and_send('disconnect')}}><img src={OffSwitch} width="60%" height="100%" class="center"/></div>
          </div>
        </div>

        {/* Laser container */}
        <div className="block-container">
          <div className="small-title">Laser</div>
          <div className="secondary-grid-container">
            <div className="rectangle-buttons" onClick={() => {validate_and_send('laser-off')}}><img src={OffSwitch} width="60%" height="100%" class="center"/></div>
            <div className="rectangle-buttons" onClick={() => {validate_and_send('laser-on')}}><img src={OnSwitch} width="60%" height="100%" class="center"/></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
