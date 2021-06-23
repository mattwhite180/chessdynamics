import logo from './logo.svg';
import './App.css';
import Chessground from 'react-chessground'
import 'react-chessground/dist/styles/chessground.css'

function App() {
  return (
    <div className="App">
      <header className="ChessDynamics">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        return <Chessground />
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
