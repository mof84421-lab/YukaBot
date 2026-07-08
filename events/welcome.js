module.exports = {
  name: 'guildMemberAdd',
  execute(member) {
    const channel = member.guild.channels.cache.find(ch => ch.name === 'ต้อนรับสมาชิก') 
                    || member.guild.systemChannel;

    if (!channel) return;
    channel.send(`🎉 ยินดีต้อนรับคุณ ${member} เข้าสู่เซิร์ฟเวอร์ครับ! อย่าลืมไปกดยืนยันตัวตนนะ ✨`);
  },
};