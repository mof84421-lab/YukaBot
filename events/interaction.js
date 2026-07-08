module.exports = {
  name: 'interactionCreate',
  async execute(interaction, client) {
    
    // ==========================================
    // ⌨️ ส่วนที่ 1: จัดการคำสั่งพิมพ์แบบ SLASH COMMANDS (/)
    // ==========================================
    if (interaction.isChatInputCommand()) {
      const { commandName } = interaction;

      // 1. คำสั่งทดสอบระบบ
      if (commandName === 'ping') {
        return interaction.reply({ content: `🏓 ปิงบอทตอนนี้อยู่ที่: \`${client.ws.ping}ms\``, ephemeral: true });
      }

      // 2. คำสั่งตั้งค่าปุ่มยืนยันตัวตน (แอดมิน)
      if (commandName === 'setup-verify') {
        if (!interaction.member.permissions.has('Administrator')) {
          return interaction.reply({ content: '❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้ (เฉพาะแอดมิน)', ephemeral: true });
        }
        // (โค้ดสำหรับส่ง Embed และปุ่มกดยืนยันตัวตนของคุณจะทำงานตรงนี้)
        return interaction.reply({ content: '✅ สร้างระบบยืนยันตัวตนเรียบร้อย!' });
      }

      // 3. คำสั่งตั้งค่าปุ่มเปิดตั๋ว (แอดมิน)
      if (commandName === 'setup-ticket') {
        if (!interaction.member.permissions.has('Administrator')) {
          return interaction.reply({ content: '❌ คุณไม่มีสิทธิ์ใช้งานคำสั่งนี้ (เฉพาะแอดมิน)', ephemeral: true });
        }
        // (โค้ดสำหรับส่ง Embed และปุ่มกดเปิดตั๋วของคุณจะทำงานตรงนี้)
        return interaction.reply({ content: '✅ สร้างระบบตั๋วแจ้งปัญหาเรียบร้อย!' });
      }

      // 🎵 4. คำสั่งระบบเพลง: PLAY
      if (commandName === 'play') {
        const voiceChannel = interaction.member.voice.channel;
        if (!voiceChannel) {
          return interaction.reply({ content: '❌ คุณต้องเข้าห้องเสียง (Voice Channel) ก่อนใช้คำสั่งนี้ครับ!', ephemeral: true });
        }

        const songName = interaction.options.getString('song');
        await interaction.reply({ content: `🔍 กำลังค้นหาและดึงเพลง: **${songName}**...` });

        try {
          await client.distube.play(voiceChannel, songName, {
            textChannel: interaction.channel,
            member: interaction.member
          });
        } catch (err) {
          console.error(err);
          await interaction.editReply({ content: '❌ เกิดข้อผิดพลาดในการเล่นเพลงนี้ กรุณาลองใหม่อีกครั้ง' });
        }
      }

      // 🎵 5. คำสั่งระบบเพลง: SKIP
      if (commandName === 'skip') {
        const queue = client.distube.getQueue(interaction.guildId);
        if (!queue) {
          return interaction.reply({ content: '❌ ตอนนี้ไม่มีเพลงอยู่ในคิวครับ', ephemeral: true });
        }

        try {
          await queue.skip();
          return interaction.reply({ content: '⏭️ ข้ามเพลงปัจจุบันให้แล้วครับ!' });
        } catch (err) {
          return interaction.reply({ content: '❌ ไม่สามารถข้ามเพลงได้ (อาจเหลือเพลงสุดท้ายในคิว)', ephemeral: true });
        }
      }

      // 🎵 6. คำสั่งระบบเพลง: STOP
      if (commandName === 'stop') {
        const queue = client.distube.getQueue(interaction.guildId);
        if (!queue) {
          return interaction.reply({ content: '❌ ตอนนี้ไม่มีเพลงที่เล่นอยู่ครับ', ephemeral: true });
        }

        try {
          await queue.stop();
          return interaction.reply({ content: '🛑 หยุดเล่นเพลง ล้างคิวทั้งหมด และออกจากห้องเสียงเรียบร้อยครับ!' });
        } catch (err) {
          return interaction.reply({ content: '❌ เกิดข้อผิดพลาดในการสั่งหยุดเพลง', ephemeral: true });
        }
      }
    }

    // ==========================================
    // 🔘 ส่วนที่ 2: จัดการระบบ ปุ่มกด (BUTTONS) เดิมของคุณ
    // ==========================================
    if (interaction.isButton()) {
      const { customId } = interaction;

      // ระบบปุ่มกดยืนยันตัวตน
      if (customId === 'verify_button') {
        // โค้ดแจกยศยืนยันตัวตนเดิมของคุณใส่ตรงนี้ได้เลยครับ...
        await interaction.reply({ content: '✅ คุณผ่านการยืนยันตัวตนแล้วครับ!', ephemeral: true });
      }

      // ระบบปุ่มกดเปิดตั๋วแจ้งปัญหา
      if (customId === 'create_ticket') {
        // โค้ดสร้างห้องตั๋วแอดมินเดิมของคุณใส่ตรงนี้ได้เลยครับ...
        await interaction.reply({ content: '🎫 กำลังสร้างห้องตั๋วส่วนตัวให้คุณสักครู่ครับ...', ephemeral: true });
      }
    }
  },
};