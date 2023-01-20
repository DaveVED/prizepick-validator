from fastapi import APIRouter, Path
from prize.services.prizes import Prizes

router = APIRouter()

prizes = Prizes()


@router.get("/prizes/{league_id}", tags=["prizes"])
async def read_prizes(
    league_id: int = Path(title="The ID of the leagure to fetch prizes for."),
):
    return prizes.get_prizes_by_league_id(league_id)
