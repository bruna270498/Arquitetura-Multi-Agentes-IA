
// ── URL do seu FastAPI ──────────────────────────────────────────
const API_URL = 'https://arquitetura-multi-agentes-ia-787425613859.us-central1.run.app/chat'; // em produção troque pela URL do Cloud Run

let isOpen = false;
let isTyping = false;
let clienteId = "user_" + Math.random().toString(36).substr(2, 9);
let firstOpen = true;

function toggleChat() {
    isOpen = !isOpen;
    document.getElementById('chat-panel').classList.toggle('open', isOpen);
    if (isOpen && firstOpen) {
        firstOpen = false;
        setTimeout(() => greetUser(), 400); 
    }
}

function openChat() {
    if (!isOpen) toggleChat();
}

function greetUser() {
    addMessage("bot", "Olá! 👋 Sou o **PSS**, assistente da PowerSeg Soluções.\n\nPosso te ajudar com informações sobre nossos serviços, gerar um orçamento ou agendar uma visita técnica. Como posso te ajudar hoje?");
}

function addMessage(role, text) {
    const msgs = document.getElementById('chat-messages');
    const quickReplies = document.getElementById('quick-replies');
    if (role === 'user' && quickReplies) quickReplies.style.display = 'none';

    const div = document.createElement('div');
    div.className = `msg ${role}`;

    const avDiv = document.createElement('div');
    avDiv.className = 'msg-avatar' + (role === 'user' ? ' user-av' : '');
    if (role === 'bot') {
      avDiv.innerHTML = '<img src="avatar.jpeg" alt="PSS" onerror="this.style.display=\'none\'"/>';
    } else {
      avDiv.textContent = 'V';
    }

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');

    div.appendChild(avDiv);
    div.appendChild(bubble);
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
    const msgs = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'msg bot';
    div.id = 'typing-indicator';
    const avDiv = document.createElement('div');
    avDiv.className = 'msg-avatar';
    avDiv.innerHTML = '<img src="avatar.jpeg" alt="" onerror="this.style.display=\'none\'"/>';
    const bubble = document.createElement('div');
    bubble.className = 'typing';
    bubble.innerHTML = '<span></span><span></span><span></span>';
    div.appendChild(avDiv);
    div.appendChild(bubble);
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

function sendQuick(text) {
    document.getElementById('chat-input').value = text;
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text || isTyping) return;

    input.value = '';
    input.style.height = 'auto';
    addMessage('user', text);

    isTyping = true;
    document.getElementById('chat-send').disabled = true;
    showTyping();

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: text, cliente_id: clienteId })
      });

      if (!res.ok) throw new Error("Erro " + res.status);
      const data = await res.json();
      removeTyping();
      addMessage('bot', data.resposta);

    } catch (err) {
      removeTyping();
      addMessage('bot', "Ops! Não consegui me conectar agora. Tente novamente ou fale pelo WhatsApp. 📱");
      console.error(err);
    }

    isTyping = false;
    document.getElementById('chat-send').disabled = false;
    input.focus();
}

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}