// ChatMessage.jsx
import styled from '@emotion/styled'

const MessageContainer = styled.div`
  padding: 10px;
  margin: 5px;
  max-width: 80%;
  word-wrap: break-word;
  ${props => props.isUser ? 'margin-left: auto; background-color: #007bff; color: white;' : 'margin-right: auto; background-color: #f8f9fa;'}
  border-radius: 10px;
`;

export default function ChatMessage({ message, isUser }) {
  return (
    <MessageContainer isUser={isUser}>
      {message}
    </MessageContainer>
  )
}