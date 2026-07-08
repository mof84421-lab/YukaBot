const { InteractionType } = require('discord.js');

module.exports = {
  name: 'interactionCreate',
  once: false,
  async execute(interaction, client) {
    // ตรวจสอบว่าเป็นคำสั่งสแลช (Slash Command) หรือไม่
    if (!interaction.isChatInputCommand()) return;

    const { commandName } = interaction;

    // ==========================================
    // 🎵 คำสั่ง /play (เปิดเพลง)
    // ==========================================
    if (commandName === 'play') {
      const voiceChannel = interaction.member.voice.channel;
      if (!voiceChannel) {
        return interaction.reply({ 
          content: '❌ คุณต้องเข้าห้องเสียง (Voice Channel) ก่อนใช้คำสั่งนี้ครับ!', 
          ephemeral: true 
        });
      }

      const songName = interaction.options.getString('song');
      
      // 🔥 บังคับให้บอทส่งสัญญาณ "กำลังคิด..." เพื่อขยายเวลาตอบกลับเป็น 15 วินาที (แก้บั๊กไม่ตอบสนอง)
      await interaction.deferReply(); 

      try {
        await client.distube.play(voiceChannel, songName, {
          textChannel: interaction.channel,
          member: interaction.member
        });
        
        // เมื่อค้นหาเจอและดึงเพลงเข้าคิวสำเร็จ ให้เปลี่ยนข้อความสถานะ
        await interaction.editReply({ 
          content: `🔍 ค้นหาและเตรียมเล่นเพลง: **${songName}** เรียบร้อยครับ!` 
        });
      } catch (err) {
        console.error(err);
        await interaction.editReply({ 
          content: '❌ เกิดข้อผิดพลาดในการโหลดเพลงนี้ กรุณลองใหม่อีกครั้งครับ' 
        });
      }
    }

    // ==========================================
    // ⏭️ คำสั่ง /skip (ข้ามเพลง)
    // ==========================================
    if (commandName === 'skip') {
      const queue = client.distube.getQueue(interaction.guildId);
      if (!queue) return interaction.reply({ content: '❌ ตอนนี้ไม่มีเพลงที่กำลังเล่นอยู่ครับ', ephemeral: true });

      try {
        await client.distube.skip(interaction.guildId);
        await interaction.reply({ content: '⏭️ ข้ามเพลงปัจจุบันให้เรียบร้อยแล้วครับ!' });
      } catch (err) {
        await interaction.reply({ content: '❌ ไม่สามารถข้ามได้ (อาจเป็นเพลงสุดท้ายในคิวแล้ว)', ephemeral: true });
      }
    }

    // ==========================================
    // ⏹️ คำสั่ง /stop (หยุดเพลงและออกจากห้อง)
    // ==========================================
    if (commandName === 'stop') {
      const queue = client.distube.getQueue(interaction.guildId);
      if (!queue) return interaction.reply({ content: '❌ ตอนนี้ไม่มีเพลงที่กำลังเล่นอยู่ครับ', ephemeral: true });

      await client.distube.stop(interaction.guildId);
      await interaction.reply({ content: '⏹️ หยุดเล่นเพลงและเคลียร์คิวทั้งหมดเรียบร้อยครับ!' });
    }
  }
};