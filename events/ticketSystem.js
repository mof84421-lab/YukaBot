const { ActionRowBuilder, ButtonBuilder, ButtonStyle, ChannelType, PermissionFlagsBits } = require('discord.js');

module.exports = {
  name: 'interactionCreate',
  async execute(interaction, client) {
    
    // 1. คำสั่งสร้างปุ่มแจ้งปัญหา (พิมพ์ /setup-ticket โดยแอดมิน)
    if (interaction.isChatInputCommand() && interaction.commandName === 'setup-ticket') {
      if (!interaction.member.permissions.has(PermissionFlagsBits.Administrator)) {
        return interaction.reply({ content: '❌ เฉพาะแอดมินเท่านั้นครับ!', ephemeral: true });
      }

      const row = new ActionRowBuilder().addComponents(
        new ButtonBuilder()
          .setCustomId('create_ticket')
          .setLabel('📩 เปิดตั๋วติดต่อแอดมิน / แจ้งปัญหา')
          .setStyle(ButtonStyle.Primary)
      );

      return interaction.reply({
        content: '🏢 **ศูนย์ช่วยเหลือและติดต่อสอบถาม (Ticket System)**\nหากมีข้อสงสัย แจ้งปัญหา หรือต้องการติดต่อแอดมิน กรุณากดปุ่มด้านล่างเพื่อเปิดห้องคุยส่วนตัวครับ',
        components: [row]
      });
    }

    // 2. จัดการเมื่อคนกดปุ่ม "เปิดตั๋ว"
    if (interaction.isButton() && interaction.customId === 'create_ticket') {
      const channelName = `ticket-${interaction.user.username}`;
      
      // ตรวจสอบก่อนว่าเคยเปิดไว้หรือยัง ป้องกันคนกดรัว ๆ
      const alreadyTicket = interaction.guild.channels.cache.find(c => c.name === channelName.toLowerCase());
      if (alreadyTicket) return interaction.reply({ content: `❌ คุณมีห้องติดต่อแอดมินอยู่แล้วที่ห้อง ${alreadyTicket} ครับ`, ephemeral: true });

      await interaction.deferReply({ ephemeral: true });

      // สร้างห้องแชทใหม่แบบส่วนตัว
      const ticketChannel = await interaction.guild.channels.create({
        name: channelName,
        type: ChannelType.GuildText,
        permissionOverwrites: [
          { id: interaction.guild.id, deny: [PermissionFlagsBits.ViewChannel] }, // ปิดไม่ให้ทุกคนเห็น
          { id: interaction.user.id, allow: [PermissionFlagsBits.ViewChannel, PermissionFlagsBits.SendMessages] }, // ให้คนกดเห็นและพิมพ์ได้
          // ถ้ามีสตาฟหรือแอดมิน สามารถเอา ID ยศมาใส่ตรงนี้ได้ เพื่อให้ทีมงานร่วมเห็นห้องด้วย
        ],
      });

      // สร้างปุ่มปิดตั๋วในห้องใหม่
      const closeRow = new ActionRowBuilder().addComponents(
        new ButtonBuilder()
          .setCustomId('close_ticket')
          .setLabel('🔒 ปิดตั๋วนี้ (ลบห้อง)')
          .setStyle(ButtonStyle.Danger)
      );

      await ticketChannel.send({
        content: `👋 สวัสดีครับคุณ ${interaction.user}\nนี่คือห้องติดต่อทีมงานส่วนตัวของคุณ กรุณาพิมพ์รายละเอียดเรื่องที่ต้องการแจ้งไว้ได้เลยครับ เจ้าหน้าที่จะรีบมาตอบกลับ\nเมื่อเสร็จสิ้นธุระแล้ว แอดมินหรือคุณสามารถกดปุ่มด้านล่างเพื่อปิดตั๋วได้เลยครับ`,
        components: [closeRow]
      });

      await interaction.editReply({ content: `✅ สร้างห้องติดต่อแอดมินเรียบร้อยแล้วครับ ไปที่ห้องนี้เลย: ${ticketChannel}` });
    }

    // 3. จัดการเมื่อกดปุ่ม "ปิดตั๋ว"
    if (interaction.isButton() && interaction.customId === 'close_ticket') {
      await interaction.reply({ content: '⚠️ ห้องนี้กำลังจะถูกลบภายใน 5 วินาที...' });
      setTimeout(() => {
        interaction.channel.delete().catch(err => console.log('ลบห้องตั๋วไม่ทัน'));
      }, 5000);
    }
  },
};