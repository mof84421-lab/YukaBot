module.exports = {
  name: 'messageCreate',
  async execute(message, client) {
    if (message.author.bot || !message.guild) return;

    // 1. คำสั่งเล่นเพลง: พิมพ์ "เปิด [ชื่อเพลง/ลิงก์]" หรือ "!play [ชื่อเพลง/ลิงก์]"
    if (message.content.startsWith('!play ') || message.content.startsWith('เปิด ')) {
      const args = message.content.split(' ');
      const musicQuery = args.slice(1).join(' ');

      if (!musicQuery) return message.reply('❌ กรุณาใส่ชื่อเพลงหรือลิงก์ด้วยครับ เช่น `เปิด เพลงคู่ชีวิต`');

      // ตรวจสอบว่าคนพิมพ์อยู่ในห้องแอร์/ห้องเสียง ไหม
      const voiceChannel = message.member.voice.channel;
      if (!voiceChannel) return message.reply('❌ คุณต้องเข้าห้องเสียง (Voice Channel) ก่อนสั่งเปิดเพลงครับ!');

      try {
        message.reply(`🔍 กำลังค้นหาและดึงเพลง: **${musicQuery}**...`);
        
        // สั่งให้ DisTube เล่นเพลงในห้องเสียงนั้น
        await client.distube.play(voiceChannel, musicQuery, {
          textChannel: message.channel,
          member: message.member,
          message: message
        });
      } catch (error) {
        console.error(error);
        message.channel.send('❌ เกิดข้อผิดพลาดในการเล่นเพลงนี้ (อาจเป็นเพราะลิขสิทธิ์หรือลิงก์ไม่ถูกต้อง)');
      }
    }

    // 2. คำสั่งข้ามเพลง: พิมพ์ "ข้าม" หรือ "!skip"
    if (message.content === '!skip' || message.content === 'ข้าม') {
      const queue = client.distube.getQueue(message.guild.id);
      if (!queue) return message.reply('❌ ตอนนี้ไม่มีเพลงที่กำลังเล่นอยู่ครับ');

      try {
        await client.distube.skip(message.guild.id);
        message.reply('⏭️ ข้ามเพลงให้เรียบร้อยแล้วครับ!');
      } catch (error) {
        // ถ้าไม่มีเพลงถัดไปในคิวแล้ว มันจะเตือน ให้เราสั่งหยุดแทน
        await client.distube.stop(message.guild.id);
        message.reply('⏹️ ไม่มีเพลงถัดไปในคิวแล้ว บอทหยุดเล่นเพลงครับ');
      }
    }

    // 3. คำสั่งหยุดเพลง/ปิดบอทเพลง: พิมพ์ "หยุด" หรือ "!stop"
    if (message.content === '!stop' || message.content === 'หยุด' || message.content === 'ออกไป') {
      const queue = client.distube.getQueue(message.guild.id);
      if (!queue) return message.reply('❌ ตอนนี้ไม่มีเพลงที่กำลังเล่นอยู่ครับ');

      await client.distube.stop(message.guild.id);
      message.reply('⏹️ หยุดเล่นเพลงและเคลียร์คิวทั้งหมดเรียบร้อยครับ!');
    }

    // 4. คำสั่งดูคิวเพลงทั้งหมด: พิมพ์ "คิว" หรือ "!queue"
    if (message.content === '!queue' || message.content === 'คิว') {
      const queue = client.distube.getQueue(message.guild.id);
      if (!queue) return message.reply('❌ ตอนนี้ไม่มีคิวเพลงครับ');

      const q = queue.songs
        .map((song, i) => `${i === 0 ? '▶️ ตอนนี้กำลังเล่น:' : `${i}.`} ${song.name} - \`${song.formattedDuration}\``)
        .slice(0, 10) // แสดงแค่ 10 เพลงแรกป้องกันข้อความยาวเกินไป
        .join('\n');

      message.reply(`📋 **รายการคิวเพลงในเซิร์ฟเวอร์:**\n${q}\n\n*มีเพลงทั้งหมดในคิว ${queue.songs.length} เพลง*`);
    }
  },
};