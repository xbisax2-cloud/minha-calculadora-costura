

# para rodar o streamlit no terminal: streamlit run teste01.py

import streamlit as st
import numpy as np
import json
import os

# Lista oficial de preços de materiais e serviços de conserto
# Nome do arquivo de texto que guardará os preços permanentemente
ARQUIVO_BANCO = "banco_precos_consertos.json"

# FUNÇÃO 1: Carrega os preços do arquivo ou cria a lista padrão se for a primeira vez
def carregar_dados_consertos():
    if os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Seus preços oficiais padrão (nascem gravados aqui)
        dados_iniciais = {
            "Zíper (Tamanhos 12, 15, 18)": 20.00,
            "Zíper (Acima do tamanho 18)": 25.00,
            "Zíper Jaqueta sem forro": 28.00,
            "Zíper Jaqueta com forro": 38.00,
            "Botão de pressão": 6.00,
            "Barra comum calça Jeans": 20.00,
            "Barra original calça Jeans": 26.00,
            "Barra de blusa, saia ou manga": 23.00,
            "Barra de vestido rodado": 26.00,
            "Ajuste para menor calça Jeans": 40.00,
            "Ajuste para menor blusa": 25.00
        }
        salvar_dados_consertos(dados_iniciais)
        return dados_iniciais

# FUNÇÃO 2: Salva qualquer alteração ou novo item permanentemente no arquivo
def salvar_dados_consertos(dados):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Inicializa o banco de dados na memória do Streamlit pegando do arquivo JSON
if "banco_consertos" not in st.session_state:
    st.session_state.banco_consertos = carregar_dados_consertos()



opcao_menu = st.sidebar.radio(
    "Navegação", 
    ["Calculadora de Tecidos", "Calculadora de Mão de Obra", "Preço Final do Conserto", "Gerenciar Preços", "Ajuda"]
)


if opcao_menu == "Calculadora de Tecidos":
    st.title("Calculadora de Tecidos")
    st.markdown("#### Aqui você pode calcular o custo do tecido com base no comprimento e largura utilizados.")


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


elif opcao_menu == "Calculadora de Mão de Obra":
    st.title("Calculadora de Mão de Obra ⏳")
    st.markdown("#### Aqui você pode calcular o custo da mão de obra usando o formato de horas e minutos (ex: 1:20 ou 0:35).")
    
    with st.form(key="meu_formulario_mao_obra", clear_on_submit=True):
        preco_hora = st.number_input("Seu valor por hora (R$):", value=16.00, step=1.00, format="%.2f")

        # Texto explicativo antes do campo
        st.write("👉 **Como preencher o tempo:** Use sempre dois-pontos (`:`) para separar as horas dos minutos.")
        
        # O campo de texto com o placeholder
        tempo_formatado = st.text_input("Tempo gasto (HORAS:MINUTOS):", placeholder="Exemplo: 1:20")
        
        # Legenda menor embaixo da caixinha com exemplos práticos rápidos
        st.caption("💡 *Exemplos: Se trabalhou 35 minutos, digite `0:35`. Se trabalhou 1 hora e meia, digite `1:30`.*")

        botao_calcular = st.form_submit_button("Calcular Mão de Obra")

    if botao_calcular:
        # 2. Verificar se o usuário digitou alguma coisa e se tem os dois-pontos ':'
        if tempo_formatado and ":" in tempo_formatado:
            try:
                # Separa o texto em duas partes: antes e depois dos dois-pontos
                partes = tempo_formatado.split(":")
                horas = int(partes[0])
                minutos = int(partes[1])
                
                # Converte tudo para minutos totais
                tempo_minutos = (horas * 60) + minutos
                
                # Faz a conta padrão do seu rascunho
                custo_total = (preco_hora / 60) * tempo_minutos
                
                # Exibe o resultado e mostra o resumo do tempo entendido pelo sistema
                st.success(f"O custo para {horas}h e {minutos}min de trabalho é: R$ {custo_total:.2f}")
                
            except ValueError:
                # Caso o usuário digite letras ou algo errado (ex: "gato:30")
                st.error("Formato inválido! Por favor, digite números no formato correto (ex: 1:20).")
        else:
            st.warning("Por favor, preencha o tempo utilizando os dois-pontos (ex: 0:40)!")

        # 1. Este bloco fica abaixo do 'if botao_calcular:', no final da aba de Mão de Obra
    st.write("---") # Cria uma linha fina horizontal para separar o cálculo das dicas
    
    # 2. Criamos a caixinha retrátil de ajuda
    with st.expander("💡 Outras dicas importantes para sua precificação (Clique para abrir)"):
        st.write("""
        Para chegar ao preço final ideal do seu serviço, lembre-se de considerar estes três fatores extras:
        
        1. **Custo do aviamento:** O preço final pode variar dependendo do custo de um novo zíper, botões ou linhas especiais utilizadas, além do preço da sua mão de obra padrão.
        2. **Dificuldade da peça:** Considere a complexidade do trabalho. Desmanchar costuras antigas, alinhavar partes delicadas ou trabalhar com tecidos muito finos ou forrados exige mais paciência e deve valorizar o seu preço.
        3. **Custos fixos:** Nunca deixe de levar em conta os custos invisíveis da sua oficina ou do seu dia a dia, como a conta de luz (máquina de costura e ferro), aluguel do espaço e a gasolina gasta para buscar materiais.
        """)


elif opcao_menu == "Preço Final do Conserto":
    st.title("Preço Final do Conserto 💰")
    st.markdown("#### Selecione todos os serviços e materiais utilizados no conserto para calcular o valor total.")
    
    # Variável que começa em zero
    valor_total_conserto = 0.0
    
    st.write("### ✂️ Itens Realizados")
    
    # A ALTERAÇÃO ESTÁ AQUI: Mudamos apenas esta linha para ler do banco JSON!
    for item, preco in st.session_state.banco_consertos.items():
        # As linhas abaixo continuam com a mesma lógica de antes:
        marcado = st.checkbox(f"{item} — R$ {preco:.2f}")
        
        if marcado:
            valor_total_conserto = valor_total_conserto + preco

    # Após passar por todos os itens, exibe o resultado
    st.write("---")
    st.metric(label="Valor Total do Orçamento", value=f"R$ {valor_total_conserto:.2f}")
    
    if valor_total_conserto > 0:
        st.success(f"**Preço sugerido para cobrar do cliente: R$ {valor_total_conserto:.2f}**")


elif opcao_menu == "Gerenciar Preços":
    st.title("Gerenciar Tabela de Preços ⚙️")
    st.markdown("#### Adicione novos tipos de consertos ou atualize o preço de itens já existentes na sua tabela.")
    
    # === BLOCO 1: FORMULÁRIO DE CADASTRO ===
    # Este bloco cria a caixinha cinza com os campos de texto e número
    with st.form(key="form_cadastro_preco", clear_on_submit=True):
        st.write("### ➕ Cadastrar / Atualizar Item")
        novo_item = st.text_input("Nome do serviço ou material (Ex: Zíper Invisível, Barra Simples):")
        novo_preco = st.number_input("Preço sugerido cobrado (R$):", value=None, step=1.00, format="%.2f")
        botao_salvar = st.form_submit_button("Salvar na Tabela")
        
    # Esta condição trata o salvamento (Alinhada perfeitamente fora do formulário)
    if botao_salvar:
        if novo_item.strip() != "":
            st.session_state.banco_consertos[novo_item.strip()] = novo_preco
            salvar_dados_consertos(st.session_state.banco_consertos)
            st.success(f"**Sucesso! '{novo_item}' foi gravado com o valor de R$ {novo_preco:.2f}!**")
            st.rerun()
        else:
            st.warning("Por favor, digite o nome do serviço para poder salvar!")

    # === LINHA DIVISÓRIA (Fora de qualquer bloco anterior) ===
    st.write("---")

    # === BLOCO 2: REMOVER ITEM (Fora de qualquer bloco anterior) ===
    st.write("### 🗑️ Remover Item da Tabela")
    
    # Buscamos as chaves reais do banco de dados
    itens_reais = list(st.session_state.banco_consertos.keys())
    
    if itens_reais:
        # Prepara a lista começando com a instrução limpa
        lista_para_selecao = ["-- Escolha um item para excluir --"] + itens_reais
        item_para_remover = st.selectbox("Selecione o item que deseja excluir:", lista_para_selecao)
        
        # Só mostra os botões se o usuário escolher um item de fato
        if item_para_remover != "-- Escolha um item para excluir --":
            
            if st.button("❌ Solicitar Exclusão"):
                st.session_state.confirmar_deletar = item_para_remover

            # Caixa amarela de confirmação de segurança
            if "confirmar_deletar" in st.session_state and st.session_state.confirmar_deletar == item_para_remover:
                st.warning(f"⚠️ **Atenção:** Você tem certeza que deseja apagar '{item_para_remover}' permanentemente?")
                
                col_sim, col_nao = st.columns(2)
                
                with col_sim:
                    if st.button("👍 Sim, tenho certeza!", type="primary"):
                        del st.session_state.banco_consertos[item_para_remover]
                        salvar_dados_consertos(st.session_state.banco_consertos)
                        
                        if "confirmar_deletar" in st.session_state:
                            del st.session_state.confirmar_deletar
                            
                        st.success(f"'{item_para_remover}' removido!")
                        st.rerun()
                        
                with col_nao:
                    if st.button("👎 Não, cancelar"):
                        if "confirmar_deletar" in st.session_state:
                            del st.session_state.confirmar_deletar
                        st.rerun()
    else:
        st.info("Sua tabela está vazia. Não há itens para remover.")



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

