import React from 'react';
import './App.css';
import ChatInput from './components/Chat/ChatInput';
import MessageList from './components/Chat/MessageList';
import { useChat } from './hooks/useChat';

function App() {

  const { messages, isLoading, error, sendMessage } = useChat();

  const handleSendMessage = (message: string, useRag: boolean) => {
    sendMessage(message, useRag);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Documentation Assistant</h1>
      </header>
      <main className="App-main">
        <div className="chat-container">
          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}
          <MessageList messages={messages} />
          <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
      </main>
    </div>
  );
}

export default App;
