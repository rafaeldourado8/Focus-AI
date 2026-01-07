import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain } from 'lucide-react';
import BackgroundGradient from './BackgroundGradient';

const Login = ({ onLogin }) => {
  useEffect(() => {
    // Carregar Google Identity Services
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    script.onload = () => {
      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID || '64508171271-dve9dqr6sig268kdnupn1psi5k9ld518.apps.googleusercontent.com',
        callback: handleGoogleLogin
      });

      window.google.accounts.id.renderButton(
        document.getElementById('googleButton'),
        { 
          theme: 'filled_black',
          size: 'large',
          width: 350,
          text: 'signin_with',
          shape: 'rectangular'
        }
      );
    };

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const handleGoogleLogin = async (response) => {
    try {
      const res = await fetch('http://localhost:8000/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: response.credential })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Erro ao fazer login');

      localStorage.setItem('token', data.access_token);
      onLogin(data.access_token);
    } catch (err) {
      console.error('Login error:', err);
      alert('Erro ao fazer login com Google');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center text-white relative bg-black">
      <BackgroundGradient />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md px-6 relative z-10"
      >
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <Brain className="w-10 h-10 text-indigo-500" />
            <span className="text-3xl font-bold tracking-tighter">Focus AI</span>
          </div>
          <p className="text-zinc-600 text-sm">
            Aprendizado profundo com metodologia socrática
          </p>
        </div>

        <div className="bg-zinc-950 border border-zinc-900 rounded-2xl p-8 shadow-2xl">
          <div className="flex flex-col items-center gap-6">
            <h2 className="text-xl font-semibold">Entre para continuar</h2>
            
            <div id="googleButton" className="w-full flex justify-center"></div>
            
            <p className="text-xs text-zinc-600 text-center">
              Ao continuar, você concorda com nossos Termos de Serviço e Política de Privacidade
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;
