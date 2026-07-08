const { Client, GatewayIntentBits } = require('discord.js');
const { DisTube } = require('distube');
const { YouTubePlugin } = require('@distube/youtube');
const path = require('path');
require('dotenv').config();

// สร้าง Client สำหรับเชื่อมต่อ Discord (เปิดสิทธิ์แบบเซฟตี้)
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
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
// 🔄 โหดยกเลิกการพึ่งพาไฟล์อื่นชั่วคราว (เซฟตี้ 100%)
// ==========================================
const eventsPath = path.join(__dirname, 'events');

// โหลดเฉพาะตัวแอปพลิเคชันหลัก 2 ตัวนี้พอ ไฟล์อื่นจะถูกละทิ้งเพื่อไม่ให้บอทแครชออฟไลน์
const safeFiles = ['ready.js', 'interaction.js'];

for (const file of safeFiles) {
  try {
    const filePath = path.join(eventsPath, file);
    const event = require(filePath);
    if (event && event.name && typeof event.execute === 'function') {
      if (event.once) {
        client.once(event.name, (...args) => event.execute(...args, client));
      } else {
        client.on(event.name, (...args) => event.execute(...args, client));
      }
      console.log(`[Safe Load] โหลดไฟล์สำเร็จ: ${file}`);
    }
  } catch (err) {
    console.log(`[Safe Warning] ข้ามการโหลดไฟล์เนื่องจากไม่มีอยู่จริงหรือเขียนผิดโครงสร้าง: ${file}`);
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

// 🚀 คำสั่งล็อกอินเข้าสู่ระบบตรง ๆ ไม่สนใจบั๊กไฟล์อื่น
console.log('[System] กำลังยิง Token ล็อกอินเข้าสู่ Discord...');
client.login(process.env.TOKEN).catch(err => {
  console.error('[Login Error] โทเคนผิดพลาดหรือไม่สามารถเข้าสู่ระบบได้:', err);
});