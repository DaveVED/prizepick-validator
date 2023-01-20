    def get_prizes_by_league_id(self, league_id: int) -> dict:
        url = f"https://api.prizepicks.com/projections?league_id={league_id}&per_page=1&single_stat=true"
        response = requests.get(url=url, headers=self.headers).json()

        projections_df = pd.json_normalize(
            response["data"], "attributes", ["id", "relationships"]
        )
        projections_df = projections_df[projections_df["type"] == "projection"]
        projections_df = projections_df.rename(
            columns={"relationships.new_player.data.id": "new_player_id"}
        )

        players_df = pd.json_normalize(response["included"], "attributes", ["id"])
        players_df = players_df[players_df["type"] == "new_player"]
        players_df = players_df.rename(columns={"id": "new_player_id"})

        merged_data = pd.merge(
            projections_df, players_df, on="new_player_id", how="inner"
        )

        final_data = merged_data.to_dict("records")

        return final_data