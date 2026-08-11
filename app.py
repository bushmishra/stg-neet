import streamlit as st
import py3Dmol
from stmol import showmol
from rdkit import Chem
from rdkit.Chem import AllChem

# Page Configuration
st.set_page_config(page_title="NEET 3D Visualizer", layout="wide")

st.title("NEET 3D Learning Platform")
st.caption("Interactive 3D Visualizations for Physics, Chemistry, and Biology")

# Subject Selector
subject = st.sidebar.selectbox("Select Subject", ["Chemistry", "Biology", "Physics"])

# ---------------------------------------------------------
# 1. CHEMISTRY MODULE
# ---------------------------------------------------------
if subject == "Chemistry":
    st.header("Chemistry: 3D Molecular Visualizer")
    molecule_choice = st.selectbox(
        "Choose a Molecule:",
        ["Aspirin", "Ethanol", "Benzene", "Glucose"]
    )
    smiles_dict = {
        "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O"
    }
    user_smiles = smiles_dict[molecule_choice]

    if st.button("Render 3D Molecule"):
        mol = Chem.MolFromSmiles(user_smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        mblock = Chem.MolToMolBlock(mol)

        view = py3Dmol.view(width=600, height=400)
        view.addModel(mblock, 'mol')
        view.setStyle({'stick': {}, 'sphere': {'scale': 0.25}})
        view.zoomTo()
        showmol(view, height=400, width=600)

# ---------------------------------------------------------
# 2. BIOLOGY MODULE
# ---------------------------------------------------------
elif subject == "Biology":
    st.header("Biology: 3D Structure Viewer")
    bio_choice = st.selectbox(
        "Select Biological Structure:",
        ["DNA Double Helix (1BNA)", "Hemoglobin (1A3N)", "Insulin (1TRZ)"]
    )
    pdb_ids = {
        "DNA Double Helix (1BNA)": "1bna",
        "Hemoglobin (1A3N)": "1a3n",
        "Insulin (1TRZ)": "1trz"
    }
    selected_pdb = pdb_ids[bio_choice]

    if st.button("Fetch and Render 3D Structure"):
        view = py3Dmol.view(query=f'pdb:{selected_pdb}', width=600, height=400)
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.addSurface(py3Dmol.VDW, {'opacity': 0.4, 'color': 'white'})
        view.zoomTo()
        showmol(view, height=400, width=600)

# ---------------------------------------------------------
# 3. PHYSICS MODULE
# ---------------------------------------------------------
elif subject == "Physics":
    st.header("Physics: Interactive 3D Vectors")
    v_x = st.slider("Velocity X component", -10.0, 10.0, 5.0)
    v_y = st.slider("Velocity Y component", -10.0, 10.0, 5.0)
    v_z = st.slider("Velocity Z component", -10.0, 10.0, 2.0)

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <div id="container" style="width: 100%; height: 400px;"></div>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf0f2f6);
        const camera = new THREE.PerspectiveCamera(75, 600/400, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(600, 400);
        document.getElementById('container').appendChild(renderer.domElement);

        const axesHelper = new THREE.AxesHelper(10);
        scene.add(axesHelper);

        const dir = new THREE.Vector3({v_x}, {v_y}, {v_z}).normalize();
        const origin = new THREE.Vector3(0, 0, 0);
        const length = Math.sqrt({v_x}*{v_x} + {v_y}*{v_y} + {v_z}*{v_z});
        const arrowHelper = new THREE.ArrowHelper(dir, origin, length, 0xff0000);
        scene.add(arrowHelper);

        camera.position.set(12, 12, 12);
        camera.lookAt(0, 0, 0);

        function animate() {{
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """
    st.components.v1.html(html_code, height=420)