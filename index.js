const { Client, GatewayIntentBits } = require('discord.js');
const express = require('express');

// ==========================================
// 1. ระบบ WEB SERVER สำหรับ RENDER (ห้ามลบ)
// ==========================================
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('🤖 บอทของคุณกำลังออนไลน์และทำงานอยู่ 24 ชม. บน Render!');
});

app.listen(port, () => {
  console.log(`[Web Server] รันบนพอร์ต ${port} สำเร็จแล้ว`);
});


// ==========================================
// 2. ตั้งค่า DISCORD BOT CLIENT
// ==========================================
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent, // จำเป็นสำหรับระบบตอบกลับอัตโนมัติ
    GatewayIntentBits.GuildMembers     // จำเป็นสำหรับระบบต้อนรับสมาชิกใหม่
  ]
});


// ==========================================
// 3. ระบบเมื่อบอทพร้อมทำงาน & ลงทะเบียน SLASH COMMANDS
// ==========================================
client.once('ready', async () => {
  console.log(`[Bot] ล็อกอินเข้าสู่ระบบในชื่อ: ${client.user.tag}!`);

  // รายการ Slash Commands ที่ต้องการสร้าง
  const commands = [
    { name: 'ping', description: 'เช็คความเร็วบอท' },
    { name: 'บ๊ายบาย', description: 'ให้บอทกล่าวลา' }
  ];

  try {
    // ลงทะเบียนคำสั่งไปที่ Discord
    await client.application.commands.set(commands);
    console.log('[Slash Commands] ลงทะเบียนคำสั่ง / ทั้งหมดสำเร็จแล้ว!');
  } catch (error) {
    console.error('[Slash Commands] เกิดข้อผิดพลาด:', error);
  }
});


// ==========================================
// 4. ระบบคำสั่งแบบ SLASH COMMANDS (พิมพ์ /)
// ==========================================
client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;

  const { commandName } = interaction;

  if (commandName === 'ping') {
    await interaction.reply(`🏓 พง! ความเร็วอินเทอร์เน็ตบอท: ${client.ws.ping}ms`);
  }
  
  if (commandName === 'บ๊ายบาย') {
    await interaction.reply(`บ๊ายบายจ้า คุณ ${interaction.user.username} 👋 ไว้เจอกันใหม่นะ!`);
  }
});


// ==========================================
// 5. ระบบต้อนรับสมาชิกใหม่ (WELCOME MESSAGE)
// ==========================================
client.on('guildMemberAdd', member => {
  // พยายามหาห้องที่ชื่อว่า 'ต้อนรับสมาชิก' หรือ 'welcome' 
  const channel = member.guild.channels.cache.find(ch => ch.name === 'ต้อนรับสมาชิก' || ch.name === 'welcome') 
                  || member.guild.systemChannel; // ถ้าหาไม่เจอ ให้ส่งเข้าห้องระบบเริ่มต้นของดิสคอร์ดแทน

  if (!channel) return;

  channel.send(`🎉 ยินดีต้อนรับคุณ ${member} เข้าสู่เซิร์ฟเวอร์ **${member.guild.name}** อย่างเป็นทางการครับ! ขอให้สนุกนะ! ✨`);
});


// ==========================================
// 6. ระบบตอบกลับคำอัตโนมัติ (AUTO RESPONSE)
// ==========================================
client.on('messageCreate', message => {
  // ถ้าเป็นข้อความจากบอทด้วยกันเอง ไม่ต้องตอบกลับ
  if (message.author.bot) return;

  // ตรวจจับคำแบบตรงตัว
  if (message.content === 'สวัสดี') {
    message.reply('สวัสดีครับผม! มีอะไรให้บอทรับใช้ไหมครับ? 🤖');
  }

  // ตรวจจับคำที่มีอยู่ในประโยค (ไม่จำเป็นต้องพิมพ์ตรงเป๊ะ)
  if (message.content.includes('ขอเลขบัญชี') || message.content.includes('โดเนท')) {
    message.reply('💰 สามารถสนับสนุนเซิร์ฟเวอร์เราได้ที่บัญชี 000-0-00000-0 นะครับ ขอบคุณมากๆ ครับ! 🙏');
  }
});


// ==========================================
// 7. รันบอทด้วย TOKEN จาก ENVIRONMENT VARIABLE
// ==========================================
client.login(process.env.TOKEN);