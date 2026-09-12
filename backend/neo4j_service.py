import os
from typing import Dict, Iterable, Optional

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


class Neo4jService:
    """Small Neo4j Aura wrapper for MoodMirror's longitudinal graph."""

    def __init__(self) -> None:
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")

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

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        )

    def verify_connection(self) -> None:
        self.driver.verify_connectivity()

    def close(self) -> None:
        self.driver.close()

    def create_constraints(self) -> None:
        statements = [
            "CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT pattern_name_unique IF NOT EXISTS FOR (p:Pattern) REQUIRE p.name IS UNIQUE",
            "CREATE CONSTRAINT topic_name_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
        ]
        with self.driver.session() as session:
            for statement in statements:
                session.run(statement).consume()

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

        with self.driver.session() as session:
            record = session.run(
                query,
                user_id=user_id,
                text=text,
                features=feature_rows,
                topics=topic_rows,
            ).single()

        if record is None:
            raise RuntimeError("Neo4j did not return an entry id")
        return record["entry_id"]

    def get_user_pattern_history(self, user_id: str, pattern_name: str):
        query = """
        MATCH (u:User {id: $user_id})-[:WROTE]->(e:Entry)
              -[r:HAS_PATTERN]->(p:Pattern {name: $pattern_name})
        RETURN e.id AS entry_id,
               e.created_at AS created_at,
               r.score AS score
        ORDER BY e.created_at ASC
        """
        with self.driver.session() as session:
            return [
                dict(record)
                for record in session.run(
                    query,
                    user_id=user_id,
                    pattern_name=pattern_name,
                )
            ]
