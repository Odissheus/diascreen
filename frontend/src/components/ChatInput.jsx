// ChatInput.jsx
import { useState } from 'react';
import styled from '@emotion/styled';

const InputContainer = styled.div`
 padding: 10px;
 background: white;
 border-top: 1px solid #e9ecef;
 display: flex;
`;

const Input = styled.input`
 flex: 1;
 padding: 8px 12px;
 border: 1px solid #ced4da;
 border-radius: 4px;
 margin-right: 8px;
`;

const Button = styled.button`
 padding: 8px 16px;
 background: #007bff;
 color: white;
 border: none;
 border-radius: 4px;
 cursor: pointer;
 &:hover { background: #0056b3; }
`;

const ChatInput = ({ onSendMessage }) => {
 const [message, setMessage] = useState('');

 const handleSubmit = (e) => {
   e.preventDefault();
   if (message.trim()) {
     onSendMessage(message);
     setMessage('');
   }
 };

 return (
   <InputContainer>
     <form onSubmit={handleSubmit} style={{ display: 'flex', width: '100%' }}>
       <Input
         value={message}
         onChange={(e) => setMessage(e.target.value)}
         placeholder="Scrivi un messaggio..."
       />
       <Button type="submit">Invia</Button>
     </form>
   </InputContainer>
 );
};

export default ChatInput;