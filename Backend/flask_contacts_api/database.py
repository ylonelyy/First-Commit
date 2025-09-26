from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['contacts_db']
contacts_collection = db['contacts']

def get_all_contacts():
    return list(contacts_collection.find({}))

def get_contact_by_email(email):
    return contacts_collection.find_one({'email': email})

def add_contact(contact):
    # exige campo email
    if 'email' not in contact:
        return None
    # evita duplicados
    existing = contacts_collection.find_one({'email': contact['email']})
    if existing:
        return None
    # insere e retorna o documento (sem _id)
    contacts_collection.insert_one(contact)
    return contacts_collection.find_one({'email': contact['email']})


def update_contact(email, data):
    result = contacts_collection.update_one({'email': email}, {'$set': data})
    if result.matched_count:
        return get_contact_by_email(email)
    return None

def delete_contact(email):
    result = contacts_collection.delete_one({'email': email})
    return result.deleted_count > 0