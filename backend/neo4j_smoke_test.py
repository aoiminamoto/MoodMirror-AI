from backend.neo4j_service import Neo4jService


def main() -> None:
    service = Neo4jService()
    try:
        service.verify_connection()
        service.create_constraints()

        entry_id = service.save_entry(
            user_id="demo-user",
            text="I am preparing for my interview and learning vision engineering today.",
            features={
                "future_orientation": 0.82,
                "action_orientation": 0.79,
                "uncertainty": 0.34,
            },
            topics=["Career", "Learning"],
        )

        history = service.get_user_pattern_history(
            user_id="demo-user",
            pattern_name="future_orientation",
        )

        print("Neo4j connection: OK")
        print(f"Created Entry: {entry_id}")
        print("future_orientation history:")
        for row in history:
            print(row)
    finally:
        service.close()


if __name__ == "__main__":
    main()
