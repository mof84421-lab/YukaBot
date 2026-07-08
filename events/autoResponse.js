module.exports = {
  name: 'messageCreate',
  execute(message) {
    if (message.author.bot) return;

    if (message.content === 'สวัสดี') {
      message.reply('สวัสดีครับผม! มีอะไรให้บอทรับใช้ไหมครับ? 🤖');
    }
  },
};