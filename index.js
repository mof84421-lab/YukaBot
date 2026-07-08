const { Client, GatewayIntentBits } = require('discord.js');
const { DisTube } = require('distube');
const { YouTubePlugin } = require('@distube/youtube');
const fs = require('fs');
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
// 🔄 โหลดระบบ EVENTS HANDLER (ระบบกรองเซฟตี้ขั้นสุด)
// ==========================================
const eventsPath = path.join(__dirname, 'events');

if (fs.existsSync(eventsPath)) {
  const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.js'));

  for (const file of eventFiles) {
    try {
      const filePath = path.join(eventsPath, file);
      const event = require(filePath);
      
      // 🔥 ตรวจสอบโครงสร้าง: ต้องมี name และเป็น Event จริง ๆ ถึงจะโหลด เพื่อไม่ให้บอทค้างหรือออฟไลน์
      if (event && event.name && typeof event.execute === 'function') {
        if (event.once) {
          client.once(event.name, (...args) => event.execute(...args, client));
        } else {
          client.on(event.name, (...args) => event.execute(...args, client));
        }
        console.log(`[System] โหลดไฟล์ Event สำเร็จ: ${file}`);
      } else {
        console.log(`[System Info] ข้ามการโหลดไฟล์ (ไม่ใช่ Event หลัก): ${file}`);
      }
    } catch (fileErr) {
      console.log(`[Warning] ไม่สามารถอ่านไฟล์ ${file} ได้เนื่องจากโครงสร้างภายในขัดแย้ง`);
    }
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