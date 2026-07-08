// ตัวเก็บข้อมูลเลเวลชั่วคราว (ถ้าบอทรีสตาร์ทบน Render ค่าจะรีเซ็ต แต่เหมาะสำหรับการเริ่มต้นครับ)
const userXP = new Map();

module.exports = {
  name: 'messageCreate',
  execute(message) {
    // ไม่นับข้อความจากบอท หรือข้อความใน DM
    if (message.author.bot || !message.guild) return;

    const userId = message.author.id;
    let userData = userXP.get(userId) || { xp: 0, level: 1 };

    // สุ่มแจก XP 15 ถึง 25 ต่อหนึ่งข้อความ
    const xpGained = Math.floor(Math.random() * 11) + 15;
    userData.xp += xpGained;

    // คำนวณ XP ที่ใช้ในการอัปเลเวล (สูตร: เลเวลปัจจุบัน * 100)
    const xpNeeded = userData.level * 100;

    if (userData.xp >= xpNeeded) {
      userData.xp -= xpNeeded;
      userData.level += 1;
      
      // ส่งข้อความแสดงความยินดี (แท็กคนพิมพ์)
      message.channel.send(`🆙 **GG!** คุณ ${message.author} เลเวลอัปเป็น **Level ${userData.level}** แล้วจ้า! 🎉`);
    }

    // บันทึกค่ากลับลงระบบ
    userXP.set(userId, userData);

    // ระบบแถม: พิมพ์ "เช็คเวล" เพื่อดูเลเวลตัวเอง
    if (message.content === '!profile' || message.content === 'เช็คเวล') {
      message.reply(`📊 **โปรไฟล์ของคุณ ${message.author.username}**\n⭐ เลเวล: ${userData.level}\n✨ XP ปัจจุบัน: ${userData.xp}/${userData.level * 100}`);
    }
  },
};