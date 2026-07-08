module.exports = {
  name: 'messageCreate',
  async execute(message) {
    if (message.author.bot) return;

    // คำสั่ง: !giveaway [เวลาเป็นวินาที] [ชื่อรางวัล]
    // ตัวอย่าง: !giveaway 60 เครดิตฟรี 500 บาท
    if (message.content.startsWith('!giveaway ')) {
      if (!message.member.permissions.has('Administrator')) return message.reply('❌ สิทธิ์ไม่พอครับ');

      const args = message.content.slice(10).split(' ');
      const duration = parseInt(args[0]); // ดึงเวลาตัวแรกมาแปลงเป็นตัวเลข (วินาที)
      const prize = args.slice(1).join(' '); // ข้อความที่เหลือทั้งหมดคือชื่อของรางวัล

      if (isNaN(duration) || !prize) {
        return message.reply('❌ รูปแบบคำสั่งไม่ถูกต้อง! กรุณาพิมพ์: `!giveaway [เวลาเป็นวินาที] [ชื่อรางวัล]`\n💡 ตัวอย่าง: `!giveaway 30 ไอดีเกมฟรี`');
      }

      const giveawayMessage = await message.channel.send(`🎉 **กิจกรรมสุ่มแจกของรางวัลมาแล้วจ้า!** 🎉\n\n🎁 ของรางวัล: **${prize}**\n⏳ เวลาเข้าร่วม: **${duration} วินาที**\n👉 **กดรีแอคชั่น 🎉 ด้านล่างเพื่อเข้าร่วมสุ่มเลย!!**`);
      
      // ให้บอทใส่รีแอคชั่นเริ่มต้นไว้ให้คนมากดตาม
      await giveawayMessage.react('🎉');

      // รอนับถอยหลังตามเวลาที่กำหนด
      setTimeout(async () => {
        // ดึงข้อมูลข้อความนั้นใหม่อีกครั้งเพื่ออัปเดตรีแอคชั่นล่าสุด
        const targetMessage = await message.channel.messages.fetch(giveawayMessage.id);
        const reaction = targetMessage.reactions.cache.get('🎉');
        
        if (!reaction) return message.channel.send('❌ เกิดข้อผิดพลาด ไม่มีใครกดรีแอคชั่นเลย');

        // ดึงรายชื่อคนกดทั้งหมด (และตัดตัวบอทออก)
        const users = await reaction.users.fetch();
        const list = users.filter(user => !user.bot).map(user => user);

        if (list.length === 0) {
          return message.channel.send(`😭 กิจกรรม **${prize}** สิ้นสุดแล้ว แต่ไม่มีใครเข้ามาร่วมสนุกเลยน้าาา`);
        }

        // สุ่มหาผู้โชคดี 1 คน
        const winner = list[Math.floor(Math.random() * list.length)];

        message.channel.send(`🎊 **ยินดีด้วยยยยย!** คุณ ${winner} เป็นผู้โชคดีได้รับรางวัล: **${prize}** ไปครอง!! 🏆✨`);
      }, duration * 1000);
    }
  },
};