from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pymongo import MongoClient

from api.application.settings import Settings


class MongoMemoryStore:
    def __init__(self, settings: Settings) -> None:
        client = MongoClient(settings.mongodb_uri)
        database = client[settings.mongodb_database]
        self.memories = database[settings.mongodb_memory_collection]
        self.knowledge = database[settings.mongodb_knowledge_collection]
        self.vector_index = settings.mongodb_vector_index

    def remember_turn(self, user_id: str, session_id: str, text: str, metadata: dict[str, Any]) -> None:
        self.memories.insert_one(
            {
                "user_id": user_id,
                "session_id": session_id,
                "text": text,
                "metadata": metadata,
                "created_at": datetime.now(UTC),
            }
        )

    def retrieve_knowledge(self, query: str, language: str, topic: str, limit: int = 5) -> list[str]:
        cursor = self.knowledge.find(
            {"language": language, "topic": {"$regex": topic, "$options": "i"}, "$text": {"$search": query}},
            {"score": {"$meta": "textScore"}, "content": 1},
        ).sort([("score", {"$meta": "textScore"})]).limit(limit)
        return [document["content"] for document in cursor]

    def retrieve_vector_context(self, embedding: list[float], limit: int = 5) -> list[str]:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.vector_index,
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": max(limit * 10, 50),
                    "limit": limit,
                }
            },
            {"$project": {"content": 1, "score": {"$meta": "vectorSearchScore"}}},
        ]
        return [document["content"] for document in self.knowledge.aggregate(pipeline)]
