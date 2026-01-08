import { useEffect, useState } from 'react';
import CerberusIcon from './CerberusIcon';

const Login = ({ onLogin }) => {
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
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
          width: 300,
          text: 'continue_with',
          shape: 'rectangular',
          logo_alignment: 'left'
        }
      );
    };

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const handleGoogleLogin = async (response) => {
    setIsLoading(true);
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
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      {/* Subtle background effect */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-red-950/20 via-transparent to-transparent opacity-50" />
      </div>

      <div className="relative z-10 w-full max-w-sm animate-fade-in">
        {/* Logo */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center mb-4">
            <CerberusIcon className="w-12 h-12 text-white" />
          </div>
          <h1 className="text-2xl font-semibold tracking-tight text-white">
            Cerberus AI
          </h1>
          <p className="text-cerberus-text-secondary text-sm mt-2">
            Guardian of Knowledge
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-cerberus-dark border border-cerberus-border rounded-2xl p-8">
          <div className="text-center mb-6">
            <h2 className="text-lg font-medium text-white">
              Bem-vindo
            </h2>
            <p className="text-cerberus-text-muted text-sm mt-1">
              Entre para continuar
            </p>
          </div>

          {/* Google Button Container */}
          <div className="flex justify-center">
            {isLoading ? (
              <div className="flex items-center justify-center h-10 text-cerberus-text-secondary">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle 
                    className="opacity-25" 
                    cx="12" 
                    cy="12" 
                    r="10" 
                    stroke="currentColor" 
                    strokeWidth="4"
                    fill="none"
                  />
                  <path 
                    className="opacity-75" 
                    fill="currentColor" 
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
              </div>
            ) : (
              <div id="googleButton" />
            )}
          </div>

          {/* Terms */}
          <p className="text-2xs text-cerberus-text-muted text-center mt-6 leading-relaxed">
            Ao continuar, você concorda com os{' '}
            <span className="text-cerberus-text-secondary hover:text-white cursor-pointer transition-colors">
              Termos de Serviço
            </span>
            {' '}e{' '}
            <span className="text-cerberus-text-secondary hover:text-white cursor-pointer transition-colors">
              Política de Privacidade
            </span>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-2xs text-cerberus-text-muted mt-6">
          Cerberus AI © 2025
        </p>
      </div>
    </div>
  );
};

export default Login;
