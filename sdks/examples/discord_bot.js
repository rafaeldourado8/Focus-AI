/**
 * Discord Bot for Cerberus AI
 * 
 * Basic example - Full implementation in future phase
 * Requires: discord.js, @cerberus-ai/sdk
 */

const { Client, GatewayIntentBits } = require('discord.js');
const { CerberusAI } = require('@cerberus-ai/sdk');

// Initialize
const cerberus = new CerberusAI(process.env.CERBERUS_API_KEY);

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

// Ready event
client.once('ready', () => {
  console.log(`✓ Logged in as ${client.user.tag}`);
});

// Message handler
client.on('messageCreate', async (message) => {
  // Ignore bots
  if (message.author.bot) return;

  // Only respond to mentions or DMs
  const isMentioned = message.mentions.has(client.user);
  const isDM = message.channel.type === 'DM';

  if (!isMentioned && !isDM) return;

  try {
    // Show typing indicator
    await message.channel.sendTyping();

    // Get response from Cerberus AI
    const response = await cerberus.chatCompletion([
      { role: 'system', content: 'You are a helpful coding assistant on Discord.' },
      { role: 'user', content: message.content.replace(`<@${client.user.id}>`, '').trim() }
    ], { model: 'cerberus-lite' });

    const reply = response.choices[0].message.content;

    // Split long messages (Discord limit: 2000 chars)
    if (reply.length > 2000) {
      const chunks = reply.match(/.{1,2000}/g);
      for (const chunk of chunks) {
        await message.reply(chunk);
      }
    } else {
      await message.reply(reply);
    }

  } catch (error) {
    console.error('Error:', error);
    await message.reply('Sorry, I encountered an error. Please try again.');
  }
});

// Slash command: /debug
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'debug') {
    const code = interaction.options.getString('code');
    const error = interaction.options.getString('error');
    const language = interaction.options.getString('language') || 'javascript';

    await interaction.deferReply();

    try {
      const response = await cerberus.debugCode(error, code, language);
      await interaction.editReply(response.debug_info.substring(0, 2000));
    } catch (err) {
      await interaction.editReply('Error processing debug request.');
    }
  }
});

// Login
client.login(process.env.DISCORD_BOT_TOKEN);
