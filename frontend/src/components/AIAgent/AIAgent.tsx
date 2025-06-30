import { faCommentDots, faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React, { useState, useRef, useEffect } from 'react';
import './AIAgent.scss';
import { Container } from 'react-bulma-components';

type Message = {
  id: number;
  role: 'user' | 'model';
  content: string;
  isLoading?: boolean;
};

export const AIAgent: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'model',
      content:
        "Hi! I'm an AI assistant in training. Soon, I'll be able to help you find the perfect pet.",
    },
  ]);
  const [userInput, setUserInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    // Scroll to bottom whenever a new message is added
    if (isOpen) {
      setTimeout(scrollToBottom, 100);
    }
  }, [messages, isOpen]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedInput = userInput.trim();
    if (trimmedInput === '') return;

    const newUserMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: trimmedInput,
    };
    setMessages(prev => [...prev, newUserMessage]);
    setUserInput('');

    // Add a placeholder for the AI's response with a loading indicator
    const loadingMessageId = Date.now() + 1;
    setMessages(prev => [
      ...prev,
      { id: loadingMessageId, role: 'model', content: '', isLoading: true },
    ]);

    // Simulate an API call delay
    setTimeout(() => {
      const devMessage = 'Sorry, this feature is still in development.';
      setMessages(prev =>
        prev.map(msg =>
          msg.id === loadingMessageId
            ? { ...msg, content: devMessage, isLoading: false }
            : msg,
        ),
      );
    }, 1500); // 1.5-second delay to simulate a response
  };

  return (
    <>
      {!isOpen && (
        <button
          className="pet-chatbot-bubble"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
        >
          <span className="icon">
            <FontAwesomeIcon icon={faCommentDots} />
          </span>
        </button>
      )}

      <Container className={`pet-chatbot-window ${isOpen ? 'is-open' : ''}`}>
        <header className="chat-header">
          <div className="ai-avatar">AI</div>
          <p className="header-title">Pet Finder Assistant</p>
          <button
            className="close-button"
            aria-label="close"
            onClick={() => setIsOpen(false)}
          >
            &times;
          </button>
        </header>

        <main className="chat-body">
          {messages.map(msg => (
            <div
              key={msg.id}
              className={`message-container ${msg.role === 'user' ? 'is-user' : 'is-model'}`}
            >
              <div className="message-bubble">
                {msg.isLoading ? (
                  <div className="dot-flashing"></div>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </main>

        <footer className="chat-footer">
          <form
            onSubmit={handleSendMessage}
            className="chat-input-form"
          >
            <input
              className="chat-input"
              type="text"
              placeholder="Type a message..."
              value={userInput}
              onChange={e => setUserInput(e.target.value)}
              aria-label="Chat input"
            />
            <button
              className="send-button"
              type="submit"
              aria-label="Send message"
              disabled={userInput.trim() === ''}
            >
              <FontAwesomeIcon icon={faPaperPlane} />
            </button>
          </form>
        </footer>
      </Container>
    </>
  );
};
