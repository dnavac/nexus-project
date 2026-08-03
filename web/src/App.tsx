import { useState, useRef, useEffect } from 'react';
import { SideNavBar } from './components/SideNavBar';

const NEXUS_LOGO = 'https://lh3.googleusercontent.com/aida-public/AB6AXuCM5lIIkVeyYMd_MEIS8gXIF4iSIrQ3BApD7VSdK27Hq8Uy78RFpkEofT4R2kfdGziWLOJAc2EYUjeysN0At9T8NttsfZDVRz43d8mLx-_P9KazaL4wc1W1Sn4HZE5CYqEbc3ZiKMBPPP8dIYOJg2_qZJp4urgM3FNgIE9Wy8aS_y2cpuZiaUnHE8ofrVTQNTrgpwmrkNLgb8TuiHgsJDrjzWpJVJcA5EXPKQF5VVc56lnt3aFw6AA6Aw';

interface Message {
  role: 'assistant' | 'user';
  content: string;
}

// Generate a unique session ID for this browser session
const SESSION_ID = `session_${Date.now()}`;
const API_URL = 'http://127.0.0.1:8080/api/chat/conversational';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Bienvenido a Nexus Premium. Soy tu asistente personal de IA. ¿En qué puedo ayudarte hoy con tu búsqueda de inmuebles en Cartagena?',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || isLoading) return;

    // Add user message
    const userMsg: Message = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: SESSION_ID, message: text }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Lo siento, pero he tenido un problema al conectarme al servidor. Por favor, inténtalo de nuevo dentro de un momento.',
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      <SideNavBar />

      {/* Main Chat Hub */}
      <main className="flex-1 flex flex-col relative lg:ml-72 h-full">

        {/* Header */}
        <header className="glass-panel sticky top-0 z-30 px-container-padding-desktop py-4 flex items-center justify-between border-b border-white/5">
          <div className="flex items-center gap-element-gap">
            <img alt="NEXUS Logo" className="h-10 w-10 object-contain rounded-md" src={NEXUS_LOGO} />
            <div>
              <h1 className="font-headline-md text-on-surface text-headline-md">Nexus AI Concierge</h1>
              <div className="flex items-center gap-2 mt-1">
                <div className="w-2 h-2 rounded-full bg-secondary-container shadow-[0_0_8px_rgba(5,102,217,0.8)]"></div>
                <span className="text-label-sm text-secondary font-label-sm uppercase tracking-wider">Online | Knowledge Base Connected</span>
              </div>
            </div>
          </div>
          <div className="flex gap-4">
            <button className="p-2 rounded-full hover:bg-white/10 transition-colors">
              <span className="material-symbols-outlined text-on-surface-variant">history</span>
            </button>
            <button className="p-2 rounded-full hover:bg-white/10 transition-colors">
              <span className="material-symbols-outlined text-on-surface-variant">more_vert</span>
            </button>
          </div>
        </header>

        {/* Chat Canvas */}
        <div className="flex-1 overflow-y-auto px-container-padding-mobile md:px-container-padding-desktop py-12 flex flex-col gap-8 pb-40">

          {messages.map((msg, idx) => (
            msg.role === 'assistant' ? (
              /* ── Bot Message ── */
              <div key={idx} className="flex gap-4 max-w-3xl self-start msg-animate">
                <div className="w-10 h-10 rounded-full glass-panel flex-shrink-0 flex items-center justify-center border border-white/10">
                  <img alt="NEXUS" className="w-6 h-6 object-contain" src={NEXUS_LOGO} />
                </div>
                <div className="glass-popover p-6 rounded-2xl rounded-tl-sm border-l-2 border-tertiary-fixed-dim">
                  <p className="font-body-md text-on-surface text-body-lg">{msg.content}</p>
                </div>
              </div>
            ) : (
              /* ── User Message ── */
              <div key={idx} className="flex gap-4 max-w-3xl self-end flex-row-reverse msg-animate">
                <div className="w-10 h-10 rounded-full bg-surface-container-highest flex-shrink-0 flex items-center justify-center border border-white/10">
                  <span className="material-symbols-outlined text-on-surface text-sm">person</span>
                </div>
                <div className="p-6 rounded-2xl rounded-tr-sm bg-gradient-to-br from-secondary-container to-surface shadow-[0_0_30px_rgba(5,102,217,0.15)] border border-secondary-container/30">
                  <p className="font-body-md text-white text-body-lg">{msg.content}</p>
                </div>
              </div>
            )
          ))}

          {/* Typing indicator */}
          {isLoading && (
            <div className="flex gap-4 max-w-3xl self-start items-center msg-animate">
              <div className="w-10 h-10 rounded-full glass-panel flex-shrink-0 flex items-center justify-center border border-white/10">
                <img alt="NEXUS" className="w-6 h-6 object-contain" src={NEXUS_LOGO} />
              </div>
              <div className="glass-popover p-4 rounded-2xl rounded-tl-sm flex items-center gap-2 w-20 h-12">
                <div className="w-2 h-2 rounded-full bg-secondary-container typing-dot"></div>
                <div className="w-2 h-2 rounded-full bg-secondary-container typing-dot"></div>
                <div className="w-2 h-2 rounded-full bg-secondary-container typing-dot"></div>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 left-0 w-full p-container-padding-mobile md:p-container-padding-desktop bg-gradient-to-t from-surface via-surface/90 to-transparent">
          <div className="max-w-4xl mx-auto glass-popover rounded-2xl flex items-center p-2 border border-white/10 focus-within:border-secondary-container/50 focus-within:shadow-[0_0_15px_rgba(5,102,217,0.3)] transition-all">
            <button className="p-3 text-on-surface-variant hover:text-secondary transition-colors rounded-xl">
              <span className="material-symbols-outlined">attach_file</span>
            </button>
            <textarea
              className="flex-1 bg-transparent border-none outline-none focus:ring-0 text-on-surface resize-none font-body-md placeholder-on-surface-variant/50 py-3 px-2 h-[48px]"
              placeholder="Ask Nexus..."
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
            />
            <div className="flex items-center gap-2 pr-2">
              <button className="p-3 text-on-surface-variant hover:text-secondary transition-colors rounded-xl">
                <span className="material-symbols-outlined">mic</span>
              </button>
              <button
                onClick={sendMessage}
                disabled={isLoading || !input.trim()}
                className="p-3 bg-tertiary-fixed-dim text-tertiary-container rounded-xl hover:bg-tertiary transition-colors shadow-lg shadow-tertiary-fixed-dim/20 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
              </button>
            </div>
          </div>
          <p className="text-center mt-4 text-[11px] text-on-surface-variant/50 font-label-sm uppercase tracking-widest">
            Nexus AI may produce inaccurate information about properties or market data.
          </p>
        </div>
      </main>
    </>
  );
}

export default App;
