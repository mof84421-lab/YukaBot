module.exports = {
  name: 'interactionCreate',
  once: false,
  async execute(interaction, client) {
    // 🛡️ เช็คความปลอดภัยล่วงหน้า: ถ้าไม่ใช่คำสั่งสแลช (Slash Command) ให้ดีดกลับทันที ไม่ให้บอทแครช
    if (!interaction || !interaction.isChatInputCommand()) return;

    const { commandName } = interaction;

    try {
      // ==========================================
      // 🎵 คำสั่ง /play (เปิดเพลง)
      // ==========================================
      if (commandName === 'play') {
        const voiceChannel = interaction.member?.voice?.channel;
        if (!voiceChannel) {
          return interaction.reply({ 
            content: '❌ คุณต้องเข้าห้องเสียง (Voice Channel) ก่อนใช้คำสั่งนี้ครับ!', 
            ephemeral: true 
          });
        }

        const songName = interaction.options.getString('song');
        if (!songName) {
          return interaction.reply({ content: '❌ กรุณาระบุชื่อเพลงหรือลิงก์เพลงด้วยครับ', ephemeral: true });
        }
        
        // 🔥 บังคับให้บอทส่งสัญญาณ "กำลังคิด..." ทันที เพื่อป้องกันดิสคอร์ดตัดสายภายใน 3 วินาที
        await interaction.deferReply(); 

        try {
          await client.distube.play(voiceChannel, songName, {
            textChannel: interaction.channel,
            member: interaction.member
          });
          
          // เปลี่ยนข้อความสถานะเมื่อเอาเพลงเข้าคิวสำเร็จ
          await interaction.editReply({ 
            content: `🔍 ค้นหาและเตรียมเล่นเพลง: **${songName}** เรียบร้อยครับ!` 
          });
        } catch (distubeErr) {
          console.error('[DisTube Error]', distubeErr);
          await interaction.editReply({ 
            content: '❌ เกิดข้อผิดพลาดในการโหลดเพลงนี้ (อาจเป็นลิงก์ที่บอทเข้าไม่ถึง) กรุณาลองใหม่อีกครั้งครับ' 
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

    } catch (globalErr) {
      console.error('[Global Interaction Error]', globalErr);
    }
  }
};