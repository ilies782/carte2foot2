import random
import json
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

CURRENCY_REWARD = {
    "Common": 1,
    "Rare": 2,
    "Epic": 3,
    "Legendary": 5
}

PACK_COST = 3

# Fichier simple pour stocker l'argent des joueurs
BALANCE_FILE = "balances.json"

def load_balances():
    try:
        with open(BALANCE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_balances(balances):
    with open(BALANCE_FILE, "w") as f:
        json.dump(balances, f)

class Packs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cards = load_cards()["cards"]
        self.balances = load_balances()

    def get_balance(self, user_id):
        return self.balances.get(str(user_id), 10)  # 10€ de départ

    def add_balance(self, user_id, amount):
        self.balances[str(user_id)] = self.get_balance(user_id) + amount
        save_balances(self.balances)

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
        user_id = ctx.author.id
        balance = self.get_balance(user_id)

        if balance < PACK_COST:
            await ctx.send(f"❌ Tu n'as pas assez d'argent pour ouvrir un pack ! Solde : {balance}€")
            return

        self.add_balance(user_id, -PACK_COST)  # On retire le prix du pack

        embed = discord.Embed(
            title="🎁 Menu Pack",
            description=f"Pack prêt à être ouvert ! Coût : {PACK_COST}€ | Solde actuel : {self.get_balance(user_id)}€",
            color=0x1abc9c
        )

        view = discord.ui.View()
        button = discord.ui.Button(label="Ouvrir un pack", style=discord.ButtonStyle.green)

        async def open_pack_callback(interaction):
            # Tirage de la carte
            card, rate = self.draw_card()
            reward = CURRENCY_REWARD.get(card["rarity"], 1)
            self.add_balance(user_id, reward)

            pack_embed = discord.Embed(
                title="🎉 Pack Ouvert !",
                description=f"Tu as obtenu une carte !",
                color=RARITY_COLORS.get(card["rarity"], 0xffffff)
            )
            pack_embed.add_field(name="👤 Joueur", value=card["player"], inline=False)
            pack_embed.add_field(name="🏟️ Club", value=card["club"], inline=False)
            pack_embed.add_field(name=f"{RARITY_EMOJIS.get(card['rarity'],'⭐')} Rareté", value=card["rarity"], inline=False)
            pack_embed.add_field(name="🎯 Taux de drop", value=f"{rate:.2f}%", inline=False)
            pack_embed.add_field(name="💰 Argent gagné", value=f"{reward}€", inline=False)
            pack_embed.add_field(name="💵 Solde actuel", value=f"{self.get_balance(user_id)}€", inline=False)

            # Bouton pour relancer
            retry_view = discord.ui.View()
            retry_button = discord.ui.Button(label="Ouvrir un autre pack", style=discord.ButtonStyle.green)

            async def retry_callback(retry_interaction):
                await open_pack_callback(retry_interaction)
            retry_button.callback = retry_callback
            retry_view.add_item(retry_button)

            await interaction.response.edit_message(embed=pack_embed, view=retry_view)

        button.callback = open_pack_callback
        view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Packs(bot))
