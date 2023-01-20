import requests
import pandas as pd

from datetime import datetime


class Prizes:
    def __init__(self):
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Access-Control-Allow-Credentials": "true",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": "https://app.prizepicks.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def get_prizes_by_league_id(self, league_id: int) -> dict:
        url = self._build_prize_pick_url(league_id=league_id)
        response = requests.get(url=url, headers=self.headers).json()

        # get projection data.
        df = pd.DataFrame(response["data"])
        projections = df[df["type"] == "projection"]

        # create new column
        projections["new_player_id"] = projections["relationships"].apply(
            lambda x: x["new_player"]["data"]["id"]
        )

        # get player data.
        df = pd.DataFrame(response["included"])
        players = df[df["type"] == "new_player"]

        # Merge player with there data.
        merged_data = projections.merge(
            players, left_on="new_player_id", right_on="id", how="inner"
        )

        merged_data["final_data"] = merged_data.apply(
            lambda row: {
                "name": row["attributes_y"]["name"],
                "position": row["attributes_y"]["position"],
                "team": row["attributes_y"]["team"],
                "image_url": row["attributes_y"]["image_url"],
                "start_time": row["attributes_x"]["start_time"],
                "stat_type": row["attributes_x"]["stat_type"],
                "line_score": row["attributes_x"]["line_score"],
                "description": row["attributes_x"]["description"],
            },
            axis=1,
        )
        final_data = merged_data["final_data"].tolist()

        current_time = datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        response = {"code": 200, "dateTime": timestamp, "prizes": final_data}
        return response

    def _build_prize_pick_url(self, **kwargs) -> str:
        base_url = "https://api.prizepicks.com/projections"

        league_id = kwargs.get("league_id", None)
        if league_id is not None:
            base_url += f"?league_id={league_id}"

        return f"{base_url}&per_page=1&single_stat=true"
