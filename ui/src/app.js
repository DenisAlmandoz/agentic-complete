const API_URL = window.localStorage.getItem('LANG_TUTOR_API_URL') || 'http://localhost:8000';

const elements = {
  targetLanguage: document.querySelector('#targetLanguage'),
  topic: document.querySelector('#topic'),
  agent: document.querySelector('#agent'),
  message: document.querySelector('#message'),
  sendButton: document.querySelector('#sendButton'),
  response: document.querySelector('#response'),
};

elements.sendButton.addEventListener('click', async () => {
  elements.response.textContent = 'Thinking...';
  const payload = {
    user_id: 'demo-user',
    target_language: elements.targetLanguage.value,
    topic: elements.topic.value,
    message: elements.message.value,
    requested_agent: elements.agent.value || null,
  };

  try {
    const response = await fetch(`${API_URL}/tutor/turn`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    elements.response.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    elements.response.textContent = `Could not reach API: ${error.message}`;
  }
});
