from discord.ext import commands
from utils.database import load_cards

class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="carte")
    async def carte_info(self, ctx, card_id: int):
        """Affiche les infos d'une carte via son ID."""
        data = load_cards()
        for card in data["cards"]:
            if card["id"] == card_id:
                await ctx.send(
                    f"**Carte #{card_id}**\n"
                    f"👤 Joueur : {card['player']}\n"
                    f"🏟️ Club : {card['club']}\n"
                    f"🔶 Rareté : {card['rarity']}"
                )
                return

        await ctx.send("❌ Carte introuvable.")

    @commands.command(name="cartes")
    async def cartes_club(self, ctx, type: str, *, club: str):
        """Affiche les cartes d'un club."""
        if type.lower() != "club":
            return await ctx.send("Usage : `!cartes club <nom du club>`")

        data = load_cards()
        results = [
            c for c in data["cards"]
            if c["club"].lower() == club.lower()
        ]

        if not results:
            return await ctx.send("❌ Aucun joueur trouvé pour ce club.")

        message = f"📌 **Cartes du club {club}**\n"
        for card in results:
            message += f"- #{card['id']} : {card['player']} ({card['rarity']})\n"

        await ctx.send(message)

    @commands.command(name="rarete")
    async def cartes_rarete(self, ctx, rarity: str):
        """Affiche les cartes d'une certaine rareté."""
        data = load_cards()
        results = [
            c for c in data["cards"]
            if c["rarity"].lower() == rarity.lower()
        ]

        if not results:
            return await ctx.send("❌ Aucune carte dans cette rareté.")

        message = f"💎 **Cartes de rareté {rarity}**\n"
        for card in results:
            message += f"- #{card['id']} : {card['player']} ({card['club']})\n"

        await ctx.send(message)


# OBLIGATOIRE POUR DISCORD.PY 2.x
async def setup(bot):
    await bot.add_cog(Cards(bot))
