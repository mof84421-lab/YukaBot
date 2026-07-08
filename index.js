const { Client, GatewayIntentBits, Collection } = require('discord.js');
const { DisTube } = require('distube');
const { YouTubePlugin } = require('@distube/youtube');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// สร้าง Client สำหรับเชื่อมต่อ Discord
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildPresences
  ]
});

// ตั้งค่าระบบเพลง DisTube
client.distube = new DisTube(client, {
  leaveOnStop: true,
  emitNewSongOnly: true,
  emitAddSongWhenCreatingQueue: false,
  emitAddListWhenCreatingQueue: false,
  plugins: [new YouTubePlugin()]
});

// เปิด Server ขนานสำหรับรันบน Render (Port 10000)
const http = require('http');
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('YukaBot ออนไลน์อยู่บน Render เรียบร้อยแล้วครับ! 🤖');
});

const PORT = process.env.PORT || 10000;
server.listen(PORT, () => {
  console.log(`[Server] YukaBot Port: ${PORT}`);
});

// ==========================================
// 🔄 โหลดยก EVENTS HANDLER (แก้ไขระบบคัดกรอง)
// ==========================================
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.js'));

for (const file of eventFiles) {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  
  // 🔥 ระบบตัวกรองป้องกันบอทค้าง: 
  // ถ้าไฟล์ไหนไม่มีรูปแบบโครงสร้าง Event ที่ถูกต้อง (เช่น ไม่มี name หรือไม่มี execute) ให้ข้ามทันที
  if (!event || !event.name || typeof event.execute !== 'function') {
    console.log(`[System Info] ข้ามการโหลดไฟล์เนื่องจากไม่ใช่โครงสร้าง Event: ${file}`);
    continue; 
  }

  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args, client));
  } else {
    client.on(event.name, (...args) => event.execute(...args, client));
  }
}

// ==========================================
// 🎵 โหลดระบบแจ้งเตือนเพลง DisTube
// ==========================================
client.distube
  .on('playSong', (queue, song) => {
    queue.textChannel.send(`🎶 กำลังเล่นเพลง: **${song.name}** - \`${song.formattedDuration}\`\nขอโดย: ${song.user}`);
  })
  .on('addSong', (queue, song) => {
    queue.textChannel.send(`✅ เพิ่มเพลง **${song.name}** เข้าในคิวแล้วครับ!`);
  })
  .on('error', (channel, e) => {
    console.error(e);
    if (channel) channel.send(`❌ เกิดข้อผิดพลาดในระบบเพลง: ${e.message.slice(0, 100)}`);
  });

// เข้าสู่ระบบด้วย Token
client.login(process.env.TOKEN).catch(err => {
  console.error('[Login Error] ไม่สามารถเชื่อมต่อกับ Discord ได้ ตรวจสอบ TOKEN อีกครั้ง:', err);
});