const afkUsers = new Map(); // ตัวจำลองเก็บสถานะ AFK

module.exports = {
  name: 'messageCreate',
  execute(message) {
    if (message.author.bot || !message.guild) return;

    const userId = message.author.id;

    // 1. ถ้าคนส่งข้อความ "กำลังติดสถานะ AFK อยู่" -> ให้ยกเลิกสถานะทันทีเมื่อเขากลับมาพิมพ์
    if (afkUsers.has(userId)) {
      const afkData = afkUsers.get(userId);
      afkUsers.delete(userId);
      return message.reply(`👋 ยินดีต้อนรับกลับมาครับ! บอทได้ปิดสถานะ AFK ของคุณเรียบร้อยแล้ว (คุณไปทำธุระเรื่อง: *${afkData.reason}* มา)`).then(msg => {
        setTimeout(() => msg.delete().catch(e => {}), 5000); // ลบใน 5 วินาที
      });
    }

    // 2. ถ้ามีใครพิมพ์แท็กหาคนท่ีติดสถานะ AFK -> บอทจะช่วยตอบแทนให้
    if (message.mentions.users.size > 0) {
      message.mentions.users.forEach(mentionedUser => {
        if (afkUsers.has(mentionedUser.id)) {
          const afkData = afkUsers.get(mentionedUser.id);
          message.reply(`💤 ตอนนี้คุณ **${mentionedUser.username}** กำลัง AFK อยู่นะครับ\n📝 เหตุผล: *${afkData.reason}*`);
        }
      });
    }

    // 3. คำสั่งเปิดโหมด AFK: พิมพ์ "เปิดบอท afk [เหตุผล]" หรือ "!afk [เหตุผล]"
    if (message.content.startsWith('!afk ') || message.content.startsWith('ไปละนะ ')) {
      const args = message.content.split(' ');
      const reason = args.slice(1).join(' ') || 'ไปทำธุระแป๊บนึงครับ';

      afkUsers.set(userId, { reason: reason, time: Date.now() });
      return message.reply(`💤 **เข้าสู่โหมด AFK สำเร็จ!** บอทจะแจ้งเตือนคนอื่นให้ว่าคุณไม่อยู่เนื่องจาก: *${reason}*`);
    }
  },
};