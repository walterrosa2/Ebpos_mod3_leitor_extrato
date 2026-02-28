import streamlit as st
import io
import zipfile
import pandas as pd
from core.itau_parser import parse_itau_pdf
from core.excel_writer import dataframe_to_xlsx_bytes
from core.logger import log_event, logger
from core.utils import sanitize_filename

# Page Config
st.set_page_config(
    page_title="Itaú PDF Reader - MVP",
    page_icon="🏦",
    layout="wide"
)

# Custom Styling (Itaú Orange + Light Red Text)
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FF9999;
    }
    .main {
        padding: 2rem;
    }
    /* Altera cor de textos padrões do Streamlit para vermelho claro */
    .stMarkdown, .stText, p, span, label, .stSelectbox, .stTextInput, .stMultiSelect {
        color: #FF9999 !important;
    }
    h1, h2, h3 {
        color: #FF6B00 !important;
        font-weight: 800;
    }
    .stButton>button {
        background-color: #FF6B00;
        color: white;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #E65A00;
        color: white;
    }
    .stDataFrame, .stDataEditor {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Auth Logic
def check_password():
    """Returns True if the user had the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔐 Login - Extrator Itaú")
    
    with st.container():
        st.info("Insira as credenciais para acessar o sistema.")
        user = st.text_input("Usuário", key="login_user")
        password = st.text_input("Senha", type="password", key="login_pass")
        
        if st.button("Entrar"):
            if user == "admin" and password == "admin":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
    return False

def main():
    if not check_password():
        return

    # Sidebar
    with st.sidebar:
        st.image("https://logodownload.org/wp-content/uploads/2014/05/itau-logo-7.png", width=80)
        st.title("Menu")
        if st.button("Sair"):
            st.session_state.authenticated = False
            st.rerun()
        st.divider()
        st.markdown("**Versão:** MVP 1.1")

    # App Main Area
    st.title("🏦 Leitor de Extrato Itaú")
    st.write("Extraia e edite lançamentos de arquivos PDF de forma simples e segura.")

    uploaded_files = st.file_uploader(
        "Faça o upload de um ou mais PDFs do Itaú",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        st.divider()
        excel_files = [] # List of (filename, bytes)

        # Usar session_state para manter os DataFrames editados
        if "dfs" not in st.session_state:
            st.session_state.dfs = {}

        for uploaded_file in uploaded_files:
            file_key = uploaded_file.name
            
            with st.expander(f"📄 {file_key}", expanded=True):
                try:
                    # Processa apenas se não estiver no session_state
                    if file_key not in st.session_state.dfs:
                        with st.spinner(f"Processando {file_key}..."):
                            pdf_bytes = uploaded_file.getvalue()
                            df_initial = parse_itau_pdf(pdf_bytes, file_key)
                            st.session_state.dfs[file_key] = df_initial
                            log_event("admin", file_key, None, len(df_initial), "SUCCESS")

                    current_df = st.session_state.dfs[file_key]

                    if current_df.empty:
                        st.warning("Nenhum lançamento encontrado.")
                        continue

                    st.info("💡 Você pode clicar nas células abaixo para editar os dados antes de baixar.")
                    
                    # Data Editor
                    edited_df = st.data_editor(
                        current_df,
                        use_container_width=True,
                        num_rows="dynamic",
                        key=f"editor_{file_key}"
                    )
                    
                    # Atualiza o session_state com as edições
                    st.session_state.dfs[file_key] = edited_df

                    # Generate Excel from EDITED data
                    xlsx_name = f"{sanitize_filename(file_key)}.xlsx"
                    xlsx_bytes = dataframe_to_xlsx_bytes(edited_df)
                    excel_files.append((xlsx_name, xlsx_bytes))
                    
                    # Individual Download
                    st.download_button(
                        label=f"Download {xlsx_name}",
                        data=xlsx_bytes,
                        file_name=xlsx_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"dl_{file_key}"
                    )
                            
                except Exception as e:
                    st.error(f"Erro ao processar {file_key}: {e}")
                    log_event("admin", file_key, None, 0, "ERROR", str(e))

        # Bulk Actions
        if len(excel_files) > 1:
            st.divider()
            st.subheader("📦 Ações em Lote")
            
            # Create ZIP
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for filename, file_data in excel_files:
                    zip_file.writestr(filename, file_data)
            
            st.download_button(
                label="📥 Baixar todos (editados) no formato .ZIP",
                data=zip_buffer.getvalue(),
                file_name="extratos_itau_editados.zip",
                mime="application/zip",
                use_container_width=True
            )

    # Limpar cache de DFs se novos arquivos forem carregados ou arquivos forem removidos
    if not uploaded_files:
        st.session_state.dfs = {}

if __name__ == "__main__":
    main()
