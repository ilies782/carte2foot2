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

class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def info_joueur(self, ctx, *, player_name: str):
        """Affiche les infos d'une carte via le nom du joueur."""
        data = load_cards()
        card = next((c for c in data["cards"] if c["player"].lower() == player_name.lower()), None)

        if not card:
            return await ctx.send("❌ Carte introuvable pour ce joueur.")

        embed = discord.Embed(
            title=f"🎴 Carte de {card['player']}",
            color=RARITY_COLORS.get(card["rarity"], 0xffffff)
        )
        embed.add_field(name="👤 Joueur", value=card["player"], inline=False)
        embed.add_field(name="🏟️ Club", value=card["club"], inline=False)
        embed.add_field(name=f"{RARITY_EMOJIS.get(card['rarity'], '⭐')} Rareté", value=card["rarity"], inline=False)

        # Optionnel : miniature de joueur si tu veux plus tard
        # embed.set_thumbnail(url="URL_DE_L_IMAGE_DU_JOUEUR")

        await ctx.send(embed=embed)

# Fonction setup pour discord.py 2.x
async def setup(bot):
    await bot.add_cog(Cards(bot))
