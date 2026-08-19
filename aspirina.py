from rdkit import Chem
from rdkit.Chem import AllChem
import streamlit as st
import py3Dmol
from stmol import showmol

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Visualizador 3D - AAS", page_icon="💊", layout="centered"
)

st.title("💊 Visualizador 3D de Moléculas")
st.markdown(
    "<h1 style='text-align: center;'>by Hebert Felix</h1>",
    unsafe_allow_html=True
)
st.markdown(
    " Analise do **Ácido Acetilsalicílico (AAS)**."
)


# Função para gerar o bloco SDF 3D a partir do SMILES do AAS
@st.cache_data
def gerar_conformero_aas():
  # SMILES do Ácido Acetilsalicílico (AAS)
  smiles_aas = "CC(=O)OC1=CC=CC=C1C(=O)O"

  # 1. Cria a molécula no RDKit
  mol = Chem.MolFromSmiles(smiles_aas)
  # 2. Adiciona os hidrogênios explícitos (essenciais para 3D)
  mol = Chem.AddHs(mol)
  # 3. Gera coordenadas 3D usando o algoritmo ETKDG
  AllChem.EmbedMolecule(mol, AllChem.ETKDG())
  # 4. Otimiza a geometria molecular (campo de força MMFF)
  AllChem.MMFFOptimizeMolecule(mol)

  # Retorna a molécula em formato de texto SDF
  return Chem.MolToMolBlock(mol)


# Carrega o bloco tridimensional
mol_block = gerar_conformero_aas()

# Controles interativos na Barra Lateral
st.sidebar.header("⚙️ Controles de Visualização")
estilo_visual = st.sidebar.selectbox(
    "Estilo de Exibição", ["stick", "sphere", "line", "cartoon"]
)
cor_atomo = st.sidebar.selectbox(
    "Esquema de Cores", ["element", "spectrum", "chain"]
)

# Renderização 3D com py3Dmol / stmol
st.subheader("Visualização Interativa: AAS")
st.info(
    "Dica: Você pode clicar e arrastar com o mouse para girar a molécula, e"
    " usar o scroll para dar zoom."
)

# Inicializa o visualizador 3D
view = py3Dmol.view(width=700, height=450)
view.addModel(mol_block, "sdf")

# Aplica o estilo escolhido pelo usuário na barra lateral
estilo_dict = {estilo_visual: {"colorscheme": cor_atomo}}
view.setStyle(estilo_dict)

view.zoomTo()

# Exibe o componente dentro do Streamlit
showmol(view, height=450, width=700)

# Informações adicionais de apoio
with st.expander("🔍 Sobre este fluxo computacional"):
  st.markdown("""
    * **SMILES (`CC(=O)OC1=CC=CC=C1C(=O)O`)**: A string linear que define a conectividade química do AAS.
    * **RDKit**: Converteu a string 2D em um arranjo espacial 3D otimizado energeticamente.
    * **stmol**: Traduziu os dados espaciais para uma interface web interativa em WebGL.
    """)