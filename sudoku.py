import streamlit as st
import time
import random
import copy
import json
import os
from streamlit.components.v1 import html

# ------------------------
# Lógica do Sudoku
# ------------------------

def pode_colocar(tab, r, c, num):
    for i in range(9):
        if tab[r][i] == num or tab[i][c] == num:
            return False
    br = (r // 3) * 3
    bc = (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if tab[br + i][bc + j] == num:
                return False
    return True

def preencher_tabuleiro(tab):
    for i in range(9):
        for j in range(9):
            if tab[i][j] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for n in nums:
                    if pode_colocar(tab, i, j, n):
                        tab[i][j] = n
                        if preencher_tabuleiro(tab):
                            return True
                        tab[i][j] = 0
                return False
    return True

def gerar_sudoku(remover=40):
    tab = [[0]*9 for _ in range(9)]
    preencher_tabuleiro(tab)
    solucao = copy.deepcopy(tab)
    removidos = 0
    while removidos < remover:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if tab[i][j] != 0:
            tab[i][j] = 0
            removidos += 1
    return tab, solucao

# ------------------------
# UI (Streamlit)
# ------------------------

st.set_page_config(page_title="Sudoku", page_icon="🧩", layout="wide")

# Estilos: título pink e blocos 3x3 com alto contraste
st.markdown("""
<style>
/* Fundo claro e texto escuro para máximo contraste */
html, body, [data-testid="stAppViewContainer"] { background: #ffffff; color: #222; }
h1.sudoku-title { text-align:center; font-size:60px; color: #ff1493; font-weight: 800; margin: 6px 0 18px; }

/* Cores alternadas dos blocos 3x3 */
.block-even { background:#FFC9DE; padding:10px; border-radius:8px; }
.block-odd  { background:#C8FACC; padding:10px; border-radius:8px; }

/* Aparência dos selects para ficarem mais legíveis */
.sudoku-cell select { width:100% !important; }
.sudoku-cell { padding:2px; }

/* Linha separadora suave */
.rule { height:1px; background:#eee; margin:12px 0 16px; }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown("<h1 class='sudoku-title'>🧩 Sudoku</h1>", unsafe_allow_html=True)

# Instruções SEM dropdown, com fonte maior
st.markdown("""
<h3 style='font-size:22px; margin: 6px 0 6px;'>ℹ️ <strong>Como jogar?</strong></h3>
<ul style='font-size:18px; margin-top: 0;'>
  <li>Complete o tabuleiro 9×9 com números de 1 a 9.</li>
  <li>Cada <strong>linha</strong>, <strong>coluna</strong> e cada <strong>bloco 3×3</strong> deve conter todos os números sem repetir.</li>
  <li>Use os menus das casas vazias para escolher o número.</li>
  <li>Clique em <strong>✅ Verificar</strong> para validar; <strong>🔁 Novo jogo</strong> reinicia.</li>
</ul>
<div class='rule'></div>
""", unsafe_allow_html=True)

# Controles
jogador = st.text_input("Digite seu nome ou apelido para jogar:")
dificuldade = st.selectbox("Escolha a dificuldade:", ["Fácil", "Médio", "Difícil"])
remover = {"Fácil": 30, "Médio": 45, "Difícil": 60}[dificuldade]

# Estado do jogo
if jogador and "jogo" not in st.session_state:
    tab, sol = gerar_sudoku(remover)
    st.session_state.jogo = {
        "inicio": time.time(),
        "tabuleiro": tab,
        "solucao": sol,
        "tentativas": 0,
        "preenchido": {},    # {(i, j): valor_escolhido}
    }

jogo = st.session_state.get("jogo", None)

if not jogo:
    st.info("Preencha seu nome ou apelido e tecle enter para iniciar o jogo.")
    st.stop()

st.subheader(f"Jogador: {jogador} | Dificuldade: {dificuldade}")

# Desenho do tabuleiro
corretas = 0
total_vazias = sum(1 for i in range(9) for j in range(9) if jogo["tabuleiro"][i][j] == 0)

for i in range(9):
    cols = st.columns(9)
    for j in range(9):
        chave = f"cell-{i}-{j}"
        valor_fixo = jogo["tabuleiro"][i][j]
        bloco_class = "block-even" if ((i//3 + j//3) % 2 == 0) else "block-odd"
        with cols[j]:
            st.markdown(f"<div class='{bloco_class} sudoku-cell'>", unsafe_allow_html=True)
            if valor_fixo != 0:
                # célula fixa (pista)
                st.number_input("", value=valor_fixo, min_value=1, max_value=9, disabled=True, label_visibility="collapsed", key=chave)
            else:
                # célula editável: select com "" (vazio) e 1..9 (evita '1' automático)
                opcoes = [""] + list(range(1, 10))
                escolha = st.selectbox("", options=opcoes, index=0, key=chave, label_visibility="collapsed")
                if escolha != "":
                    jogo["preenchido"][(i, j)] = int(escolha)
                    if int(escolha) == jogo["solucao"][i][j]:
                        corretas += 1
            st.markdown("</div>", unsafe_allow_html=True)

# Progresso
if total_vazias == 0:
    st.info("Nada para preencher nesta geração. Clique em “Novo jogo”.")
else:
    st.progress(corretas / total_vazias)
    st.info(f"Corretas: {corretas}/{total_vazias}")

# Ações (sem Dica)
col1, col2 = st.columns(2)

if col1.button("✅ Verificar"):
    jogo["tentativas"] += 1
    if corretas == total_vazias and total_vazias > 0:
        tempo = int(time.time() - jogo["inicio"])
        st.success(f"🎉 Parabéns {jogador}, você concluiu em {tempo}s!")
        # salva no ranking
        ranking_path = "ranking_sudoku.json"
        if os.path.exists(ranking_path):
            with open(ranking_path, "r", encoding="utf-8") as f:
                ranking = json.load(f)
        else:
            ranking = []
        ranking.append({"nome": jogador, "tempo": tempo, "tentativas": jogo["tentativas"]})
        ranking.sort(key=lambda x: (x["tempo"], x["tentativas"]))
        with open(ranking_path, "w", encoding="utf-8") as f:
            json.dump(ranking, f, indent=2, ensure_ascii=False)
    else:
        st.warning("❌ Ainda há erros ou células em branco. Continue tentando!")

if col2.button("🔁 Novo jogo"):
    del st.session_state["jogo"]
    st.experimental_rerun()

# Ranking (sem “dicas”)
st.subheader("🏆 Ranking Local (salvo em arquivo)")
if os.path.exists("ranking_sudoku.json"):
    with open("ranking_sudoku.json", "r", encoding="utf-8") as f:
        ranking = json.load(f)
    for k, r in enumerate(ranking[:10], start=1):
        st.markdown(f"{k}. {r['nome']} — ⏱️ {r['tempo']}s | Tentativas: {r['tentativas']}")