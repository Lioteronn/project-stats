import logging

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement

logger = logging.getLogger("nextcord")


def setup_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        }
    )
    return session


class StatsScrapper:
    def __init__(self, url: str):
        self.session = setup_session()
        self.html = self._get_stats_from_url(url)
        self.stats_container = self._get_stats_container(self.html)

    def _traverse_nodes(self, from_node: PageElement, nodes: list[str]) -> PageElement:
        current = from_node
        for node in nodes:
            current = current.find_next(node)
            if not current:
                raise ValueError(f"Node {node} not found")
        return current

    def _get_stats_from_url(self, url: str) -> str:
        try:
            response = self.session.get(url)
            if response.status_code != 200:
                logger.error(f"Failed to get stats from {url}: {response.status_code}")
                raise ValueError(
                    f"Failed to get stats from {url}: {response.status_code}"
                )
            return response.text
        except Exception as e:
            logger.error(f"Error fetching stats from {url}: {e}")
            raise ValueError(f"Error fetching stats from {url}: {e}")

    def _get_stats_container(self, html: str) -> PageElement:
        soup = BeautifulSoup(html, "html.parser")
        root_div = soup.find("div", class_="rematch")
        if root_div is None:
            raise ValueError("Root div not found")

        # Navigate step by step with null checks
        current = root_div.find_next("main")
        if current is None:
            raise ValueError("Current div not found")

        current = self._traverse_nodes(
            current, ["div", "section", "div", "div", "div", "div"]
        )

        # Get the second child (index 1)
        children_divs = list(current.find_all("div", recursive=False))
        stats_container = children_divs[1]

        if stats_container is None:
            raise ValueError("Stats container not found")

        return stats_container

    def _get_name(self) -> str:
        name = self._traverse_nodes(
            self.stats_container, ["div", "div:nth-child(2)", "div", "span"]
        )

        return name.text.strip()

    def _get_level(self) -> str:
        level = self._traverse_nodes(
            self.stats_container, ["div", "div", "div:nth-child(2)"]
        )

        return level.text.strip()

    def _get_match_stats(self) -> dict[str, str]:
        match_stats_container = self._traverse_nodes(
            self.stats_container,
            [
                "div:nth-child(2)",
                "div",
                "div",
                "div",
                "div",
                "div:nth-child(2)",
            ],
        )

        stats = {
            "rank": self._traverse_nodes(
                match_stats_container,
                # TODO: ["div:nth-child(2)", "div", "div:nth-child(2)", "div"],
            ).text.strip(),
        }

        return stats

    def _get_all_stats(self) -> dict[str, str]:
        lifetime_stats_container = self._traverse_nodes(
            self.stats_container,
            [
                "div:nth-child(2)",
                "div",
                "div",
                "div",
                "div",
                "div",
                "div:nth-child(2)",
                "div",
            ],
        )

        stats = {
            "wins": self._traverse_nodes(
                lifetime_stats_container, ["div", "div"]
            ).text.strip(),
            "goals": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(2)"]
            ).text.strip(),
            "shots": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(3)"]
            ).text.strip(),
            "assists": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(4)"]
            ).text.strip(),
            "saves": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(5)"]
            ).text.strip(),
            "steals": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(6)"]
            ).text.strip(),
            "tackles": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(7)"]
            ).text.strip(),
            "mvps": self._traverse_nodes(
                lifetime_stats_container, ["div", "div:nth-child(8)"]
            ).text.strip(),
        }

        return stats
