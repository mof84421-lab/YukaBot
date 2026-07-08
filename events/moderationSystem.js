// รายการคำหยาบหรือคำที่ไม่ต้องการให้พิมพ์ (สามารถมาเพิ่ม-ลดตรงนี้ได้เลย)
const bannedWords = ['ค_ย', 'ควย', 'เย็ด', 'เหี้ย', 'สัส', 'มึง', 'กู']; 

module.exports = {
  name: 'messageCreate',
  async execute(message) {
    if (message.author.bot || !message.guild) return;

    // ตรวจสอบว่าข้อความมีคำหยาบอยู่ไหม
    const hasBannedWord = bannedWords.some(word => message.content.toLowerCase().includes(word));

    if (hasBannedWord) {
      try {
        // ลบข้อความที่หยาบคายทิ้งทันที
        await message.delete();
        
        // ส่งข้อความเตือน และให้มันลบตัวเองใน 5 วินาทีเพื่อไม่ให้รกช่องแชท
        const warning = await message.channel.send(`⚠️ คุณ ${message.author} กรุณาสุภาพด้วยครับ! ห้ามพิมพ์คำหยาบคายในเซิร์ฟเวอร์นี้นะครับ 🤫`);
        setTimeout(() => warning.delete().catch(err => console.log('ลบข้อความเตือนไม่ทัน')), 5000);
        
      } catch (error) {
        console.error('ไม่สามารถลบข้อความได้ (บอทอาจจะไม่มีสิทธิ์ Manage Messages):', error);
      }
    }
  },
};