import React, { useState } from 'react';
import '../styles/ChatWidget.css';

const ChatWidget = () => {
 const [message, setMessage] = useState('');
 const [messages, setMessages] = useState([]);

 const handleSubmit = async (e) => {
   e.preventDefault();
   if (!message.trim()) return;

   setMessages([...messages, { text: message, isUser: true }]);
   
   try {
     const response = await fetch('http://localhost:8000/api/chat/chat', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({ message })
     });
     
     const data = await response.json();
     setMessages(prev => [...prev, { text: data.response, isUser: false }]);
   } catch (error) {
     console.error('Error:', error);
     setMessages(prev => [...prev, { 
       text: "Mi dispiace, si è verificato un errore. Riprova più tardi.", 
       isUser: false 
     }]);
   }
   
   setMessage('');
 };

 return (
   <div className="chat-widget-container">
     <div className="chat-widget">
       <div className="chat-messages">
         {messages.map((msg, idx) => (
           <div key={idx} className={`message ${msg.isUser ? 'user' : 'bot'}`}>
             {msg.text}
           </div>
         ))}
       </div>
       <form className="chat-input" onSubmit={handleSubmit}>
         <input
           value={message}
           onChange={(e) => setMessage(e.target.value)}
           placeholder="Scrivi un messaggio..."
           autoFocus
         />
         <button type="submit">Invia</button>
       </form>
     </div>
   </div>
 );
};

export default ChatWidget;