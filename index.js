const { Client, GatewayIntentBits } = require('discord.js');
const express = require('express');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('บอทมือถือออนไลน์แล้ว!');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.on('messageCreate', (message) => {
  if (message.author.bot) return;
  if (message.content === 'สวัสดี') {
    message.reply('สวัสดีครับ! ยินดีที่ได้คุยกันผ่านมือถือ');
  }
});

client.login(process.env.DISCORD_TOKEN);