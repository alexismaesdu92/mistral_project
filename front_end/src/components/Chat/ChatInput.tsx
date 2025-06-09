import React, {useState, FormEvent, KeyboardEvent, useCallback} from 'react';
import Button from '../common/Button';
import ToggleSwitch from '../common/ToggleSwitch';
import './ChatInput.css';

interface ChatInputProps {
    onSendMessage: (message: string, useRag: boolean) => void;
    isLoading?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({onSendMessage, isLoading = false}) => {
    const [message, setMessage] = useState('');
    const [ragEnabled, setRagEnabled] = useState(false);

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (message.trim() && !isLoading){
            onSendMessage(message, ragEnabled);
            setMessage('');
        }
    };
    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    // Utiliser useCallback pour éviter les re-rendus inutiles
    const toggleRag = useCallback(() => {
        setRagEnabled(prevState => !prevState);
    }, []);

    return (
        <form className = "chat-input-container" onSubmit = {handleSubmit}>
            <div className="chat-input-controls" onClick={e => e.stopPropagation()}>
                <ToggleSwitch 
                    isOn={ragEnabled}
                    handleToggle={toggleRag}
                    label="RAG"
                    disabled={isLoading}
                    title={ragEnabled ? "Désactiver RAG" : "Activer RAG"}
                />
            </div>
            <textarea
                className = "chat-input"
                value = {message}
                onChange = {(e) => setMessage(e.target.value)}
                onKeyDown = {handleKeyDown}
                placeholder = "Type your message..."
                disabled = {isLoading}
                rows={1}

            />
            <Button
                type="submit"
                buttonType="primary"
                size="large"
                disabled={!message.trim() || isLoading}
            >
                {isLoading ? 'Sending...' : 'Send'}
            </Button>
        </form>
    );
};

export default ChatInput;
