import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './ChatMessage.css';

interface ChatMessageProps {
  role: string;
  content: string;
}

// Définir le type pour les props du composant code
interface CodeProps {
  node?: any;
  inline?: boolean;
  className?: string;
  children?: React.ReactNode;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ role, content }) => {
  return (
    <div className={`chat-message ${role === 'user' ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {role === 'user' ? (
          <p>{content}</p>
        ) : (
          <ReactMarkdown
            components={{
              code: ({ inline, className, children }: CodeProps) => {
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={match[1]}
                    PreTag="div"
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className}>
                    {children}
                  </code>
                );
              }
            }}
          >
            {content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
