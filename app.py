import streamlit as st
import streamlit.components.v1 as components
import random

# 1. Page Configuration (Responsive Viewport)
st.set_page_config(
    page_title="NEET 3D | IIT Madras BS",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"  # Auto-collapse sidebar on mobile screens
)

# 2. Custom Mobile-Optimized CSS
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    /* Global Background */
    .stApp {
        background-color: #090d16;
        color: #f8fafc;
    }
    
    /* Responsive Header Card */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    
    @media (min-width: 768px) {
        .header-title {
            font-size: 2.2rem;
        }
        .main-header {
            padding: 24px;
        }
    }
    
    /* Responsive Quote Box */
    .quote-card {
        background: rgba(30, 41, 59, 0.7);
        border-left: 4px solid #6366f1;
        padding: 10px 14px;
        margin: 10px 0 20px 0;
        border-radius: 0 10px 10px 0;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    .badge {
        background-color: #f59e0b;
        color: #000;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    /* Touch canvas optimization */
    canvas {
        touch-action: none;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Motivational Quotes
quotes = [
    "“NCERT is your bible, consistency is your key. Every chapter brings you closer to your white coat!”",
    "“The future belongs to those who believe in the beauty of their dreams.” — Eleanor Roosevelt",
    "“Success isn't about greatness. It's about consistency.” — Dwayne Johnson",
    "“Future Doctor, keep pushing! Your apron is waiting for you at your dream medical college.”"
]
selected_quote = random.choice(quotes)

# Header Layout (Flex stack on mobile, multi-column on desktop)
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/en/6/69/IIT_Madras_Logo.svg", width=90)
with col_title:
    st.markdown("""
        <div class="main-header">
            <h1 class="header-title">🧬 NEET 3D Learning Platform</h1>
            <p style="margin:4px 0 0 0; color: #cbd5e1; font-size: 0.85rem;">
                Created by <span class="badge">Sudhanshu Mishra</span> | <b>IITM BS (Diploma Level)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Motivational Quote Box
st.markdown(f'<div class="quote-card">💡 <b>Daily Motivation:</b> {selected_quote}</div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📌 Subject Menu")
subject = st.sidebar.radio("Select Subject:", [
    "🧬 Biology (Class 11 & 12 NCERT)",
    "🧪 Chemistry (3D Resonance)",
    "⚡ Physics (3D Mechanics)",
    "💬 Live Peer Q&A Board"
])

st.sidebar.divider()

# ---------------------------------------------------------
# 1. BIOLOGY MODULE (Touch Enabled)
# ---------------------------------------------------------
if subject == "🧬 Biology (Class 11 & 12 NCERT)":
    st.subheader("🧬 Class 11 & 12 NCERT Biology 3D Explorer")

    chapter = st.selectbox(
        "Select NCERT Chapter:",
        [
            "Class 12 Ch 6: DNA Double Helix (Molecular Genetics)",
            "Class 11 Ch 8: Fluid Mosaic Cell Membrane (Cell Biology)",
            "Class 11 Ch 17: Hemoglobin & O2 Transport (Human Physiology)",
            "Class 11 Ch 9: Insulin & Protein Folding (Biomolecules)",
            "Class 12 Ch 11: EcoRI Restriction Enzyme (Biotechnology)"
        ]
    )

    render_style = st.selectbox("3D Rendering Style:", ["Cartoon Ribbon + Labels", "Surface Envelope (VDW)", "Ball & Stick Spheres"])

    bio_database = {
        "Class 12 Ch 6: DNA Double Helix (Molecular Genetics)": {
            "pdb": "1bna",
            "info": "<b>NCERT Concepts:</b> B-DNA double helix showing sugar-phosphate backbones and complementary hydrogen base pairs (A=T, G≡C).",
            "label": "G≡C Base Pair Region"
        },
        "Class 11 Ch 8: Fluid Mosaic Cell Membrane (Cell Biology)": {
            "pdb": "1afo",
            "info": "<b>NCERT Concepts:</b> Transmembrane helices spanning hydrophobic core of the lipid bilayer.",
            "label": "Transmembrane Helix"
        },
        "Class 11 Ch 17: Hemoglobin & O2 Transport (Human Physiology)": {
            "pdb": "1a3n",
            "info": "<b>NCERT Concepts:</b> Quaternary structure containing 2 Alpha and 2 Beta chains with oxygen-binding Heme groups.",
            "label": "Oxygen Binding Site"
        },
        "Class 11 Ch 9: Insulin & Protein Folding (Biomolecules)": {
            "pdb": "1trz",
            "info": "<b>NCERT Concepts:</b> Peptide hormone composed of A-chain and B-chain connected by disulfide bonds.",
            "label": "Disulfide Linkage Region"
        },
        "Class 12 Ch 11: EcoRI Restriction Enzyme (Biotechnology)": {
            "pdb": "1b88",
            "info": "<b>NCERT Concepts:</b> Restriction endonuclease cutting DNA at palindromic sequences (5'-GAATTC-3').",
            "label": "Active Cleavage Site"
        }
    }

    selected_bio = bio_database[chapter]
    st.markdown(selected_bio["info"], unsafe_allow_html=True)

    style_js = "viewer.setStyle({}, {cartoon: {color: 'spectrum'}});"
    if render_style == "Surface Envelope (VDW)":
        style_js = "viewer.setStyle({}, {cartoon: {color: 'spectrum'}}); viewer.addSurface(py3Dmol.VDW, {opacity: 0.5, color: 'white'});"
    elif render_style == "Ball & Stick Spheres":
        style_js = "viewer.setStyle({}, {stick: {}, sphere: {scale: 0.3}});"

    # Mobile-Responsive HTML Wrapper
    html_code = f"""
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="bio_canvas" style="width: 100%; height: 60vh; max-height: 480px; border: 2px solid #312e81; border-radius: 12px; background-color: #0f172a; touch-action: none;"></div>
    <script>
        let viewer = $3Dmol.createViewer(document.getElementById('bio_canvas'), {{backgroundColor: '#0f172a'}});
        $3Dmol.download('pdb:{selected_bio["pdb"]}', viewer, {{}}, function() {{
            {style_js}
            viewer.addLabel('{selected_bio["label"]}', {{
                fontSize: 12, fontColor: 'white', backgroundColor: '#dc2626', backgroundOpacity: 0.9, inFront: true
            }}, {{x: 0, y: 0, z: 0}});
            viewer.spin("y", 0.5);
            viewer.render();
            viewer.zoomTo();
        }});
    </script>
    """
    components.html(html_code, height=500)

# ---------------------------------------------------------
# 2. CHEMISTRY MODULE (Touch Enabled)
# ---------------------------------------------------------
elif subject == "🧪 Chemistry (3D Resonance)":
    st.subheader("🧪 Organic Chemistry 3D Resonance Explorer")

    chem_choice = st.selectbox(
        "Select Molecule / Ion:",
        [
            "Benzene (Aromatic Ring π-Cloud Delocalization)",
            "Aniline (+R / +M Resonance Effect)",
            "Phenol (Acidity & Phenoxide Stabilization)",
            "Glucose (Haworth Projection Ring Conformers)"
        ]
    )

    chem_database = {
        "Benzene (Aromatic Ring π-Cloud Delocalization)": {
            "cid": 241,
            "desc": "<b>Resonance Concept:</b> Complete delocalization of 6 π-electrons creating equal bond lengths (139 pm).",
            "label": "Planar Aromatic Ring"
        },
        "Aniline (+R / +M Resonance Effect)": {
            "cid": 6800,
            "desc": "<b>Resonance Concept:</b> Lone pair on Nitrogen delocalizes into the ring, activating Ortho/Para positions.",
            "label": "-NH2 Group"
        },
        "Phenol (Acidity & Phenoxide Stabilization)": {
            "cid": 996,
            "desc": "<b>Resonance Concept:</b> Oxygen lone pair delocalization stabilizes the phenoxide ion.",
            "label": "-OH Group"
        },
        "Glucose (Haworth Projection Ring Conformers)": {
            "cid": 5793,
            "desc": "<b>Biomolecules Concept:</b> Pyranose ring cyclic structure of D-glucose.",
            "label": "Pyranose Ring Core"
        }
    }

    selected_chem = chem_database[chem_choice]
    st.markdown(selected_chem["desc"], unsafe_allow_html=True)

    html_code = f"""
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="chem_canvas" style="width: 100%; height: 60vh; max-height: 480px; border: 2px solid #312e81; border-radius: 12px; background-color: #0b0f19; touch-action: none;"></div>
    <script>
        let viewer = $3Dmol.createViewer(document.getElementById('chem_canvas'), {{backgroundColor: '#0b0f19'}});
        $3Dmol.download('cid:{selected_chem["cid"]}', viewer, {{}}, function() {{
            viewer.setStyle({{}}, {{stick: {{colorscheme: 'Jmol'}}, sphere: {{scale: 0.35}}}});
            let atoms = viewer.getAtoms({{}});
            if (atoms.length > 0) {{
                viewer.addLabel('{selected_chem["label"]}', {{
                    fontSize: 12, fontColor: 'black', backgroundColor: '#f59e0b', backgroundOpacity: 0.95, inFront: true
                }}, {{x: atoms[0].x, y: atoms[0].y, z: atoms[0].z}});
            }}
            viewer.spin("y", 0.8);
            viewer.render();
            viewer.zoomTo();
        }});
    </script>
    """
    components.html(html_code, height=500)

# ---------------------------------------------------------
# 3. PHYSICS MODULE (Touch & Motion Enabled)
# ---------------------------------------------------------
elif subject == "⚡ Physics (3D Mechanics)":
    st.subheader("⚡ Physics: 3D Vector Mechanics")
    st.write("Adjust coordinate sliders below to observe real-time spatial vector resultant shifts.")

    v_x = st.slider("Vector X-Component (i)", -10.0, 10.0, 6.0)
    v_y = st.slider("Vector Y-Component (j)", -10.0, 10.0, 8.0)
    v_z = st.slider("Vector Z-Component (k)", -10.0, 10.0, 4.0)

    html_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <div id="phys_canvas" style="width: 100%; height: 50vh; max-height: 450px; border: 2px solid #312e81; border-radius: 12px; touch-action: none;"></div>
    <script>
        const container = document.getElementById('phys_canvas');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0b0f19);

        const camera = new THREE.PerspectiveCamera(75, container.clientWidth/container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{antialias: true}});
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const gridHelper = new THREE.GridHelper(20, 20, 0x6366f1, 0x1e293b);
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
            scene.rotation.y += 0.005;
            renderer.render(scene, camera);
        }}
        animate();
    </script>
    """
    components.html(html_code, height=470)

# ---------------------------------------------------------
# 4. LIVE DISCUSSION BOARD
# ---------------------------------------------------------
elif subject == "💬 Live Peer Q&A Board":
    st.subheader("💬 Live Peer Q&A & Discussion Board")

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