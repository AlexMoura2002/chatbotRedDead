import streamlit as st
from firebase_utils import iniciar_firebase, verificar_usuario, criar_usuario

# Configuração da página
st.set_page_config(page_title="Login", layout="centered", page_icon="🔐")

# Inicializa Firebase
iniciar_firebase()

# Gerenciar sessão do usuário
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = False
    st.session_state.uid = None

# Se não está logado, exibe o login/cadastro
if not st.session_state.usuario_logado:
    st.title("🔐 Acesso ao Chatbot")
    
    aba = st.radio("Escolha:", ["Login", "Cadastro"])
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if aba == "Login":
        if st.button("Entrar"):
            uid = verificar_usuario(email)
            if uid:
                st.session_state.usuario_logado = True
                st.session_state.uid = uid
                st.success("✅ Login realizado com sucesso!")
                st.experimental_rerun()  # Atualiza a página após login
            else:
                st.error("❌ Usuário não encontrado ou senha incorreta.")
    else:
        if st.button("Cadastrar"):
            uid = criar_usuario(email, senha)
            if "auth" in str(uid):
                st.error(f"Erro: {uid}")
            else:
                st.success("Usuário criado com sucesso! Faça login agora.")

# Se logado, redireciona para o chatbot
if st.session_state.usuario_logado:
    st.switch_page("pages/chatbot.py")
