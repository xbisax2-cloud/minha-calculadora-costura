

# para rodar o streamlit no terminal: streamlit run teste01.py

import streamlit as st
import numpy as np

opcao_menu = st.sidebar.radio("Navegação", ["Calculadora de Tecidos", "Ajuda"])

if opcao_menu == "Calculadora de Tecidos":
    st.title("Calculadora de Tecidos")
    
    # 1. Criamos um formulário que se limpa sozinho após o envio
    with st.form(key="meu_formulario_tecido", clear_on_submit=True):
        
        # Preço e rolo continuam com valores padrões para poupar digitação
        preco_metro = st.number_input("Preço do metro (R$):", value=30.00, step=1.00, format="%.2f")
        largura_rolo = st.number_input("Largura padrão do rolo (m):", value=1.40, step=0.05, format="%.2f")

        # 2. Mudamos o 'value' para None para eles nascerem totalmente vazios!
        comprimento_usado = st.number_input("Comprimento utilizado (m):", value=None, step=0.01, format="%.2f")
        largura_usada = st.number_input("Largura utilizada (m):", value=None, step=0.01, format="%.2f")

        # 3. O botão do formulário precisa ser obrigatoriamente um 'st.form_submit_button'
        botao_calcular = st.form_submit_button("Calcular")

    # 4. A conta e o resultado ficam DO LADO DE FORA do 'with st.form'
    # Assim, o app calcula primeiro e limpa os campos para a próxima rodada!
    if botao_calcular:
        # Uma segurança extra: conferir se o usuário preencheu os campos vazios
        if comprimento_usado is not None and largura_usada is not None:
            custo_total = ((comprimento_usado * largura_usada) / largura_rolo) * preco_metro
            st.success(f"O tecido utilizado custa: R$ {custo_total:.2f}")
        else:
            st.warning("Por favor, preencha o comprimento e a largura utilizados!")


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


