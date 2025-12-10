import random
from discord.ext import commands
import discord
from utils.database import load_cards

# Couleurs par rareté
RARITY_COLORS = {
    "Common": 0x95a5a6,    # Gris
    "Rare": 0x3498db,      # Bleu
    "Epic": 0x9b59b6,      # Violet
    "Legendary": 0xf1c40f  # Or
}

RARITY_EMOJIS = {
    "Common": "⚪",
    "Rare": "🔵",
    "Epic": "🟣",
    "Legendary": "🟡"
}

class Packs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pack")
    async def open_pack(self, ctx):
        """Ouvre un pack et donne une carte aléatoire parmi toutes les cartes."""
        data = load_cards()
        cards = data["cards"]

        card = random.choice(cards)

        # Embed Discord
        embed = discord.Embed(
            title="🎉 Pack Ouvert !",
            description=f"Tu as obtenu une carte !",
            color=RARITY_COLORS.get(card["rarity"], 0xffffff)
        )

        embed.add_field(name="👤 Joueur", value=card["player"], inline=False)
        embed.add_field(name="🏟️ Club", value=card["club"], inline=False)
        embed.add_field(name=f"{RARITY_EMOJIS.get(card['rarity'],'⭐')} Rareté", value=card["rarity"], inline=False)

        # Tu peux ajouter une image si tu veux (exemple) :
        # embed.set_thumbnail(url="https://link-to-card-image.png")

        await ctx.send(embed=embed)

# Pour discord.py 2.x
async def setup(bot):
    await bot.add_cog(Packs(bot))
