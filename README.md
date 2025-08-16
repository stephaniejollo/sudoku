# 🧩 Sudoku com Streamlit — Versão Estilizada

▶️ Demo ao vivo

https://sudoku-stephaniejollo.streamlit.app

Sudoku 9×9 feito em Python + Streamlit, com visual moderno e foco na experiência do jogador.

## ✨ Funcionalidades

- Geração automática de tabuleiros válidos (backtracking)
- **Três níveis de dificuldade**: Fácil, Médio, Difícil
- **Blocos 3×3 com cores de alto contraste** (alternadas) para leitura mais fácil
- **Título “Sudoku” em rosa pink** com grande destaque
- **“Como jogar?” sempre visível** e com **fonte maior**
- Células editáveis com **select** (vazio, 1–9) para evitar preenchimento acidental
- **Verificação da solução**, **barra de progresso** e **contagem de tentativas**
- **Ranking local** salvo em `ranking_sudoku.json`
- Código limpo e **sem a funcionalidade de dica**

> Observação: recursos como “dica automática” e “solver” não fazem parte desta versão por decisão de design. Se quiser, podemos reintroduzi-los futuramente.

## 🧰 Requisitos

- **Python 3.10+**
- **Streamlit 1.30+**

Instale diretamente (ou via `requirements.txt`):
```bash
pip install streamlit>=1.30
```

## ▶️ Como rodar

Dentro da pasta do projeto, execute:
```bash
streamlit run sudoku.py
```
O app abre em `http://localhost:8501`.

## 📁 Estrutura sugerida

```
sudoku/
├── sudoku.py               # app principal (Streamlit)
├── README.md               # este arquivo
├── requirements.txt        # dependências (opcional)
└── ranking_sudoku.json     # gerado automaticamente (ranking local)
```

## 🖼️ Screenshot
<img width="1361" height="599" alt="image" src="https://github.com/user-attachments/assets/c2415f22-8ddf-4044-a0b6-4cefee29921c" />

```

## 🆘 Dicas de solução de problemas (Windows)

- **“streamlit” não é reconhecido**  
  Use: `python -m pip install --upgrade pip` e depois `python -m pip install streamlit`

- **“File does not exist” ao rodar**  
  Confirme que está na pasta certa:  
  `cd C:\Users\SeuUsuario\...\sudoku`  
  e então: `streamlit run sudoku.py`

## 📝 Licença

MIT — use, modifique e compartilhe livremente.
