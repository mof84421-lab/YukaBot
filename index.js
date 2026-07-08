const { Client, GatewayIntentBits, Collection } = require('discord.js');
const express = require('express');
const fs = require('fs');
const path = require('path');

// ==========================================
// RENDER WEB SERVER
// ==========================================
const app = express();
const port = process.env.PORT || 3000;
app.get('/', (req, res) => res.send('🤖 บอท Multi-System ออนไลน์บน Render แล้ว!'));
app.listen(port, () => console.log(`[Server] Port: ${port}`));

// ==========================================
// DISCORD CLIENT SETUP
// ==========================================
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
  ]
});

client.commands = new Collection();

// โหลดไฟล์กิจกรรมทั้งหมด (Events Handler)
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.js'));

for (const file of eventFiles) {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args, client));
  } else {
    client.on(event.name, (...args) => event.execute(...args, client));
  }
}

// รันบอท
client.login(process.env.TOKEN);