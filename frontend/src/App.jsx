import './App.css'
import ChatWidget from './components/ChatWidget'

// Aggiungiamo uno stile minimo per il corpo
const bodyStyle = {
 margin: 0,
 padding: 20,
 minHeight: '100vh',
 background: '#f5f5f5'
}

function App() {
 return (
   <div style={bodyStyle}>
     <h1>Assistente Diabete - Demo</h1>
     <ChatWidget />
   </div>
 )
}

export default App