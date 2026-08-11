import streamlit as st
import streamlit.components.v1 as components
import random

# Page Configuration
st.set_page_config(
    page_title="NEET 3D | IIT Madras BS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism & Modern CSS Styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    .quote-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #6366f1;
        padding: 12px 20px;
        margin: 15px 0;
        border-radius: 0 12px 12px 0;
        font-style: italic;
    }
    .badge {
        background-color: #f59e0b;
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DYNAMIC NEET MOTIVATIONAL QUOTES
# ---------------------------------------------------------
quotes = [
    "“The future belongs to those who believe in the beauty of their dreams.” — Eleanor Roosevelt",
    "“NCERT is your bible, consistency is your key. Every chapter brings you closer to your white coat!”",
    "“Success isn't about greatness. It's about consistency. Consistent hard work leads to success.” — Dwayne Johnson",
    "“Believe you can and you're halfway there.” — Theodore Roosevelt",
    "“Future Doctor, keep pushing! Your apron is waiting for you at your dream medical college.”",
    "“Small daily improvements over time lead to stunning results.” — Robin Sharma"
]

selected_quote = random.choice(quotes)

# Header Section
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg", width=120)
with col_title:
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; font-size: 2.2rem;">🧬 NEET 3D Interactive Platform</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">
                Designed & Developed by <span class="badge">Sudhanshu Mishra</span> | <b>IIT Madras BS (Diploma Level)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Motivational Banner
st.markdown(f"""
    <div class="quote-card">
        💡 <b>NEET Daily Motivation:</b> {selected_quote}
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
subject = st.sidebar.radio("Choose Learning Module:", [
    "🧬 Biology (3D Spatial Models)",
    "🧪 Chemistry (Resonance & Structure)",
    "⚡ Physics (3D Vector Mechanics)",
    "💬 Live Peer Q&A & Discussion"
])

st.sidebar.divider()
st.sidebar.info("✨ **Tip:** Click and drag inside the 3D viewers to rotate the structures. Scroll to zoom in/out.")

# ---------------------------------------------------------
# 1. BIOLOGY MODULE
# ---------------------------------------------------------
if subject == "🧬 Biology (3D Spatial Models)":
    st.header("🧬 Class 11 & 12 NCERT Biology 3D Models")
    
    chapter = st.selectbox(
        "Select NCERT Chapter Topic:",
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
            "info": "<b>NCERT Key Concepts:</b> Double helical structure, Sugar-Phosphate backbone, Hydrogen-bonded base pairing (A=T, G≡C).",
            "labels": [
                {"text": "Sugar-Phosphate Backbone", "sel": {"chain": "A", "resi": 1}},
                {"text": "G≡C Base Pair", "sel": {"chain": "A", "resi": 6}},
                {"text": "A=T Base Pair", "sel": {"chain": "B", "resi": 19}}
            ]
        },
        "Cell: The Unit of Life (Cell Membrane & Transport)": {
            "pdb": "1afo",
            "info": "<b>NCERT Key Concepts:</b> Fluid Mosaic Model, Transmembrane helices spanning hydrophobic core.",
            "labels": [
                {"text": "Transmembrane Alpha Helix A", "sel": {"chain": "A"}},
                {"text": "Transmembrane Alpha Helix B", "sel": {"chain": "B"}}
            ]
        },
        "Human Physiology (Hemoglobin / Oxygen Transport)": {
            "pdb": "1a3n",
            "info": "<b>NCERT Key Concepts:</b> Quaternary tetramer structure (2 Alpha chains + 2 Beta chains) binding O2.",
            "labels": [
                {"text": "Alpha-1 Subunit", "sel": {"chain": "A"}},
                {"text": "Beta-1 Subunit", "sel": {"chain": "B"}},
                {"text": "Alpha-2 Subunit", "sel": {"chain": "C"}}
            ]
        },
        "Biomolecules (Insulin Structure)": {
            "pdb": "1trz",
            "info": "<b>NCERT Key Concepts:</b> Peptide hormone composed of A-chain and B-chain linked by disulfide bonds.",
            "labels": [
                {"text": "A-Chain Peptide", "sel": {"chain": "A"}},
                {"text": "B-Chain Peptide", "sel": {"chain": "B"}}
            ]
        }
    }

    selected_bio = bio_data[chapter]
    st.markdown(f"<p>{selected_bio['info']}</p>", unsafe_allow_html=True)

    label_js_lines = []
    for l in selected_bio["labels"]:
        txt = l["text"]
        sel_str = str(l["sel"]).replace("'", '"')
        label_js_lines.append(f"""
        let atoms_{txt.replace(' ', '_').replace('=', '_').replace('≡', '_')} = viewer.getAtoms({sel_str});
        if (atoms_{txt.replace(' ', '_').replace('=', '_').replace('≡', '_')}.length > 0) {{
            let atom = atoms_{txt.replace(' ', '_').replace('=', '_').replace('≡', '_')}[0];
            viewer.addLabel('{txt}', {{
                font: 'Arial',
                fontSize: 13,
                fontColor: 'white',
                backgroundColor: '#ef4444',
                backgroundOpacity: 0.9,
                borderThickness: 1,
                borderColor: 'white',
                inFront: true
            }}, {{x: atom.x, y: atom.y, z: atom.z}});
        }}
        """)
    
    js_labels = "\n".join(label_js_lines)

    html_code = f"""
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="bio_container" style="width: 100%; height: 500px; border: 2px solid #312e81; border-radius: 12px;"></div>
    <script>
        let viewer = $3Dmol.createViewer(document.getElementById('bio_container'), {{backgroundColor: '#f8fafc'}});
        $3Dmol.download('pdb:{selected_bio["pdb"]}', viewer, {{}}, function() {{
            viewer.setStyle({{}}, {{cartoon: {{color: 'spectrum'}}}});
            {js_labels}
            viewer.render();
            viewer.zoomTo();
        }});
    </script>
    """
    components.html(html_code, height=520)

# ---------------------------------------------------------
# 2. CHEMISTRY MODULE
# ---------------------------------------------------------
elif subject == "🧪 Chemistry (Resonance & Structure)":
    st.header("🧪 Chemistry: Resonance Structures & Electronic Effects")
    
    chem_choice = st.selectbox(
        "Select Molecule / Ion for Analysis:",
        ["Benzene (Aromatic Ring Delocalization)", "Aniline (+R / +M Effect)", "Phenol (Resonance Stabilization)"]
    )

    chem_data = {
        "Benzene (Aromatic Ring Delocalization)": {
            "cid": 241,
            "desc": "<b>Resonance Concept:</b> Delocalized π-electrons forming an aromatic ring above and below the planar carbon frame.",
            "label": "Delocalized Carbon Ring"
        },
        "Aniline (+R / +M Effect)": {
            "cid": 6800,
            "desc": "<b>Resonance Concept:</b> Lone pair on Nitrogen (-NH2) delocalizes into the benzene ring (+M effect).",
            "label": "-NH2 Functional Group"
        },
        "Phenol (Resonance Stabilization)": {
            "cid": 996,
            "desc": "<b>Resonance Concept:</b> Oxygen lone pair delocalization stabilizes the phenoxide ion.",
            "label": "-OH Functional Group"
        }
    }

    selected_chem = chem_data[chem_choice]
    st.markdown(selected_chem["desc"], unsafe_allow_html=True)

    html_code = f"""
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="chem_container" style="width: 100%; height: 500px; border: 2px solid #312e81; border-radius: 12px;"></div>
    <script>
        let viewer = $3Dmol.createViewer(document.getElementById('chem_container'), {{backgroundColor: '#0f172a'}});
        $3Dmol.download('cid:{selected_chem["cid"]}', viewer, {{}}, function() {{
            viewer.setStyle({{}}, {{stick: {{colorscheme: 'Jmol'}}, sphere: {{scale: 0.3}}}});
            let atoms = viewer.getAtoms({{}});
            if (atoms.length > 0) {{
                viewer.addLabel('{selected_chem["label"]}', {{
                    fontSize: 13,
                    fontColor: 'black',
                    backgroundColor: '#f59e0b',
                    backgroundOpacity: 0.95,
                    inFront: true
                }}, {{x: atoms[0].x, y: atoms[0].y, z: atoms[0].z}});
            }}
            viewer.render();
            viewer.zoomTo();
        }});
    </script>
    """
    components.html(html_code, height=520)

# ---------------------------------------------------------
# 3. PHYSICS MODULE
# ---------------------------------------------------------
elif subject == "⚡ Physics (3D Vector Mechanics)":
    st.header("⚡ Physics: 3D Vector Mechanics & Motion")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        v_x = st.slider("Vector X-Component (i)", -10.0, 10.0, 6.0)
    with c2:
        v_y = st.slider("Vector Y-Component (j)", -10.0, 10.0, 8.0)
    with c3:
        v_z = st.slider("Vector Z-Component (k)", -10.0, 10.0, 4.0)

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <div id="phys_container" style="width: 100%; height: 500px; border: 2px solid #312e81; border-radius: 12px;"></div>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a);

        const camera = new THREE.PerspectiveCamera(75, 600/500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(document.getElementById('phys_container').clientWidth, 500);
        document.getElementById('phys_container').appendChild(renderer.domElement);

        const gridHelper = new THREE.GridHelper(20, 20, 0x475569, 0x334155);
        scene.add(gridHelper);
        const axesHelper = new THREE.AxesHelper(10);
        scene.add(axesHelper);

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

# ---------------------------------------------------------
# 4. LIVE DISCUSSION BOARD
# ---------------------------------------------------------
elif subject == "💬 Live Peer Q&A & Discussion":
    st.header("💬 Live Peer Q&A & Discussion Board")
    st.write("Post your questions or study notes below to collaborate with other NEET aspirants.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"name": "Sudhanshu Mishra (Admin)", "text": "Welcome to the NEET 3D discussion room! Ask any questions regarding Biology models or Organic Chemistry resonance mechanisms here."},
            {"name": "Ananya", "text": "Can someone explain why the G≡C base pair in DNA has 3 hydrogen bonds while A=T has only 2?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message("user" if "Admin" not in msg["name"] else "assistant"):
            st.markdown(f"**{msg['name']}**: {msg['text']}")

    with st.form("chat_form", clear_on_submit=True):
        user_name = st.text_input("Your Name / Student ID:", placeholder="e.g. Rahul S.")
        user_msg = st.text_area("Your Question or Note:", placeholder="Type your discussion post here...")
        submitted = st.form_submit_button("Post Question")

        if submitted and user_msg.strip():
            display_name = user_name.strip() if user_name.strip() else "Anonymous Aspirant"
            st.session_state.messages.append({"name": display_name, "text": user_msg})
            st.rerun()