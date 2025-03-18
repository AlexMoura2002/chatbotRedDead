import streamlit as st
import time
import fitz  # PyMuPDF para leitura do PDF
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.utils import gerar_resposta
from firebase_utils import salvar_conversa, buscar_historico

st.set_page_config(page_title="Curiosidades Red Dead", layout="wide", page_icon="🤠")

# Verifica se o usuário está logado
if not st.session_state.get("usuario_logado"):
    st.warning("⚠️ Acesso negado! Faça login primeiro.")
    st.stop()

# Função para extrair texto do PDF
def extrair_texto_pdf(pdf_path):
    texto = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            texto += page.get_text("text") + "\n"
    return texto

# Função para buscar resposta no PDF
def buscar_resposta_no_pdf(pergunta, conteudo_pdf):
    linhas = conteudo_pdf.split("\n")
    for i, linha in enumerate(linhas):
        if pergunta.lower() in linha.lower():
            return linhas[i + 1] if i + 1 < len(linhas) else "Não encontrei uma resposta exata, mas posso tentar ajudar!"
    return None

# Carregar conteúdo do PDF
pdf_path = "Curiosidades_RedDead.pdf"
conteudo_pdf = extrair_texto_pdf(pdf_path)

# Cabeçalho
st.title("🤠 Curiosidades Red Dead")
st.caption("Chatbot sobre fatos e segredos do universo Red Dead Redemption")

# Inicializa histórico se não existir
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Exibição do histórico
with st.expander("📜 Ver histórico"):
    historico = buscar_historico(st.session_state.uid)
    if historico:
        for item in historico[::-1]:
            st.markdown(f"🕒 {item['hora']}")
            st.markdown(f"**Você:** {item['pergunta']}")
            st.markdown(f"**Chatbot:** {item['resposta']}")
            st.markdown("---")
    else:
        st.info("Você ainda não possui histórico de conversas.")

# Exibição do chat no formato correto
st.subheader("💬 Chat")

for msg in st.session_state.conversation_history:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💻 **Você:** {msg['message']}")
    else:
        st.markdown(f"🤖 **Chatbot:** {msg['message']}")  

# Entrada do usuário
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Faça sua pergunta:", placeholder="Qual o segredo do cavalo lendário?", height=100)
    submit_button = st.form_submit_button("Enviar")

# Processamento da pergunta
if submit_button and user_input:
    with st.spinner("Buscando resposta..."):
        st.markdown(f"🧑‍💻 **Você:** {user_input}")

        resposta = None  

        try:
            resposta = buscar_resposta_no_pdf(user_input, conteudo_pdf)

            # Se não encontrou no PDF, usa a IA Gemini 1.5
            if not resposta:
                resposta = gerar_resposta(user_input)

            # 🔹 Garante que a resposta seja string e processa quebras de linha corretamente
            resposta = str(resposta).strip().replace("\n", "  \n") if resposta else "Erro ao obter resposta."

            # 🔹 Debug no console
            print(f"DEBUG - RESPOSTA COMPLETA:\n{resposta}")

            # 🔹 Verificar tamanho da resposta
            if len(resposta) > 1000:
                print("⚠️ Resposta muito longa, exibindo em expander!")

            # 🔹 Exibir resposta corretamente no chat
            with st.expander("🤖 Resposta do Chatbot:"):
                st.write(resposta, unsafe_allow_html=True)  

            # Salvar conversa no Firebase
            salvar_conversa(
                uid=st.session_state.uid,
                pergunta=user_input,
                resposta=resposta,
                hora=time.strftime("%d/%m/%Y %H:%M")
            )

            # Atualizar histórico
            st.session_state.conversation_history.append({"role": "user", "message": user_input})
            st.session_state.conversation_history.append({"role": "assistant", "message": resposta})

        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")
            print(f"Erro: {e}")

        # Atualizar interface
        st.rerun()