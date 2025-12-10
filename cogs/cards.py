from discord.ext import commands
from utils.database import load_cards

class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="carte")
    async def carte_info(self, ctx, card_id: int):
        data = load_cards()
        for card in data["cards"]:
            if card["id"] == card_id:
                await ctx.send(
                    f"**Carte #{card_id}**\n"
                    f"👤 Joueur : {card['player']}\n"
                    f"🏟️ Club : {card['club']}\n"
                    f"⭐ Rareté : {card['rarity']}"
                )
                return
        await ctx.send("❌ Carte introuvable.")

# =========================
# Fonction setup pour discord.py 2.x
# =========================
async def setup(bot):
    await bot.add_cog(Cards(bot))
