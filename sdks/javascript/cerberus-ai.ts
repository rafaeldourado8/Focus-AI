/**
 * Cerberus AI JavaScript SDK
 * 
 * Official JavaScript/TypeScript client for Cerberus AI API
 */

interface Message {
  role: string;
  content: string;
}

interface ChatCompletionOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  debugMode?: boolean;
}

interface CodeAnalyzeOptions {
  checks?: string[];
}

interface CodeRefactorOptions {
  goals?: string[];
}

export class CerberusAI {
  private apiKey: string;
  private baseUrl: string;

  constructor(apiKey: string, baseUrl: string = 'http://localhost:8000') {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async request(endpoint: string, options: RequestInit = {}): Promise<any> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Create a chat completion
   */
  async chatCompletion(
    messages: Message[],
    options: ChatCompletionOptions = {}
  ): Promise<any> {
    return this.request('/v1/chat/completions', {
      method: 'POST',
      body: JSON.stringify({
        messages,
        model: options.model || 'cerberus-pro',
        temperature: options.temperature || 0.7,
        max_tokens: options.maxTokens || 2048,
        debug_mode: options.debugMode || false,
      }),
    });
  }

  /**
   * Analyze code for issues
   */
  async analyzeCode(
    code: string,
    language: string,
    options: CodeAnalyzeOptions = {}
  ): Promise<any> {
    return this.request('/v1/code/analyze', {
      method: 'POST',
      body: JSON.stringify({
        code,
        language,
        checks: options.checks || ['security', 'performance', 'style'],
      }),
    });
  }

  /**
   * Debug code with error
   */
  async debugCode(
    error: string,
    code: string,
    language: string,
    context?: string
  ): Promise<any> {
    return this.request('/v1/code/debug', {
      method: 'POST',
      body: JSON.stringify({
        error,
        code,
        language,
        context,
      }),
    });
  }

  /**
   * Refactor code
   */
  async refactorCode(
    code: string,
    language: string,
    options: CodeRefactorOptions = {}
  ): Promise<any> {
    return this.request('/v1/code/refactor', {
      method: 'POST',
      body: JSON.stringify({
        code,
        language,
        goals: options.goals || ['readability', 'maintainability'],
      }),
    });
  }

  /**
   * List available models
   */
  async listModels(): Promise<any> {
    return this.request('/v1/models', { method: 'GET' });
  }

  /**
   * Get usage statistics
   */
  async getUsage(): Promise<any> {
    return this.request('/v1/usage', { method: 'GET' });
  }
}

export default CerberusAI;
