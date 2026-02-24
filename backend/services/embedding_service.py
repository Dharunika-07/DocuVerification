import hashlib
import numpy as np
from extensions.db import mongo


class EmbeddingService:

    @staticmethod
    def generate_embedding(text):
        if not text or len(text.strip()) == 0:
            return [0.0] * 100

        try:
            text_normalized = text.lower().strip()

            hash_obj = hashlib.sha256(text_normalized.encode())
            hash_bytes = hash_obj.digest()

            embedding = []
            for i in range(0, min(len(hash_bytes), 100)):
                embedding.append(float(hash_bytes[i]) / 255.0)

            while len(embedding) < 100:
                embedding.append(0.0)

            return embedding[:100]

        except Exception as e:
            print(f"Error generating embedding: {e}")
            return [0.0] * 100


    @staticmethod
    def calculate_similarity(embedding1, embedding2):
        try:
            if len(embedding1) != len(embedding2):
                min_len = min(len(embedding1), len(embedding2))
                embedding1 = embedding1[:min_len]
                embedding2 = embedding2[:min_len]

            if len(embedding1) == 0:
                return 0.0

            arr1 = np.array(embedding1)
            arr2 = np.array(embedding2)

            dot_product = np.dot(arr1, arr2)
            norm1 = np.linalg.norm(arr1)
            norm2 = np.linalg.norm(arr2)

            if norm1 == 0 or norm2 == 0:
                return 1.0 if np.array_equal(arr1, arr2) else 0.0

            similarity = dot_product / (norm1 * norm2)
            return float(similarity)

        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0


    @staticmethod
    def find_duplicates(current_embedding, threshold=0.99):
        """
        Finds duplicate documents by comparing embeddings.
        """

        try:
            all_verifications = list(
                mongo.db.verifications.find(
                    {"embedding": {"$exists": True}}
                )
            )

            duplicates = []

            for verification in all_verifications:
                stored_embedding = verification.get("embedding")

                if not stored_embedding:
                    continue

                similarity = EmbeddingService.calculate_similarity(
                    current_embedding,
                    stored_embedding
                )

                if similarity >= threshold:
                    duplicates.append({
                        "verification_id": str(verification["_id"]),
                        "document_id": str(verification["document_id"]),
                        "similarity": similarity,
                    })

            return duplicates

        except Exception as e:
            print(f"Error finding duplicates: {e}")
            return []