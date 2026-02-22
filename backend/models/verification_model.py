# # from datetime import datetime
# # from bson import ObjectId

# # class VerificationModel:
# #     @staticmethod
# #     def create_verification(db, document_id, user_id, risk_score, risk_level, 
# #                           verification_result, fraud_indicators, auto_decision, 
# #                           gemini_response, embedding):
# #         verification = {
# #             'document_id': ObjectId(document_id),
# #             'user_id': ObjectId(user_id),
# #             'risk_score': risk_score,
# #             'risk_level': risk_level,
# #             'verification_result': verification_result,
# #             'fraud_indicators': fraud_indicators,
# #             'auto_decision': auto_decision,
# #             'gemini_response': gemini_response,
# #             'embedding': embedding,
# #             'status': 'pending' if auto_decision == 'manual_review' else auto_decision,
# #             'officer_decision': None,
# #             'officer_notes': None,
# #             'officer_id': None,
# #             'created_at': datetime.utcnow(),
# #             'updated_at': datetime.utcnow()
# #         }
# #         result = db.verifications.insert_one(verification)
# #         return result.inserted_id
    
# #     @staticmethod
# #     def find_by_id(db, verification_id):
# #         return db.verifications.find_one({'_id': ObjectId(verification_id)})
    
# #     @staticmethod
# #     def find_by_document(db, document_id):
# #         return db.verifications.find_one({'document_id': ObjectId(document_id)})
    
# #     @staticmethod
# #     def find_by_user(db, user_id):
# #         return list(db.verifications.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))
    
# #     @staticmethod
# #     def find_pending(db):
# #         return list(db.verifications.find({'status': 'pending'}).sort('created_at', -1))
    
# #     @staticmethod
# #     def find_all(db):
# #         return list(db.verifications.find().sort('created_at', -1))
    
# #     @staticmethod
# #     def update_officer_decision(db, verification_id, officer_id, decision, notes):
# #         db.verifications.update_one(
# #             {'_id': ObjectId(verification_id)},
# #             {
# #                 '$set': {
# #                     'status': decision,
# #                     'officer_decision': decision,
# #                     'officer_notes': notes,
# #                     'officer_id': ObjectId(officer_id),
# #                     'updated_at': datetime.utcnow()
# #                 }
# #             }
# #         )
    
# #     @staticmethod
# #     def find_duplicates(db, embedding, threshold=0.95):
# #         all_verifications = list(db.verifications.find({'embedding': {'$exists': True}}))
# #         return all_verifications


# # models/verification_model.py

# from datetime import datetime
# from bson import ObjectId
# from extensions.db import mongo


# class VerificationModel:

#     @staticmethod
#     def create_verification(
#         document_id,
#         user_id,
#         risk_score,
#         risk_level,
#         verification_result,
#         fraud_indicators,
#         auto_decision,
#         gemini_response,
#         embedding
#     ):
#         verification = {
#             'document_id': ObjectId(document_id),
#             'user_id': ObjectId(user_id),
#             'risk_score': risk_score,
#             'risk_level': risk_level,
#             'verification_result': verification_result,
#             'fraud_indicators': fraud_indicators,
#             'auto_decision': auto_decision,
#             'gemini_response': gemini_response,
#             'embedding': embedding,
#             'status': 'pending' if auto_decision == 'manual_review' else auto_decision,
#             'officer_decision': None,
#             'officer_notes': None,
#             'officer_id': None,
#             'created_at': datetime.utcnow(),
#             'updated_at': datetime.utcnow()
#         }

#         result = mongo.db.verifications.insert_one(verification)
#         return result.inserted_id

#     @staticmethod
#     def find_by_id(verification_id):
#         return mongo.db.verifications.find_one({
#             '_id': ObjectId(verification_id)
#         })

#     @staticmethod
#     def find_by_document(document_id):
#         return mongo.db.verifications.find_one({
#             'document_id': ObjectId(document_id)
#         })

#     @staticmethod
#     def find_by_user(user_id):
#         return list(
#             mongo.db.verifications.find(
#                 {'user_id': ObjectId(user_id)}
#             ).sort('created_at', -1)
#         )

#     @staticmethod
#     def find_pending():
#         return list(
#             mongo.db.verifications.find(
#                 {'status': 'pending'}
#             ).sort('created_at', -1)
#         )

#     @staticmethod
#     def find_all():
#         return list(
#             mongo.db.verifications.find().sort('created_at', -1)
#         )

#     @staticmethod
#     def update_officer_decision(verification_id, officer_id, decision, notes):
#         mongo.db.verifications.update_one(
#             {'_id': ObjectId(verification_id)},
#             {
#                 '$set': {
#                     'status': decision,
#                     'officer_decision': decision,
#                     'officer_notes': notes,
#                     'officer_id': ObjectId(officer_id),
#                     'updated_at': datetime.utcnow()
#                 }
#             }
#         )

#     @staticmethod
#     def find_duplicates(embedding, threshold=0.95):
#         # Placeholder logic — customize similarity later
#         return list(
#             mongo.db.verifications.find({'embedding': {'$exists': True}})
#         )

# models/verification_model.py

from datetime import datetime
from bson import ObjectId
from extensions.db import mongo


class VerificationModel:

    @staticmethod
    def create_verification(
        document_id,
        user_id,
        risk_score,
        risk_level,
        verification_result,
        fraud_indicators,
        auto_decision,
        gemini_response,
        embedding
    ):
        verification = {
            "document_id": ObjectId(document_id),
            "user_id": ObjectId(user_id),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "verification_result": verification_result,
            "fraud_indicators": fraud_indicators,
            "auto_decision": auto_decision,
            "gemini_response": gemini_response,
            "embedding": embedding,
            "status": "pending" if auto_decision == "manual_review" else auto_decision,
            "officer_decision": None,
            "officer_notes": None,
            "officer_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = mongo.db.verifications.insert_one(verification)
        return result.inserted_id

    @staticmethod
    def find_by_id(verification_id):
        return mongo.db.verifications.find_one({"_id": ObjectId(verification_id)})

    @staticmethod
    def find_by_document(document_id):
        return mongo.db.verifications.find_one({
            "document_id": ObjectId(document_id)
        })

    @staticmethod
    def find_by_user(user_id):
        return list(
            mongo.db.verifications
            .find({"user_id": ObjectId(user_id)})
            .sort("created_at", -1)
        )

    @staticmethod
    def find_pending():
        return list(
            mongo.db.verifications
            .find({"status": "pending"})
            .sort("created_at", -1)
        )

    @staticmethod
    def find_all():
        return list(
            mongo.db.verifications
            .find()
            .sort("created_at", -1)
        )

    @staticmethod
    def update_officer_decision(verification_id, officer_id, decision, notes):
        mongo.db.verifications.update_one(
            {"_id": ObjectId(verification_id)},
            {
                "$set": {
                    "status": decision,
                    "officer_decision": decision,
                    "officer_notes": notes,
                    "officer_id": ObjectId(officer_id),
                    "updated_at": datetime.utcnow()
                }
            }
        )

    @staticmethod
    def find_duplicates(embedding):
        return list(
            mongo.db.verifications.find({"embedding": {"$exists": True}})
        )