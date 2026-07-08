module.exports = {
  name: 'ready',
  once: true,
  async execute(client) {
    console.log(`[Bot] ออนไลน์แล้วในชื่อ: ${client.user.tag}`);
    
    // ลงทะเบียนคำสั่ง Slash Command ทั้งหมดที่นี่
    const commands = [
      { name: 'ping', description: 'เช็คความเร็วบอท' },
      { name: 'setup-verify', description: 'สร้างปุ่มกดระบบยืนยันตัวตน' }
    ];

    try {
      await client.application.commands.set(commands);
      console.log('[Slash Commands] อัปเดตคำสั่งสำเร็จ!');
    } catch (error) {
      console.error(error);
    }
  },
};