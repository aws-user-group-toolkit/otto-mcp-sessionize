import os

import requests
from mcp.server.fastmcp import FastMCP

class SessionizeApi:

    def __init__(self):
        self.url = os.environ.get("SESSIONIZE_URL")
        self.dateFilterCategoryId = int(
            os.environ.get("SESSIONIZE_DATE_FILTER_CATEGORY_ID")
        )

    def get_sessions(self):
        response = requests.get(self.url)
        return response.json()

    def get_sessions_by_date(self, date):
        sessions = self.get_sessions()
        filtered = []
        for group in sessions:
            for session in group["sessions"]:
                for category in session["categories"]:
                    if category["id"] == self.dateFilterCategoryId:
                        for item in category["categoryItems"]:
                            if item["name"] == date:
                                filtered.append(session)
        return self._format_sessions(filtered)

    def _format_sessions(self, sessions):
        formattedSessions = ""
        for session in sessions:
            formattedSessions += (
                "###### SESSION ######\n"
                f'Title: {session["title"]}\n\n'
                f'Description:\n{session["description"]}\n\n'
                "Speakers:\n"
            )

            for speaker in session["speakers"]:
                formattedSessions += f'{speaker["name"]}\n'
            formattedSessions += "\n###### END SESSION ######\n\n"

        return formattedSessions

mcp = FastMCP("sessionize", host="0.0.0.0", port=8080, stateless_http=True, json_response=True)


@mcp.tool()
def search_sessionize(date: str) -> str:
    """
    Searches Sessionize for potential speakers and talks for a given month in
    'Month Year' format (e.g., 'April 2025').
    """

    sessionize = SessionizeApi()
    return sessionize.get_sessions_by_date(date)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
