import random
from discord.ext import commands
from utils.database import load_cards

class Packs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pack")
    async def open_pack(self, ctx):
        data = load_cards()
        cards = data["cards"]

        chances = {
            "Legendary": 1,
            "Epic": 5,
            "Rare": 20,
            "Common": 74
        }

        rarity = random.choices(
            list(chances.keys()),
            weights=list(chances.values()),
            k=1
        )[0]

        possible_cards = [c for c in cards if c["rarity"] == rarity]

        card = random.choice(possible_cards)

        await ctx.send(
            f"🎉 **Pack ouvert !**\n"
            f"⭐ Rareté obtenue : **{rarity}**\n"
            f"👤 Joueur : **{card['player']}**\n"
            f"🏟️ Club : **{card['club']}**\n"
            f"🃏 ID : {card['id']}"
        )

async def setup(bot):
    await bot.add_cog(Packs(bot))
