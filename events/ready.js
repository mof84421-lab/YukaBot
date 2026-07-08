const { REST, Routes } = require('discord.js');

module.exports = {
  name: 'ready',
  once: true,
  async execute(client) {
    console.log(`[Bot] ออนไลน์แล้วในชื่อ: ${client.user.tag}`);

    // กำหนดค่าสเตตัสเท่ ๆ ให้ YukaBot
    client.user.setActivity('🎶 พิมพ์ / เพื่อดูคำสั่งทั้งหมด', { type: 3 }); // Type 3 = Watching

    // รายชื่อคำสั่ง Slash Commands ทั้งหมดของเซิร์ฟเวอร์
    const commands = [
      { name: 'ping', description: 'เช็คความเร็วการตอบกลับของบอท' },
      { name: 'setup-verify', description: 'สร้างปุ่มกดระบบยืนยันตัวตน' },
      { name: 'setup-ticket', description: 'สร้างปุ่มเปิดตั๋วแจ้งปัญหาติดต่อแอดมิน' },
      
      // 🎵 เพิ่มคำสั่งระบบเพลงแบบ Slash Command
      { 
        name: 'play', 
        description: 'เปิดเพลงจากชื่อหรือลิงก์ YouTube/SoundCloud',
        options: [
          {
            name: 'song',
            type: 3, // 3 คือประเภท String (ข้อความ)
            description: 'พิมพ์ชื่อเพลง หรือ วางลิงก์เพลงที่ต้องการเปิด',
            required: true
          }
        ]
      },
      { name: 'skip', description: 'ข้ามเพลงปัจจุบันที่กำลังเล่นอยู่' },
      { name: 'stop', description: 'หยุดเล่นเพลงทั้งหมด ล้างคิว และให้บอทออกจากห้องเสียง' }
    ];

    const rest = new REST({ version: '10' }).setToken(process.env.TOKEN);

    try {
      console.log('[Deploy] กำลังอัปเดตคำสั่ง (Slash Commands) ทั้งหมดไปยัง Discord...');
      
      // อัปเดตคำสั่งแบบ Global (ใช้ได้ทุกเซิร์ฟเวอร์ที่บอทอยู่)
      await rest.put(
        Routes.applicationCommands(client.user.id),
        { body: commands }
      );

      console.log('[Deploy] อัปเดตคำสั่งทั้งหมดเสร็จสิ้น! พร้อมใช้งานแล้ว 🎉');
    } catch (error) {
      console.error('[Deploy Error] เกิดข้อผิดพลาดในการลงทะเบียนคำสั่ง:', error);
    }
  },
};