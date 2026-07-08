const { Client, GatewayIntentBits, Collection } = require('discord.js');
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
// 🔄 ระบบโหลดอัจฉริยะ: รันทุกระบบพร้อมกันโดยไม่ให้บอทแครช
// ==========================================
const eventsPath = path.join(__dirname, 'events');

if (fs.existsSync(eventsPath)) {
  const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.js'));

  for (const file of eventFiles) {
    try {
      const filePath = path.join(eventsPath, file);
      const moduleData = require(filePath);
      
      // 🎯 ถ้าไฟล์ไหนมีโครงสร้างเป็น Event หลัก (ready, interactionCreate) ให้ผูกระบบเข้า Discord
      if (moduleData && moduleData.name && typeof moduleData.execute === 'function') {
        if (moduleData.once) {
          client.once(moduleData.name, (...args) => moduleData.execute(...args, client));
        } else {
          client.on(moduleData.name, (...args) => moduleData.execute(...args, client));
        }
        console.log(`[Event Loaded] เชื่อมต่อระบบ Event สำเร็จ: ${file}`);
      } 
      // ⚙️ ถ้าเป็นไฟล์ระบบคำสั่งอื่น ๆ (Casino, Level, AFK) ให้สั่งรันทำงานเบื้องหลังไปเลย ไม่ต้องข้าม
      else if (typeof moduleData === 'function') {
        moduleData(client);
        console.log(`[System Loaded] เปิดใช้งานระบบเสริมสำเร็จ: ${file}`);
      } else {
        console.log(`[System Info] ไฟล์ระบบแบบดึงข้อมูลทั่วไปพร้อมใช้งาน: ${file}`);
      }
    } catch (fileErr) {
      // ป้องกันกรณีไฟล์บางตัวมีบั๊ก ให้ข้ามไปรันไฟล์อื่นต่อทันที บอทจะได้ไม่ออฟไลน์
      console.log(`[Safe Guard] ข้ามข้อผิดพลาดในไฟล์ ${file} เพื่อป้องกันบอทล่ม: ${fileErr.message}`);
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