import firebase_admin
from firebase_admin import credentials, auth, firestore

# Inicializa Firebase
def iniciar_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

# Login manual simples (apenas exemplo com e-mail)
def verificar_usuario(email):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except:
        return None

# Criar novo usuário (registro)
def criar_usuario(email, senha):
    try:
        user = auth.create_user(email=email, password=senha)
        return user.uid
    except Exception as e:
        return str(e)

# Salvar conversa no Firestore
def salvar_conversa(uid, pergunta, resposta, hora):
    db = firestore.client()
    doc_ref = db.collection("historico").document(uid)
    doc_ref.set({
        "mensagens": firestore.ArrayUnion([{
            "hora": hora,
            "pergunta": pergunta,
            "resposta": resposta
        }])
    }, merge=True)

# Buscar histórico
def buscar_historico(uid):
    db = firestore.client()
    doc_ref = db.collection("historico").document(uid)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("mensagens", [])
    return []
