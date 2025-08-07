"""Balance-related HTTP routes."""
import logging
import azure.functions as func
from services.cost_basis import calculate_cost_basis
from assets.asset_pairs import BTCEUR, ETHEUR, SOLEUR, PAXGEUR
from utils.html_renderer import html
from utils.kraken_client import user


def get_balance(req: func.HttpRequest) -> func.HttpResponse:
    """Fetches and returns the account balance from Kraken."""
    account_balance = user.get_account_balance()

    asset_to_eur_map = {
        "XXBT": BTCEUR(),
        "XETH": ETHEUR(),
        "SOL": SOLEUR(),
        "PAXG": PAXGEUR(),
    }

    balance = {}

    for asset, amount_str in account_balance.items():
        amount = float(amount_str)

        if amount == 0:
            continue

        if asset == "ZEUR":
            balance[asset] = {
                "amount": round(amount, 2),
                "price": 0,
                "cost_basis": 0,
                "average_price": 0,
                "unrealized_pnl": 0,
                "unrealized_pnl_pct": 0,
            }
            continue

        asset_pair = asset_to_eur_map[asset]

        if asset_pair is None:
            logging.warning(f"No asset pair found for {asset}, skipping.")
            continue

        cost_basis = calculate_cost_basis(asset_pair, amount)

        balance[asset] = {
            "amount": amount,
            "price": amount * asset_pair.get_asset_price(),
            "cost_basis": cost_basis,
            "average_price": cost_basis / amount if amount > 0 else 0,
            "unrealized_pnl": asset_pair.get_asset_price() * amount - cost_basis,
            "unrealized_pnl_pct": (
                (
                    (asset_pair.get_asset_price() * amount - cost_basis)
                    / cost_basis
                    * 100
                )
                if cost_basis > 0
                else 0
            ),
        }

    return html(template="balance.html.j2", balance=balance)
