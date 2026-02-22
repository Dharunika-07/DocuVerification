# # from datetime import datetime
# # from bson import ObjectId

# # class DocumentModel:
# #     @staticmethod
# #     def create_document(db, user_id, filename, file_path, document_type, extracted_text):
# #         document = {
# #             'user_id': ObjectId(user_id),
# #             'filename': filename,
# #             'file_path': file_path,
# #             'document_type': document_type,
# #             'extracted_text': extracted_text,
# #             'status': 'pending',
# #             'uploaded_at': datetime.utcnow()
# #         }
# #         result = db.documents.insert_one(document)
# #         return result.inserted_id
    
# #     @staticmethod
# #     def find_by_id(db, document_id):
# #         return db.documents.find_one({'_id': ObjectId(document_id)})
    
# #     @staticmethod
# #     def find_by_user(db, user_id):
# #         return list(db.documents.find({'user_id': ObjectId(user_id)}).sort('uploaded_at', -1))
    
# #     @staticmethod
# #     def find_all(db):
# #         return list(db.documents.find().sort('uploaded_at', -1))
    
# #     @staticmethod
# #     def update_status(db, document_id, status):
# #         db.documents.update_one(
# #             {'_id': ObjectId(document_id)},
# #             {'$set': {'status': status}}
# #         )

# from datetime import datetime
# from bson import ObjectId
# from extensions.db import mongo

# class DocumentModel:

#     @staticmethod
#     def create_document(user_id, filename, file_path, document_type, extracted_text):
#         document = {
#             'user_id': ObjectId(user_id),
#             'filename': filename,
#             'file_path': file_path,
#             'document_type': document_type,
#             'extracted_text': extracted_text,
#             'status': 'pending',
#             'uploaded_at': datetime.utcnow()
#         }
#         result = mongo.db.documents.insert_one(document)
#         return result.inserted_id

#     @staticmethod
#     def find_by_id(document_id):
#         return mongo.db.documents.find_one({'_id': ObjectId(document_id)})

#     @staticmethod
#     def find_by_user(user_id):
#         return list(mongo.db.documents.find(
#             {'user_id': ObjectId(user_id)}
#         ).sort('uploaded_at', -1))


# models/document_model.py

from datetime import datetime
from bson import ObjectId
from extensions.db import mongo


class DocumentModel:

    @staticmethod
    def create_document(user_id, filename, file_path, document_type, extracted_text):
        document = {
            "user_id": ObjectId(user_id),
            "filename": filename,
            "file_path": file_path,
            "document_type": document_type,
            "extracted_text": extracted_text,
            "status": "pending",
            "uploaded_at": datetime.utcnow()
        }

        result = mongo.db.documents.insert_one(document)
        return result.inserted_id

    @staticmethod
    def find_by_id(document_id):
        return mongo.db.documents.find_one({"_id": ObjectId(document_id)})

    @staticmethod
    def find_by_user(user_id):
        return list(
            mongo.db.documents
            .find({"user_id": ObjectId(user_id)})
            .sort("uploaded_at", -1)
        )

    @staticmethod
    def find_all():
        return list(
            mongo.db.documents
            .find()
            .sort("uploaded_at", -1)
        )

    @staticmethod
    def update_status(document_id, status):
        mongo.db.documents.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {"status": status}}
        )