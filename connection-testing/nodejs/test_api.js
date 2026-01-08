const axios = require('axios');

class CerberusClient {
  constructor(apiKey, baseUrl = 'http://localhost:8000') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
    this.messages = [];
    this.client = axios.create({
      baseURL: baseUrl,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async ask(question, debugMode = false) {
    this.messages.push({ role: 'user', content: question });

    const { data } = await this.client.post('/v1/chat/completions', {
      model: 'cerberus-pro',
      messages: this.messages,
      debug_mode: debugMode
    });

    const assistantMsg = data.choices[0].message.content;
    this.messages.push({ role: 'assistant', content: assistantMsg });

    return data;
  }

  async analyzeCode(code, language, checks = ['security', 'performance', 'style']) {
    const { data } = await this.client.post('/v1/code/analyze', {
      code,
      language,
      checks
    });
    return data;
  }

  async debugCode(error, code, language, context = null) {
    const { data } = await this.client.post('/v1/code/debug', {
      error,
      code,
      language,
      context
    });
    return data;
  }

  async getModels() {
    const { data } = await this.client.get('/v1/models');
    return data;
  }
}

// Teste básico
(async () => {
  const API_KEY = 'your-api-key-here';
  const client = new CerberusClient(API_KEY);

  console.log('💬 Enviando pergunta...');
  const answer = await client.ask('Como implementar JWT em FastAPI?');
  console.log(`✅ Resposta: ${answer.choices[0].message.content.substring(0, 100)}...`);
  console.log(`📊 Tokens: ${answer.usage.total_tokens}`);

  console.log('\n🔍 Listando modelos...');
  const models = await client.getModels();
  console.log(`✅ ${models.models.length} modelos disponíveis`);
})();

module.exports = CerberusClient;
