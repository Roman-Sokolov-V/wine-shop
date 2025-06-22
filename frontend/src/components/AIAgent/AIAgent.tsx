import { faMessage } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React, { useState, useRef, useEffect } from 'react';
import './AIAgent.scss';

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

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (userInput.trim() === '') return;

    const newUserMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: userInput,
    };
    setMessages(prev => [...prev, newUserMessage]);
    setUserInput('');

    const loadingMessageId = Date.now() + 1;
    setMessages(prev => [
      ...prev,
      { id: loadingMessageId, role: 'model', content: '', isLoading: true },
    ]);

    setTimeout(() => {
      const devMessage = 'Sorry, this feature is still in development.';
      setMessages(prev =>
        prev.map(msg =>
          msg.id === loadingMessageId
            ? { ...msg, content: devMessage, isLoading: false }
            : msg,
        ),
      );
    }, 1200); // 1.2-second delay to simulate a response
  };

  return (
    <div>
      {!isOpen && (
        <button
          className="button is-info is-large is-rounded pet-chatbot-bubble"
          onClick={() => setIsOpen(true)}
        >
          <span className="icon">
            <FontAwesomeIcon
              icon={faMessage}
              className="has-text-white pl-1"
            />
          </span>
        </button>
      )}

      <div className={`pet-chatbot-window ${isOpen ? 'is-open' : ''}`}>
        <div
          className="box"
          style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
        >
          <header className="modal-card-head">
            <p className="modal-card-title">Pet Finder Assistant</p>
            <button
              className="delete"
              aria-label="close"
              onClick={() => setIsOpen(false)}
            ></button>
          </header>

          <section
            className="modal-card-body is-flex-grow-1"
            style={{ overflowY: 'auto' }}
          >
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`mb-4 ${msg.role === 'user' ? 'has-text-right' : ''}`}
              >
                <div
                  className={`box is-inline-block ${msg.role === 'model' ? 'has-background-white' : 'has-background-primary-light'}`}
                >
                  {msg.isLoading ? (
                    <div className="dot-flashing"></div>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </section>

          <footer className="modal-card-foot">
            <form
              onSubmit={handleSendMessage}
              style={{ flexGrow: 1 }}
            >
              <div className="field has-addons">
                <div className="control is-expanded">
                  <input
                    className="input"
                    type="text"
                    placeholder="Type a message..."
                    value={userInput}
                    onChange={e => setUserInput(e.target.value)}
                  />
                </div>
                <div className="control">
                  <button
                    className="button is-primary"
                    type="submit"
                  >
                    Send
                  </button>
                </div>
              </div>
            </form>
          </footer>
        </div>
      </div>
    </div>
  );
};
