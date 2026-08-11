import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(page_title="NEET 3D | IIT Madras BS", layout="wide")

# Custom Header with IIT Madras Logo & Student Details
col1, col2 = st.columns([1, 5])
with col1:
    # Official IIT Madras Logo
    st.image("https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg", width=110)
with col2:
    st.title("NEET 3D Interactive Learning Platform")
    st.markdown("**Created by:** Sudhanshu Mishra | *IITM BS (Diploma Level)*")

st.divider()

# Subject Selector Sidebar
subject = st.sidebar.radio("Select Subject", ["Biology (Chapter-Wise)", "Chemistry (Resonance & Labeling)", "Physics (3D Mechanics)"])

# ---------------------------------------------------------
# 1. BIOLOGY MODULE (Chapter-Wise 3D with Spatial Labels)
# ---------------------------------------------------------
if subject == "Biology (Chapter-Wise)":
    st.header("🧬 Biology: Chapter-Wise 3D Models with Spatial Labels")
    
    chapter = st.selectbox(
        "Select NCERT Chapter:",
        [
            "Molecular Basis of Inheritance (DNA Double Helix)",
            "Cell: The Unit of Life (Cell Membrane & Transport)",
            "Human Physiology (Hemoglobin / Oxygen Transport)",
            "Biomolecules (Insulin Structure)"
        ]
    )

    bio_data = {
        "Molecular Basis of Inheritance (DNA Double Helix)": {
            "pdb": "1bna",
            "info": "**Key Features Labeled:** Sugar-Phosphate Backbone, Hydrogen-bonded Nitrogenous Base Pairs (A=T, G≡C), Major and Minor Grooves.",
            "labels": [
                {"text": "Sugar-Phosphate Backbone", "pos": [0, 10, 0]},
                {"text": "Hydrogen-bonded Base Pairs", "pos": [0, 0, 0]},
                {"text": "Major Groove", "pos": [0, -10, 0]}
            ]
        },
        "Cell: The Unit of Life (Cell Membrane & Transport)": {
            "pdb": "1afo",
            "info": "**Key Features Labeled:** Glycophorin A Transmembrane Helices, Lipid Bilayer Boundary.",
            "labels": [
                {"text": "Transmembrane Alpha Helix", "pos": [0, 0, 0]},
                {"text": "Hydrophobic Core Region", "pos": [0, 8, 0]}
            ]
        },
        "Human Physiology (Hemoglobin / Oxygen Transport)": {
            "pdb": "1a3n",
            "info": "**Key Features Labeled:** Quaternary Tetramer (2 Alpha + 2 Beta Chains), Central Heme Groups for Oxygen Binding.",
            "labels": [
                {"text": "Alpha Subunit", "pos": [15, 15, 15]},
                {"text": "Beta Subunit", "pos": [-15, -15, -15]},
                {"text": "Heme Binding Site", "pos": [0, 0, 0]}
            ]
        },
        "Biomolecules (Insulin Structure)": {
            "pdb": "1trz",
            "info": "**Key Features Labeled:** A-Chain, B-Chain, Interchain Disulfide Bonds.",
            "labels": [
                {"text": "A-Chain Peptide", "pos": [10, 5, 0]},
                {"text": "B-Chain Peptide", "pos": [-10, -5, 0]},
                {"text": "Disulfide Linkage", "pos": [0, 0, 0]}
            ]
        }
    }

    selected_bio = bio_data[chapter]
    st.markdown(selected_bio["info"])

    # Convert label data into JS string
    label_js = ""
    for l in selected_bio["labels"]:
        txt = l["text"]
        x, y, z = l["pos"]
        label_js += f"viewer.addLabel('{txt}', {{fontColor: 'white', backgroundColor: 'black', fontSize: 12}}, {{x: {x}, y: {y}, z: {z}}});\n"

    # 3Dmol.js Renderer
    html_code = f"""
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="bio_container" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 8px;"></div>
    <script>
        let viewer = $3Dmol.createViewer(document.getElementById('bio_container'), {{backgroundColor: '#f8f9fa'}});
        $3Dmol.download('pdb:{selected_bio["pdb"]}', viewer, {{}}, function() {{
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum'}}}});
            {label_js}
            viewer.render();
            viewer.zoomTo();
        }});
    </script>
    """
    components.html(html_code, height=520)

# ---------------------------------------------------------
# 2. CHEMISTRY MODULE (Resonance Structures & Annotation)
# ---------------------------------------------------------
elif subject == "Chemistry (Resonance & Labeling)":
    st.header("🧪 Chemistry: Resonance Structures & Electronic Delocalization")
    
    chem_choice = st.selectbox(
        "Select Molecule / Ion for Resonance Analysis:",
        ["Benzene (Aromatic Ring Delocalization)", "Aniline (+R / +M Effect)", "Phenol (Resonance Stabilization)"]
    )

    chem_data = {
        "Benzene (Aromatic Ring Delocalization)": {
            "cid": 241,
            "desc": "**Resonance Concept:** Equal C-C bond lengths due to delocalized π-electrons forming a continuous ring above and below the planar ring.",
            "labels": [
                {"text": "Delocalized π-Cloud Carbon Ring", "pos": [0, 0, 0]},
                {"text": "sp2 Hybridized Carbon", "pos": [1.4, 0, 0]}
            ]
        },
        "Aniline (+R / +M Effect)": {
            "cid": 6800,
            "desc": "**Resonance Concept:** Lone pair on nitrogen (-NH2) delocalizes into the benzene ring, increasing electron density at Ortho and Para positions.",
            "labels": [
                {"text": "-NH2 Donor Group (Lone Pair)", "pos": [0, 2.2, 0]},
                {"text": "Ortho Position (High e- density)", "pos": [1.2, 0.7, 0]},
                {"text": "Para Position (High e- density)", "pos": [0, -2.2, 0]}
            ]
        },
        "Phenol (Resonance Stabilization)": {
            "cid": 996,
            "desc": "**Resonance Concept:** Oxygen lone pair delocalization stabilizes the phenoxide ion, making phenol acidic in nature.",
            "labels": [
                {"text": "-OH Group", "pos": [0, 2.1, 0]},
                {"text": "Aromatic Ring System", "pos": [0, -0.5, 0]}
            ]
        }
    }

    selected_chem = chem_data[chem_choice]
    st.markdown(selected_chem["desc"])

    chem_label_js = ""
    for l in selected_chem["labels"]:
        txt = l["text"]
        x, y, z = l["pos"]
        chem_label_js += f"viewer.addLabel('{txt}', {{fontColor: 'yellow', backgroundColor: '#333333', fontSize: 11}}, {{x: {x}, y: {y}, z: {z}}});\n"

    html_code = f"""
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="chem_container" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 8px;"></div>
    <script>
        let viewer = $3Dmol.createViewer(document.getElementById('chem_container'), {{backgroundColor: '#1e1e1e'}});
        $3Dmol.download('cid:{selected_chem["cid"]}', viewer, {{}}, function() {{
            viewer.setStyle({{}}, {{stick: {{colorscheme: 'Jmol'}}, sphere: {{scale: 0.25}}}});
            {chem_label_js}
            viewer.render();
            viewer.zoomTo();
        }});
    </script>
    """
    components.html(html_code, height=520)

# ---------------------------------------------------------
# 3. PHYSICS MODULE (3D Mechanics Vector Motion)
# ---------------------------------------------------------
elif subject == "Physics (3D Mechanics)":
    st.header("⚡ Physics: 3D Vector Motions & Mechanics")
    st.write("Adjust magnitude components to visualize the resultant 3D force/velocity vector in spatial coordinates.")

    c1, c2, c3 = st.columns(3)
    with c1:
        v_x = st.slider("Vector X-Component (i)", -10.0, 10.0, 6.0)
    with c2:
        v_y = st.slider("Vector Y-Component (j)", -10.0, 10.0, 8.0)
    with c3:
        v_z = st.slider("Vector Z-Component (k)", -10.0, 10.0, 4.0)

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <div id="phys_container" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 8px;"></div>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);

        const camera = new THREE.PerspectiveCamera(75, 600/500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(document.getElementById('phys_container').clientWidth, 500);
        document.getElementById('phys_container').appendChild(renderer.domElement);

        // Grid and Axes
        const gridHelper = new THREE.GridHelper(20, 20, 0x475569, 0x334155);
        scene.add(gridHelper);
        const axesHelper = new THREE.AxesHelper(10);
        scene.add(axesHelper);

        // Vector Arrow
        const dir = new THREE.Vector3({v_x}, {v_y}, {v_z}).normalize();
        const origin = new THREE.Vector3(0, 0, 0);
        const length = Math.sqrt({v_x}*{v_x} + {v_y}*{v_y} + {v_z}*{v_z});
        const arrowHelper = new THREE.ArrowHelper(dir, origin, length, 0x38bdf8, 1.5, 0.8);
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
    components.html(html_code, height=520)