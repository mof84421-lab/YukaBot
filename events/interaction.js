const { ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');

module.exports = {
  name: 'interactionCreate',
  async execute(interaction, client) {
    
    // 1. จัดการคำสั่ง Slash Commands ( / )
    if (interaction.isChatInputCommand()) {
      if (interaction.commandName === 'ping') {
        return interaction.reply(`🏓 พง! ความเร็ว: ${client.ws.ping}ms`);
      }

      if (interaction.commandName === 'setup-verify') {
        if (!interaction.member.permissions.has('Administrator')) {
          return interaction.reply({ content: '❌ เฉพาะแอดมินเท่านั้นครับ!', ephemeral: true });
        }

        const row = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId('verify_button')
            .setLabel('✅ กดยืนยันตัวตน')
            .setStyle(ButtonStyle.Success)
        );

        return interaction.reply({
          content: '⚙️ **ระบบยืนยันตัวตน**\nกรุณากดปุ่มด้านล่างเพื่อเข้าสู่เซิร์ฟเวอร์ครับ',
          components: [row]
        });
      }
    }

    // 2. จัดการระบบปุ่มกด (Buttons)
    if (interaction.isButton()) {
      if (interaction.customId === 'verify_button') {
        const roleName = 'Member'; // ยศที่ต้องการแจก
        const role = interaction.guild.roles.cache.find(r => r.name === roleName);

        if (!role) return interaction.reply({ content: '❌ ไม่เจอยศในระบบ', ephemeral: true });
        if (interaction.member.roles.cache.has(role.id)) {
          return interaction.reply({ content: '🤝 คุณยืนยันตัวตนไปแล้ว!', ephemeral: true });
        }

        try {
          await interaction.member.roles.add(role);
          await interaction.reply({ content: '🎉 ผ่านการยืนยันตัวตนเรียบร้อยครับ!', ephemeral: true });
        } catch (err) {
          await interaction.reply({ content: '❌ บอทไม่มีอำนาจให้ยศ (ให้ลากยศบอทขึ้นไว้เหนทอยศ Member ในตั้งค่าดิสคอร์ด)', ephemeral: true });
        }
      }
    }
  },
};