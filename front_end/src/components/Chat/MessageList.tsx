import React, {useEffect, useRef} from 'react';
import ChatMessage from './ChatMessage';
import './MessageList.css';

interface ChatMessageProps {
  role: string;
  content: string;
}

interface MessageListProps {
    messages: ChatMessageProps[];

}

const MessageList: React.FC<MessageListProps> = ({ messages}) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({behavior: 'smooth'});
    };
    useEffect(() => {
        scrollToBottom();
    }, [messages]);
    return (
        <div className = "message-list">
            {messages.length === 0 ? (
                <div className = "empty-state">
                    <div className = "empty-state-content">
                        <div className = "empty-state-icon">💬</div>
                        <h3>Start Conversation</h3>
                        <p>Ask me anything to get started</p>
                    </div>
                </div>
            ): (
                <>
                    {messages.map((message, index) => (
                        <ChatMessage
                            key = {index}
                            role = {message.role}
                            content = {message.content}
                        />
                    ))}
                    <div ref = {messagesEndRef} />
                </>
            )}
        </div>
    );
};

export default MessageList;