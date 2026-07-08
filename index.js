const { Client, GatewayIntentBits, Collection } = require('discord.js');
const express = require('express');
const fs = require('fs');
const path = require('path');
const { DisTube } = require('distube');
const { YouTubePlugin } = require('@distube/youtube'); // 👈 เพิ่มปลั๊กอินสำหรับดึงสตรีมเพลง
const { SoundCloudPlugin } = require('@distube/soundcloud');

// ==========================================
// RENDER WEB SERVER
// ==========================================
const app = express();
const port = process.env.PORT || 3000;
app.get('/', (req, res) => res.send('🤖 YukaBot ออนไลน์พร้อมระบบเพลงและมัลติฟังก์ชันบน Render แล้ว!'));
app.listen(port, () => console.log(`[Server] YukaBot Port: ${port}`));

// ==========================================
// DISCORD CLIENT SETUP
// ==========================================
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildVoiceStates
  ]
});

client.commands = new Collection();

// ==========================================
// ตั้งค่าระบบเพลง DISTUBE (อัปเดตเวอร์ชันใหม่)
// ==========================================
client.distube = new DisTube(client, {
  emitNewSongOnly: true,
  nsfw: false,
  plugins: [new YouTubePlugin(), new SoundCloudPlugin()] // 👈 ใส่ปลั๊กอินเพื่อให้เปิดเพลงไม่ติดขัด
});

client.distube.on('playSong', (queue, song) => {
  queue.textChannel.send(`🎶 **YukaBot กำลังเล่น:** **${song.name}** - \`${song.formattedDuration}\`\n👤 ขอโดย: ${song.user}`);
});

client.distube.on('addSong', (queue, song) => {
  queue.textChannel.send(`✅ เพิ่มเข้าคิว YukaBot แล้ว: **${song.name}** โดยคุณ ${song.user}`);
});

// ==========================================
// โหลด EVENTS HANDLER
// ==========================================
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

client.login(process.env.TOKEN);