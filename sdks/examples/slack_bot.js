/**
 * Slack Bot Example using Cerberus AI
 * 
 * Requires: @slack/bolt, @cerberus-ai/sdk
 */

const { App } = require('@slack/bolt');
const { CerberusAI } = require('@cerberus-ai/sdk');

// Initialize
const cerberus = new CerberusAI(process.env.CERBERUS_API_KEY);

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET
});

// Handle mentions
app.event('app_mention', async ({ event, say }) => {
  try {
    const response = await cerberus.chatCompletion([
      { role: 'system', content: 'You are a helpful coding assistant on Slack.' },
      { role: 'user', content: event.text }
    ], { model: 'cerberus-lite' });
    
    await say({
      text: response.choices[0].message.content,
      thread_ts: event.ts
    });
  } catch (error) {
    console.error(error);
    await say('Sorry, I encountered an error.');
  }
});

// Handle DMs
app.message(async ({ message, say }) => {
  if (message.channel_type === 'im') {
    try {
      const response = await cerberus.chatCompletion([
        { role: 'user', content: message.text }
      ]);
      
      await say(response.choices[0].message.content);
    } catch (error) {
      console.error(error);
    }
  }
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log('⚡️ Slack bot is running!');
})();
