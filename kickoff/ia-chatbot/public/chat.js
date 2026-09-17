const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('message-input');

const history = [];

function addMessage(role, text) {
  const el = document.createElement('div');
  el.className = `message ${role === 'user' ? 'user' : 'bot'}`;
  el.textContent = text;
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

formEl.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = inputEl.value.trim();
  if (!message) return;

  addMessage('user', message);
  inputEl.value = '';
  inputEl.disabled = true;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Error desconocido');
    }

    addMessage('bot', data.reply);
    history.push({ role: 'user', parts: [{ text: message }] });
    history.push({ role: 'model', parts: [{ text: data.reply }] });
  } catch (error) {
    addMessage('bot', `⚠️ ${error.message}`);
  } finally {
    inputEl.disabled = false;
    inputEl.focus();
  }
});
