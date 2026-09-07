
# para rodar o streamlit no terminal: streamlit run teste01.py

import streamlit as st
import numpy as np

opcao_menu = st.sidebar.radio("Navegação", ["Calculadora de Tecidos", "Ajuda"])

if opcao_menu == "Calculadora de Tecidos":
    st.title("Calculadora de Tecidos")
    
    # O valor 30.00 fica gravado como padrão, mas é totalmente editável pelo usuário
    preco_metro = st.number_input("Preço do metro (R$):", value=30.00, step=1.00, format="%.2f")
    largura_rolo = st.number_input("Largura padrão do rolo (m):", value=1.40, step=0.05, format="%.2f")

    # O formato "%.2f" força a exibição de 2 casas decimais usando a vírgula do seu sistema
    comprimento_usado = st.number_input("Comprimento utilizado (m):", value=0.00, step=0.01, format="%.2f")
    largura_usada = st.number_input("Largura utilizada (m):", value=0.00, step=0.01, format="%.2f")

    # O botão físico na tela
    if st.button("Calcular"):
        # Tudo que estiver com esse espaço (indentação) para a direita
        # só vai acontecer quando o botão for clicado!
        custo_total = ((comprimento_usado * largura_usada) / largura_rolo) * preco_metro
        st.success(f"O tecido utilizado custa: R$ {custo_total:.2f}")

elif opcao_menu == "Ajuda":
    st.title("Central de Ajuda")
    st.subheader("Como calculamos o custo do tecido?")
    # Texto simples, direto e formatado
    st.write("""
    Nossa calculadora descobre o custo exato de um pedaço menor (retalho) recortado de um rolo de tecido maior. 
    A lógica funciona em 3 passos simples:
    
    1. **Calculamos a área usada:** Multiplicamos o comprimento pela largura do seu pedaço para saber quantos metros quadrados ele ocupa.
    2. **Calculamos a proporção:** Dividimos o seu pedaço pelo tamanho total da largura do rolo padrão para descobrir a fração exata de tecido consumida.
    3. **Descobrimos o valor:** Multiplicamos essa fração pelo preço do metro cobrado na loja para chegar ao custo final de centavos.
   """)

