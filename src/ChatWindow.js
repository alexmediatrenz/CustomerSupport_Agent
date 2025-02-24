import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';
import styles from './ChatWindow.module.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const chatHistoryRef = useRef(null);

  // Initialize chat with a conversation ID and welcome message
  useEffect(() => {
    setConversationId(uuidv4());
    setMessages([{ sender: 'bot', text: "Hello! I'm the Mediatrenz support assistant. How can I help you today?" }]);
  }, []);

  // Auto-scroll to the latest message
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]);

  // Function to send a message to the backend
  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message to chat history
    setMessages((prev) => [...prev, { sender: 'user', text: messageText }]);
    setIsTyping(true);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conversation_id: conversationId, message: messageText }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setIsTyping(false);
      setMessages((prev) => [...prev, { sender: 'bot', text: data.response }]);
    } catch (error) {
      setIsTyping(false);
      setMessages((prev) => [...prev, { sender: 'bot', text: 'Sorry, there was an error. Please try again later.' }]);
    }
  };

  // Handle send button click
  const handleSend = () => {
    sendMessage(input);
    setInput('');
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  // Quick reply options
  const quickReplies = [
    { label: 'Services', message: 'What services do you offer?' },
    { label: 'Contact', message: 'How can I contact support?' },
    { label: 'Hours', message: 'What are your business hours?' },
    { label: 'Urgent', message: 'I have an urgent issue.' },
  ];

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <h1>Mediatrenz Customer Support</h1>
      </div>
      <div className={styles.chatHistory} ref={chatHistoryRef} role="log" aria-live="polite">
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
            {msg.text}
          </div>
        ))}
        {isTyping && <TypingIndicator />}
      </div>
      <div className={styles.quickReplies}>
        {quickReplies.map((qr, index) => (
          <button key={index} onClick={() => sendMessage(qr.message)}>
            {qr.label}
          </button>
        ))}
      </div>
      <div className={styles.inputArea}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

// Typing indicator component
const TypingIndicator = () => (
  <div className={styles.typingIndicator}>
    <span></span><span></span><span></span>
  </div>
);

export default ChatWindow;
