const { Client, GatewayIntentBits } = require('discord.js');
const { DisTube } = require('distube');
const { YouTubePlugin } = require('@distube/youtube');
const path = require('path');
require('dotenv').config();

// สร้าง Client สำหรับเชื่อมต่อ Discord (เปิดสิทธิ์ครบถ้วน)
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

// ตั้งค่าระบบเพลง DisTube (v5)
client.distube = new DisTube(client, {
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
// 🔄 โหลดระบบ EVENTS HANDLER (เจาะจงเฉพาะไฟล์หลัก)
// ==========================================
const eventsPath = path.join(__dirname, 'events');

// 🎯 ล็อกเป้าหมายโหลดเฉพาะ 2 ไฟล์นี้เท่านั้น ไฟล์อื่นในโฟลเดอร์จะไม่ถูกดึงมารันให้ค้าง
const targetFiles = ['ready.js', 'interaction.js'];

for (const fileName of targetFiles) {
  try {
    const filePath = path.join(eventsPath, fileName);
    const event = require(filePath);
    
    if (event && event.name && typeof event.execute === 'function') {
      if (event.once) {
        client.once(event.name, (...args) => event.execute(...args, client));
      } else {
        client.on(event.name, (...args) => event.execute(...args, client));
      }
      console.log(`[System] โหลดไฟล์ Event สำเร็จ: ${fileName}`);
    }
  } catch (error) {
    console.log(`[Warning] ไม่สามารถโหลดไฟล์ ${fileName} ได้ หรือไม่มีไฟล์นี้อยู่จริง`);
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
console.log('[System] กำลังเชื่อมต่อไปยัง Discord...');
client.login(process.env.TOKEN).catch(err => {
  console.error('[Login Error] ไม่สามารถเชื่อมต่อกับ Discord ได้ ตรวจสอบ TOKEN อีกครั้ง:', err);
});