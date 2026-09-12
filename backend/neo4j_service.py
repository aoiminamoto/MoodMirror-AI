import os
from typing import Dict, Iterable, Optional
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()


class Neo4jService:
    """Neo4j Aura wrapper using the HTTPS Query API.

    Aura supports HTTPS on port 443. This is useful on networks that block
    Bolt/routing traffic on port 7687.
    """

    def __init__(self) -> None:
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        missing = [
            name
            for name, value in {
                "NEO4J_URI": self.uri,
                "NEO4J_USERNAME": self.username,
                "NEO4J_PASSWORD": self.password,
            }.items()
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Missing Neo4j environment variables: " + ", ".join(missing)
            )

        self.host = self._extract_host(self.uri)
        self.query_url = f"https://{self.host}/db/{self.database}/query/v2"
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _extract_host(uri: str) -> str:
        parsed = urlparse(uri)
        if parsed.hostname:
            return parsed.hostname

        host = uri
        for prefix in ("neo4j+s://", "neo4j://", "https://", "http://"):
            host = host.replace(prefix, "")
        return host.strip("/")

    def _query(self, statement: str, parameters: Optional[dict] = None) -> dict:
        response = requests.post(
            self.query_url,
            auth=self.auth,
            headers=self.headers,
            json={
                "statement": statement,
                "parameters": parameters or {},
            },
            timeout=30,
        )

        if not response.ok:
            detail = response.text[:1000]
            raise RuntimeError(
                f"Neo4j Query API request failed ({response.status_code}): {detail}"
            )

        payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(f"Neo4j returned errors: {payload['errors']}")
        return payload

    @staticmethod
    def _rows(payload: dict):
        data = payload.get("data") or {}
        fields = data.get("fields") or []
        values = data.get("values") or []
        return [dict(zip(fields, row)) for row in values]

    def verify_connection(self) -> None:
        self._query("RETURN 1 AS ok")

    def close(self) -> None:
        # requests uses short-lived HTTPS calls, so there is no persistent
        # Neo4j driver connection to close.
        return None

    def create_constraints(self) -> None:
        statements = [
            "CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT pattern_name_unique IF NOT EXISTS FOR (p:Pattern) REQUIRE p.name IS UNIQUE",
            "CREATE CONSTRAINT topic_name_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
        ]
        for statement in statements:
            self._query(statement)

    def save_entry(
        self,
        user_id: str,
        text: str,
        features: Dict[str, float],
        topics: Optional[Iterable[str]] = None,
    ) -> str:
        feature_rows = [
            {"name": name, "score": float(score)}
            for name, score in features.items()
        ]
        topic_rows = list(topics or [])

        query = """
        MERGE (u:User {id: $user_id})
        CREATE (e:Entry {
            id: randomUUID(),
            text: $text,
            created_at: datetime()
        })
        MERGE (u)-[:WROTE]->(e)

        WITH e
        UNWIND $features AS f
        MERGE (p:Pattern {name: f.name})
        CREATE (e)-[:HAS_PATTERN {score: f.score}]->(p)

        WITH e
        FOREACH (topic_name IN $topics |
            MERGE (t:Topic {name: topic_name})
            MERGE (e)-[:MENTIONS]->(t)
        )

        RETURN e.id AS entry_id
        """

        payload = self._query(
            query,
            {
                "user_id": user_id,
                "text": text,
                "features": feature_rows,
                "topics": topic_rows,
            },
        )
        rows = self._rows(payload)
        if not rows:
            raise RuntimeError("Neo4j did not return an entry id")
        return rows[0]["entry_id"]

    def get_user_pattern_history(self, user_id: str, pattern_name: str):
        query = """
        MATCH (u:User {id: $user_id})-[:WROTE]->(e:Entry)
              -[r:HAS_PATTERN]->(p:Pattern {name: $pattern_name})
        RETURN e.id AS entry_id,
               toString(e.created_at) AS created_at,
               r.score AS score
        ORDER BY e.created_at ASC
        """
        payload = self._query(
            query,
            {
                "user_id": user_id,
                "pattern_name": pattern_name,
            },
        )
        return self._rows(payload)
