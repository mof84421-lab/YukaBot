const { REST, Routes, SlashCommandBuilder } = require('discord.js');

module.exports = {
  name: 'ready',
  once: true,
  async execute(client) {
    console.log(`[Online] ${client.user.tag} พร้อมใช้งานแล้วครับ! 🤖✨`);

    // ==========================================
    // 📋 รวมชุดคำสั่ง (Slash Commands) ของทุกระบบ
    // ==========================================
    const commands = [
      // 🎵 1. ระบบเพลง (Music System)
      new SlashCommandBuilder()
        .setName('play')
        .setDescription('เปิดเพลงจาก YouTube / SoundCloud')
        .addStringOption(option => 
          option.setName('song')
            .setDescription('ชื่อเพลง หรือ ลิงก์เพลง')
            .setRequired(true)),
      new SlashCommandBuilder().setName('skip').setDescription('ข้ามเพลงปัจจุบัน'),
      new SlashCommandBuilder().setName('stop').setDescription('หยุดเล่นเพลงและออกจากห้องเสียง'),

      // 🎰 2. ระบบคาสิโน (Casino System)
      new SlashCommandBuilder().setName('money').setDescription('เช็คจำนวนเงินของคุณ'),
      new SlashCommandBuilder().setName('work').setDescription('ทำงานหาเงินประจำวัน'),
      new SlashCommandBuilder()
        .setName('slots')
        .setDescription('เล่นสล็อตแมชชีนเสี่ยงโชค')
        .addIntegerOption(option => 
          option.setName('bet')
            .setDescription('จำนวนเงินที่ต้องการเดิมพัน')
            .setRequired(true)),

      // 📊 3. ระบบเลเวล (Level System)
      new SlashCommandBuilder().setName('rank').setDescription('ดูการ์ดเลเวลและอันดับของคุณ'),
      new SlashCommandBuilder().setName('leaderboard').setDescription('ดูอันดับผู้เล่นที่เลเวลสูงที่สุดในเซิร์ฟเวอร์'),

      // 💤 4. ระบบ AFK (AFK System)
      new SlashCommandBuilder()
        .setName('afk')
        .setDescription('ตั้งสถานะไม่อยู่หน้าจอ (AFK)')
        .addStringOption(option => 
          option.setName('reason')
            .setDescription('เหตุผลที่ไม่อยู่')
            .setRequired(false)),

      // 🎫 5. ระบบตั๋วช่วยเหลือ (Ticket System)
      new SlashCommandBuilder().setName('setup-ticket').setDescription('ตั้งค่าปุ่มกดสร้างตั๋วติดต่อทีมงาน (สำหรับผู้ดูแล)'),

      // 🎉 6. ระบบแจกของ (Giveaway System)
      new SlashCommandBuilder().setName('giveaway').setDescription('เริ่มกิจกรรมสุ่มแจกรางวัลในเซิร์ฟเวอร์')
    ].map(command => command.toJSON());

    // ==========================================
    // 🚀 ยิงข้อมูลคำสั่งทั้งหมดขึ้นระบบ Discord หลังบ้าน
    // ==========================================
    const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

    try {
      console.log('[System] กำลังลงทะเบียนคำสั่งสแลชทั้งหมด...');

      // ส่งคำสั่งแบบ Global (ใช้งานได้ทุกเซิร์ฟเวอร์ที่บอทอยู่)
      await rest.put(
        Routes.applicationCommands(client.user.id),
        { body: commands }
      );

      console.log('[System] ลงทะเบียนคำสั่งสแลชสำเร็จและพร้อมใช้งานครบทุกระบบแล้ว! 🎉');
    } catch (error) {
      console.error('[Error] เกิดข้อผิดพลาดในการลงทะเบียนคำสั่ง:', error);
    }
  }
};