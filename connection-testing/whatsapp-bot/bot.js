const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const CerberusClient = require('../nodejs/test_api');

const CERBERUS_API_KEY = process.env.CERBERUS_API_KEY || 'your-api-key-here';
const cerberus = new CerberusClient(CERBERUS_API_KEY);

const whatsapp = new Client({
  authStrategy: new LocalAuth()
});

// Armazena sessões por número de telefone
const userSessions = new Map();

whatsapp.on('qr', (qr) => {
  console.log('📱 Escaneie o QR Code:');
  qrcode.generate(qr, { small: true });
});

whatsapp.on('ready', () => {
  console.log('✅ WhatsApp Bot conectado!');
  console.log('🤖 Cerberus AI pronto para responder');
});

whatsapp.on('message', async (msg) => {
  if (msg.from.includes('@g.us')) return;
  if (msg.fromMe) return;

  const userId = msg.from;
  const question = msg.body;

  try {
    if (!userSessions.has(userId)) {
      const client = new CerberusClient(CERBERUS_API_KEY);
      userSessions.set(userId, client);
      console.log(`🆕 Nova sessão criada para ${userId}`);
    }

    const client = userSessions.get(userId);
    
    msg.reply('🤔 Pensando...');

    const answer = await client.ask(question);
    const content = answer.choices[0].message.content;
    
    await msg.reply(content);
    
    console.log(`✅ Resposta enviada para ${userId}`);
  } catch (error) {
    console.error('❌ Erro:', error.message);
    await msg.reply('Desculpe, ocorreu um erro ao processar sua mensagem.');
  }
});

whatsapp.initialize();

console.log('🚀 Iniciando WhatsApp Bot com Cerberus AI...');
