import random
from discord.ext import commands
import discord
from utils.database import load_cards

# Couleurs et emojis par rareté
RARITY_COLORS = {
    "Common": 0x95a5a6,
    "Rare": 0x3498db,
    "Epic": 0x9b59b6,
    "Legendary": 0xf1c40f
}

RARITY_EMOJIS = {
    "Common": "⚪",
    "Rare": "🔵",
    "Epic": "🟣",
    "Legendary": "🟡"
}

DROP_RATES = {
    "Common": 0.5,
    "Rare": 0.3,
    "Epic": 0.15,
    "Legendary": 0.05
}

POINTS_REWARD = {
    "Common": 1,
    "Rare": 2,
    "Epic": 3,
    "Legendary": 5
}

class Packs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = load_cards()["cards"]

    def draw_card(self):
        rarities = list(DROP_RATES.keys())
        probabilities = list(DROP_RATES.values())
        chosen_rarity = random.choices(rarities, probabilities, k=1)[0]

        filtered_cards = [card for card in self.cards if card["rarity"] == chosen_rarity]
        card = random.choice(filtered_cards)

        num_cards_same_rarity = len(filtered_cards)
        exact_rate = DROP_RATES[chosen_rarity] / num_cards_same_rarity * 100

        return card, exact_rate

    @commands.command(name="pack")
    async def pack_menu(self, ctx):
        """Menu pour ouvrir un pack"""
        embed = discord.Embed(
            title="🎁 Bienvenue dans le jeu de packs !",
            description=(
                "🔹 Le but du jeu est d'ouvrir des packs pour obtenir des cartes.\n"
                "🔹 Chaque carte a une rareté différente avec un taux de drop précis.\n"
                "🔹 Tu gagnes des points selon la rareté de la carte :\n"
                "⚪ Common = 1 point\n"
                "🔵 Rare = 2 points\n"
                "🟣 Epic = 3 points\n"
                "🟡 Legendary = 5 points\n\n"
                "Appuie sur le bouton ci-dessous pour ouvrir ton premier pack !"
            ),
            color=0x1abc9c
        )

        view = discord.ui.View()
        button = discord.ui.Button(label="Ouvrir un pack", style=discord.ButtonStyle.green)

        async def open_pack_callback(interaction):
            card, rate = self.draw_card()
            points = POINTS_REWARD.get(card["rarity"], 1)

            pack_embed = discord.Embed(
                title="🎉 Pack Ouvert !",
                description=f"Tu as obtenu une carte !",
                color=RARITY_COLORS.get(card["rarity"], 0xffffff)
            )
            pack_embed.add_field(name="👤 Joueur", value=card["player"], inline=False)
            pack_embed.add_field(name="🏟️ Club", value=card["club"], inline=False)
            pack_embed.add_field(name=f"{RARITY_EMOJIS.get(card['rarity'],'⭐')} Rareté", value=card["rarity"], inline=False)
            pack_embed.add_field(name="🎯 Taux de drop", value=f"{rate:.2f}%", inline=False)
            pack_embed.add_field(name="🏆 Points gagnés", value=f"{points}", inline=False)

            await interaction.response.edit_message(embed=pack_embed, view=view)

        button.callback = open_pack_callback
        view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Packs(bot))
