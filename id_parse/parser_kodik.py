import requests

class KodikParser:
    """
   Parser for the Kodik player
    """
    def __init__(self, token: str | None = None) -> None:
        self.TOKEN = token or self.get_token()

    def api_request(self, endpoint: str, payload: dict) -> dict:
        """General method for making API requests."""
        if not self.TOKEN:
            return {}

        payload["token"] = self.TOKEN
        response = requests.post(f"https://kodikapi.com/{endpoint}", data=payload)

        if response.status_code != 200:
            return {}

        data = response.json()
        return data if data.get('results') else {}

    def base_search_by_id(self, id: str, limit: int = 50) -> dict:
        """Basic search by ID (Shikimori only)."""
        return self.api_request('search', {
            "shikimori_id": id,
            "limit": limit,
            "with_material_data": 'true'
        })

    def search_by_id(self, id: str, limit: int | None = None):
        """Search by ID and return the first kinopoisk_id."""
        if 'shiki' in id:
            id = id.replace('shiki', '')
        search_data = self.base_search_by_id(id, limit or 50)
        results = search_data.get('results', [])
        return next((res.get('kinopoisk_id') for res in results if res.get('kinopoisk_id')), None)

    @staticmethod
    def get_token() -> str:
        """Attempt to retrieve the Kodik token automatically (may not work)"""
        try:
            script_url = 'https://kodik-add.com/add-players.min.js?v=2'
            data = requests.get(script_url).text
            token_start = data.find('token=') + 7
            return data[token_start:data.find('"', token_start)]
        except:
            return ""
