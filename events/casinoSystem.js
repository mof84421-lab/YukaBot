const wallet = new Map(); // ตัวเก็บกระเป๋าตังค์จำลอง
const cooldowns = new Map(); // ตัวกันปั๊มเงินรายวัน

module.exports = {
  name: 'messageCreate',
  execute(message) {
    if (message.author.bot) return;

    const userId = message.author.id;
    let balance = wallet.get(userId) || 0;

    // 1. คำสั่งรับเงินรายวัน (!daily)
    if (message.content === '!daily' || message.content === 'รับเงิน') {
      const lastDaily = cooldowns.get(userId);
      const now = Date.now();
      
      // คูลดาวน์ 24 ชั่วโมง (86400000 มิลลิวินาที)
      if (lastDaily && now - lastDaily < 86400000) {
        const remaining = 86400000 - (now - lastDaily);
        const hours = Math.floor(remaining / 3600000);
        return message.reply(`⏰ คุณรับเงินไปแล้ว! มารับใหม่ในอีก ${hours} ชั่วโมงข้างหน้านะครับ`);
      }

      const reward = 500; // แจกวันละ 500
      wallet.set(userId, balance + reward);
      cooldowns.set(userId, now);
      return message.reply(`💰 ยินดีด้วย! คุณได้รับเงินรายวันจำนวน **$${reward}** เรียบร้อยแล้ว (เงินทั้งหมด: $${balance + reward})`);
    }

    // 2. คำสั่งเช็คเงิน (!wallet)
    if (message.content === '!wallet' || message.content === 'กระเป๋าตังค์') {
      return message.reply(`💳 ในกระเป๋าของคุณ ${message.author.username} มีเงินอยู่ **$${balance}**`);
    }

    // 3. คำสั่งเล่นพนันเสี่ยงดวง (!gamble [จำนวนเงิน])
    if (message.content.startsWith('!gamble ') || message.content.startsWith('แทง ')) {
      const args = message.content.split(' ');
      const bet = parseInt(args[1]);

      if (isNaN(bet) || bet <= 0) {
        return message.reply('❌ กรุณาใส่จำนวนเงินที่ต้องการเดิมพันให้ถูกต้อง เช่น `!gamble 100` หรือ `แทง 100`');
      }

      if (balance < bet) {
        return message.reply('❌ เงินในกระเป๋าไม่พอที่จะเดิมพันครับ ไปพิมพ์ `!daily` เพื่อรับเงินฟรีก่อนนะ!');
      }

      // สุ่มโอกาสชนะ 50/50
      const win = Math.random() > 0.5;

      if (win) {
        wallet.set(userId, balance + bet);
        message.reply(`🎰 **WIN!!** ดวงดีสุดๆ! คุณชนะการเดิมพัน ได้รับเงินมาเพิ่มอีก **$${bet}** (เงินทั้งหมด: $${balance + bet}) 🤑`);
      } else {
        wallet.set(userId, balance - bet);
        message.reply(`📉 **LOSE...** บอทกินเรียบ! คุณเสียเงินไป **$${bet}** รอบหน้าเอาใหม่นะ (เงินทั้งหมดเหลือ: $${balance - bet}) 🥲`);
      }
    }
  },
};