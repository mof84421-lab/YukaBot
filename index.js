const { Client, GatewayIntentBits, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const express = require('express');

// ==========================================
// 1. ระบบ WEB SERVER สำหรับ RENDER
// ==========================================
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('🤖 บอทออนไลน์พร้อมระบบยืนยันตัวตนทำงานอยู่บน Render!');
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
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
  ]
});


// ==========================================
// 3. ระบบเมื่อบอทพร้อมทำงาน & ลงทะเบียน SLASH COMMANDS
// ==========================================
client.once('ready', async () => {
  console.log(`[Bot] ล็อกอินเข้าสู่ระบบในชื่อ: ${client.user.tag}!`);

  // เพิ่มคำสั่ง /setup-verify เพื่อสร้างปุ่มยืนยันตัวตน
  const commands = [
    { name: 'ping', description: 'เช็คความเร็วบอท' },
    { name: 'บ๊ายบาย', description: 'ให้บอทกล่าวลา' },
    { name: 'setup-verify', description: 'สร้างปุ่มกดเปิดระบบยืนยันตัวตน (สำหรับแอดมิน)' }
  ];

  try {
    await client.application.commands.set(commands);
    console.log('[Slash Commands] ลงทะเบียนคำสั่งทั้งหมดสำเร็จแล้ว!');
  } catch (error) {
    console.error('[Slash Commands] เกิดข้อผิดพลาด:', error);
  }
});


// ==========================================
// 4. ระบบคำสั่งแบบ SLASH COMMANDS & การกดปุ่ม
// ==========================================
client.on('interactionCreate', async interaction => {
  
  // ส่วนที่ 4.1: จัดการเมื่อมีคนใช้คำสั่งพิมพ์ /
  if (interaction.isChatInputCommand()) {
    const { commandName } = interaction;

    if (commandName === 'ping') {
      await interaction.reply(`🏓 พง! ความเร็วอินเทอร์เน็ตบอท: ${client.ws.ping}ms`);
    }
    
    if (commandName === 'บ๊ายบาย') {
      await interaction.reply(`บ๊ายบายจ้า คุณ ${interaction.user.username} 👋 ไว้เจอกันใหม่นะ!`);
    }

    // คำสั่งสร้างปุ่มยืนยันตัวตน (ให้พิมพ์คำสั่งนี้ในห้องที่อยากให้คนมากดยืนยันตัวตน)
    if (commandName === 'setup-verify') {
      // ตรวจสอบว่าคนใช้คำสั่งเป็นแอดมินหรือไม่ (เพื่อความปลอดภัย)
      if (!interaction.member.permissions.has('Administrator')) {
        return interaction.reply({ content: '❌ เฉพาะแอดมินเท่านั้นที่ใช้คำสั่งนี้ได้ครับ!', ephemeral: true });
      }

      // สร้างปุ่มกด
      const row = new ActionRowBuilder()
        .addComponents(
          new ButtonBuilder()
            .setCustomId('verify_button')
            .setLabel('✅ กดตรงนี้เพื่อยืนยันตัวตน')
            .setStyle(ButtonStyle.Success) // ปุ่มสีเขียว
        );

      await interaction.reply({
        content: '⚙️ **ระบบยืนยันตัวตน (Verification)**\nกรุณากดปุ่มด้านล่างเพื่อเข้าสู่เซิร์ฟเวอร์และเปิดใช้งานห้องต่าง ๆ ครับ',
        components: [row]
      });
    }
  }

  // ส่วนที่ 4.2: จัดการเมื่อมีคน "กดปุ่ม" ยืนยันตัวตน
  if (interaction.isButton()) {
    if (interaction.customId === 'verify_button') {
      
      // ⚠️ ให้เปลี่ยนชื่อยศตรงนี้ให้ตรงกับยศในดิสคอร์ดของคุณ
      const roleName = 'Member'; 
      const role = interaction.guild.roles.cache.find(r => r.name === roleName);

      if (!role) {
        return interaction.reply({ 
          content: `❌ ไม่เจอยศที่ชื่อ "${roleName}" ในเซิร์ฟเวอร์ กรุณาแจ้งแอดมินให้สร้างยศนี้ก่อนครับ`, 
          ephemeral: true 
        });
      }

      // ตรวจสอบว่าเขามียศนี้อยู่แล้วหรือยัง
      if (interaction.member.roles.cache.has(role.id)) {
        return interaction.reply({ content: '🤝 คุณเคยยืนยันตัวตนไปแล้วนะคราบบบ!', ephemeral: true });
      }

      try {
        // แจกยศให้คนที่กดปุ่ม
        await interaction.member.roles.add(role);
        // ephemeral: true หมายถึง ข้อความนี้จะเห็นแค่คนที่กดปุ่มเท่านั้น คนอื่นไม่เห็นรกแชท
        await interaction.reply({ content: '🎉 ยืนยันตัวตนสำเร็จ! ขอให้สนุกกับเซิร์ฟเวอร์เรานะครับ', ephemeral: true });
      } catch (error) {
        console.error(error);
        await interaction.reply({ content: '❌ บอทไม่สามารถให้ยศได้ เนื่องจากยศของบอทอยู่ต่ำกว่ายศนี้ในตั้งค่าเซิร์ฟเวอร์!', ephemeral: true });
      }
    }
  }
});


// ==========================================
// 5. ระบบต้อนรับสมาชิกใหม่
// ==========================================
client.on('guildMemberAdd', member => {
  const channel = member.guild.channels.cache.find(ch => ch.name === 'ต้อนรับสมาชิก' || ch.name === 'welcome') 
                  || member.guild.systemChannel;

  if (!channel) return;
  channel.send(`🎉 ยินดีต้อนรับคุณ ${member} เข้าสู่เซิร์ฟเวอร์! อย่าลืมไปกดยืนยันตัวตนด้วยนะครับ ✨`);
});


// ==========================================
// 6. ระบบตอบกลับคำอัตโนมัติ
// ==========================================
client.on('messageCreate', message => {
  if (message.author.bot) return;

  if (message.content === 'สวัสดี') {
    message.reply('สวัสดีครับผม! มีอะไรให้บอทรับใช้ไหมครับ? 🤖');
  }
});

// รันบอท
client.login(process.env.TOKEN);