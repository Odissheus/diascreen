// ChatWidget.jsx
import { useState } from 'react';
import styled from '@emotion/styled';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { sendMessage } from './api';

const Widget = styled.div`
 position: fixed;
 bottom: 20px;
 right: 20px;
 width: 350px;
 height: 500px;
 border-radius: 10px;
 box-shadow: 0 0 10px rgba(0,0,0,0.1);
 display: flex;
 flex-direction: column;
 overflow: hidden;
 background: white;
`;

const Header = styled.div`
 background: #007bff;
 color: white;
 padding: 15px;
 font-weight: bold;
`;

const MessagesContainer = styled.div`
 flex: 1;
 overflow-y: auto;
 padding: 10px;
 display: flex;
 flex-direction: column;
`;

const ChatWidget = () => {
 const [messages, setMessages] = useState([]);

 const handleSendMessage = async (text) => {
   const userMessage = { text, isUser: true };
   setMessages(prev => [...prev, userMessage]);

   try {
     const response = await sendMessage(text);
     const botMessage = { text: response, isUser: false };
     setMessages(prev => [...prev, botMessage]);
   } catch (error) {
     console.error('Error:', error);
     const errorMessage = { 
       text: 'Mi dispiace, si è verificato un errore. Riprova più tardi.', 
       isUser: false 
     };
     setMessages(prev => [...prev, errorMessage]);
   }
 };

 return (
   <Widget>
     <Header>Assistente Diabete</Header>
     <MessagesContainer>
       {messages.map((message, index) => (
         <ChatMessage
           key={index}
           message={message.text}
           isUser={message.isUser}
         />
       ))}
     </MessagesContainer>
     <ChatInput onSendMessage={handleSendMessage} />
   </Widget>
 );
};

export default ChatWidget;