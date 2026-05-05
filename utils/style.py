ANIMATION_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── CANVAS ── */
#bio-canvas {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
    opacity: 0.55;
}
.stApp > div { position: relative; z-index: 1; }

/* ── HEADER ── */
.patelki-header {
    background: linear-gradient(135deg, #050d1a 0%, #0a1628 40%, #0d1f3c 100%);
    padding: 1.1rem 2rem;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid rgba(59,130,246,.25);
    position: relative; z-index: 10;
    box-shadow: 0 4px 32px rgba(0,0,0,.6), 0 0 60px rgba(59,130,246,.08);
}
.patelki-header::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,.6), rgba(99,102,241,.4), transparent);
}
.patelki-logo {
    width: 52px; height: 52px; border-radius: 50%;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6, #60a5fa);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 700; color: #fff;
    border: 2px solid rgba(96,165,250,.4);
    box-shadow: 0 0 20px rgba(59,130,246,.5), 0 0 40px rgba(59,130,246,.2);
    flex-shrink: 0; position: relative;
    animation: pulse-logo 3s ease-in-out infinite;
}
@keyframes pulse-logo {
    0%, 100% { box-shadow: 0 0 20px rgba(59,130,246,.5), 0 0 40px rgba(59,130,246,.2); }
    50% { box-shadow: 0 0 30px rgba(59,130,246,.8), 0 0 60px rgba(59,130,246,.35); }
}
.patelki-title h1 { font-size: 17px; font-weight: 700; color: #fff; margin: 0; letter-spacing: .3px; }
.patelki-title p  { font-size: 11px; color: #93C5FD; margin: 3px 0 0; letter-spacing: .4px; }

/* ── STAT CARDS ── */
.stat-card {
    background: linear-gradient(135deg, rgba(10,22,40,.95) 0%, rgba(15,30,55,.9) 100%);
    border: 1px solid rgba(59,130,246,.15);
    border-radius: 14px; padding: 1.1rem 1.3rem;
    backdrop-filter: blur(20px);
    transition: transform .25s, box-shadow .25s, border-color .25s;
    position: relative; overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,.7), rgba(99,102,241,.5), transparent);
}
.stat-card::after {
    content: '';
    position: absolute; bottom: -40px; right: -40px;
    width: 100px; height: 100px; border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,.08), transparent);
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(59,130,246,.2), 0 0 20px rgba(59,130,246,.1);
    border-color: rgba(59,130,246,.35);
}
.stat-lbl {
    font-size: 10px; color: #475569;
    text-transform: uppercase; letter-spacing: .8px; margin-bottom: 8px;
    font-weight: 600;
}
.stat-val { font-size: 30px; font-weight: 700; color: #F1F5F9; line-height: 1; }
.stat-sub { font-size: 11px; color: #334155; margin-top: 5px; }

/* ── GLASS PANEL ── */
.glass-panel {
    background: rgba(10,22,40,.85);
    border: 1px solid rgba(59,130,246,.12);
    border-radius: 14px; overflow: hidden;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 32px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.04);
}

/* ── STREAMLIT WIDGETS ── */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stDateInput"] input,
div[data-testid="stNumberInput"] input {
    background: rgba(5,15,30,.9) !important;
    border: 1px solid rgba(59,130,246,.2) !important;
    border-radius: 8px !important; color: #F1F5F9 !important;
    transition: border-color .2s, box-shadow .2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(59,130,246,.6) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.12), 0 0 20px rgba(59,130,246,.08) !important;
}
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    border: none !important; color: #fff !important;
    font-weight: 600 !important; border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(37,99,235,.4) !important;
    transition: transform .15s, box-shadow .15s !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(37,99,235,.5) !important;
}
div[data-testid="stButton"] button {
    border-radius: 8px !important;
    transition: transform .15s !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #60A5FA !important;
    border-bottom-color: #3B82F6 !important;
}

/* ── DATAFRAME ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px; overflow: hidden;
    border: 1px solid rgba(59,130,246,.1) !important;
}
div[data-testid="stDataFrame"] iframe {
    border-radius: 10px;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(5,15,30,.5); }
::-webkit-scrollbar-thumb { background: rgba(59,130,246,.4); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(59,130,246,.7); }

/* ── ALERT ── */
div[data-testid="stAlert"] { border-radius: 10px !important; backdrop-filter: blur(8px) !important; }

/* ── MICROSCOPE GRID OVERLAY ── */
.micro-grid {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(59,130,246,.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,.03) 1px, transparent 1px);
    background-size: 50px 50px;
}
</style>

<!-- GRID OVERLAY -->
<div class="micro-grid"></div>

<!-- CANVAS -->
<canvas id="bio-canvas"></canvas>

<script>
(function() {
    var C = document.getElementById('bio-canvas');
    var ctx = C.getContext('2d');
    var W, H;
    var rbcs = [], wbcs = [], platelets = [], molecules = [], scanLines = [];
    var time = 0;

    function resize() {
        W = C.width  = window.innerWidth;
        H = C.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    /* ── SEL DARAH MERAH (bikonkaf, bergerak lambat) ── */
    function RBC() {
        this.reset(true);
    }
    RBC.prototype.reset = function(init) {
        this.x = init ? Math.random() * W : -60;
        this.y = Math.random() * H;
        this.r = 9 + Math.random() * 7;
        this.vx = .15 + Math.random() * .35;
        this.vy = (Math.random() - .5) * .2;
        this.angle = Math.random() * Math.PI * 2;
        this.aSpeed = (Math.random() - .5) * .008;
        this.alpha = .18 + Math.random() * .22;
        this.pulse = Math.random() * Math.PI * 2;
        this.pSpeed = .018 + Math.random() * .015;
        this.wobble = Math.random() * Math.PI * 2;
    };
    RBC.prototype.update = function() {
        this.x += this.vx;
        this.y += this.vy + Math.sin(this.wobble) * .08;
        this.wobble += .02;
        this.angle += this.aSpeed;
        this.pulse += this.pSpeed;
        if (this.x > W + 60) this.reset(false);
    };
    RBC.prototype.draw = function() {
        var pr = this.r * (1 + .05 * Math.sin(this.pulse));
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = this.alpha;

        /* Bayangan luar */
        ctx.beginPath();
        ctx.ellipse(0, 0, pr + 2, (pr + 2) * .58, 0, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(120,10,10,.15)';
        ctx.fill();

        /* Body bikonkaf */
        ctx.beginPath();
        ctx.ellipse(0, 0, pr, pr * .6, 0, 0, Math.PI * 2);
        var grad = ctx.createRadialGradient(-pr*.2, -pr*.1, pr*.05, 0, 0, pr);
        grad.addColorStop(0,   'rgba(255,100,100,.08)');
        grad.addColorStop(.35, 'rgba(200,50,50,.45)');
        grad.addColorStop(.7,  'rgba(160,20,20,.65)');
        grad.addColorStop(1,   'rgba(120,10,10,.8)');
        ctx.fillStyle = grad;
        ctx.fill();

        /* Tepi membran */
        ctx.strokeStyle = 'rgba(230,90,90,' + (this.alpha * 1.8) + ')';
        ctx.lineWidth = 1;
        ctx.stroke();

        /* Lekukan tengah */
        ctx.beginPath();
        ctx.ellipse(0, 0, pr * .35, pr * .2, 0, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(80,5,5,' + (this.alpha * 1.2) + ')';
        ctx.fill();

        /* Highlight */
        ctx.beginPath();
        ctx.ellipse(-pr*.25, -pr*.15, pr*.2, pr*.1, -Math.PI/6, 0, Math.PI*2);
        ctx.fillStyle = 'rgba(255,160,160,.12)';
        ctx.fill();

        ctx.restore();
    };

    /* ── SEL DARAH PUTIH ── */
    function WBC() {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.r = 13 + Math.random() * 5;
        this.vx = (Math.random() - .5) * .25;
        this.vy = (Math.random() - .5) * .25;
        this.alpha = .1 + Math.random() * .12;
        this.pulse = Math.random() * Math.PI * 2;
        this.pSpeed = .012 + Math.random() * .01;
        this.lobes = 3 + Math.floor(Math.random() * 2);
        this.rotation = Math.random() * Math.PI * 2;
        this.rSpeed = (Math.random() - .5) * .005;
    }
    WBC.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.pulse += this.pSpeed;
        this.rotation += this.rSpeed;
        if (this.x < -80) this.x = W + 80;
        if (this.x > W+80) this.x = -80;
        if (this.y < -80) this.y = H + 80;
        if (this.y > H+80) this.y = -80;
    };
    WBC.prototype.draw = function() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.globalAlpha = this.alpha;
        var r = this.r * (1 + .07 * Math.sin(this.pulse));
        /* Lobus inti */
        for (var i = 0; i < this.lobes; i++) {
            var ang = (i / this.lobes) * Math.PI * 2;
            ctx.beginPath();
            ctx.arc(Math.cos(ang)*r*.32, Math.sin(ang)*r*.32, r*.5, 0, Math.PI*2);
            var g = ctx.createRadialGradient(Math.cos(ang)*r*.2, Math.sin(ang)*r*.2, 0,
                Math.cos(ang)*r*.32, Math.sin(ang)*r*.32, r*.5);
            g.addColorStop(0, 'rgba(120,180,255,.35)');
            g.addColorStop(1, 'rgba(60,100,200,.15)');
            ctx.fillStyle = g;
            ctx.fill();
        }
        /* Membran */
        ctx.beginPath();
        ctx.arc(0, 0, r, 0, Math.PI*2);
        ctx.strokeStyle = 'rgba(100,160,255,' + (this.alpha*2.5) + ')';
        ctx.lineWidth = 1.2;
        ctx.setLineDash([3,5]);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.restore();
    };

    /* ── PLATELET (trombosit kecil) ── */
    function Platelet() {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.r = 3 + Math.random() * 3;
        this.vx = (Math.random() - .5) * .5;
        this.vy = (Math.random() - .5) * .5;
        this.alpha = .12 + Math.random() * .18;
        this.pulse = Math.random() * Math.PI * 2;
    }
    Platelet.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.pulse += .04;
        if (this.x < 0 || this.x > W) this.vx *= -1;
        if (this.y < 0 || this.y > H) this.vy *= -1;
    };
    Platelet.prototype.draw = function() {
        var r = this.r * (1 + .2*Math.sin(this.pulse));
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.beginPath();
        ctx.ellipse(this.x, this.y, r, r*.6, this.pulse, 0, Math.PI*2);
        ctx.fillStyle = 'rgba(250,200,100,.6)';
        ctx.fill();
        ctx.strokeStyle = 'rgba(255,220,120,.8)';
        ctx.lineWidth = .5;
        ctx.stroke();
        ctx.restore();
    };

    /* ── MOLEKUL / PARTIKEL ── */
    function Molecule() {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.vx = (Math.random() - .5) * .3;
        this.vy = (Math.random() - .5) * .3;
        this.size = 1 + Math.random() * 2.5;
        this.alpha = .06 + Math.random() * .12;
        this.color = ['59,130,246','99,102,241','16,185,129','236,72,153'][Math.floor(Math.random()*4)];
        this.pulse = Math.random() * Math.PI * 2;
        this.connected = [];
    }
    Molecule.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.pulse += .025;
        if (this.x < 0 || this.x > W) this.vx *= -1;
        if (this.y < 0 || this.y > H) this.vy *= -1;
    };
    Molecule.prototype.draw = function() {
        var s = this.size * (1 + .25*Math.sin(this.pulse));
        ctx.beginPath();
        ctx.arc(this.x, this.y, s, 0, Math.PI*2);
        ctx.fillStyle = 'rgba('+this.color+','+this.alpha+')';
        ctx.fill();
        /* Halo */
        ctx.beginPath();
        ctx.arc(this.x, this.y, s*2.5, 0, Math.PI*2);
        ctx.fillStyle = 'rgba('+this.color+','+(this.alpha*.2)+')';
        ctx.fill();
    };

    /* ── SCAN LINE (efek mikroskop) ── */
    function ScanLine() {
        this.y = Math.random() * H;
        this.vy = .3 + Math.random() * .5;
        this.alpha = .015 + Math.random() * .025;
        this.width = W;
    }
    ScanLine.prototype.update = function() {
        this.y += this.vy;
        if (this.y > H) { this.y = -2; this.alpha = .015 + Math.random()*.025; }
    };
    ScanLine.prototype.draw = function() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = 'rgba(59,130,246,1)';
        ctx.fillRect(0, this.y, this.width, 1);
        ctx.restore();
    };

    /* ── KONEKSI ANTAR MOLEKUL ── */
    function drawConnections() {
        for (var i = 0; i < molecules.length; i++) {
            for (var j = i+1; j < molecules.length; j++) {
                var dx = molecules[i].x - molecules[j].x;
                var dy = molecules[i].y - molecules[j].y;
                var d = Math.sqrt(dx*dx + dy*dy);
                if (d < 130) {
                    ctx.beginPath();
                    ctx.moveTo(molecules[i].x, molecules[i].y);
                    ctx.lineTo(molecules[j].x, molecules[j].y);
                    var a = .07 * (1 - d/130);
                    ctx.strokeStyle = 'rgba(59,130,246,'+a+')';
                    ctx.lineWidth = .7;
                    ctx.stroke();
                }
            }
        }
    }

    /* ── LINGKARAN MIKROSKOP (pojok) ── */
    function drawMicroscope() {
        var cx = W - 80, cy = H - 80, r = 55;
        ctx.save();
        ctx.globalAlpha = .06;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI*2);
        ctx.strokeStyle = 'rgba(59,130,246,1)';
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(cx, cy, r*.7, 0, Math.PI*2);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(cx-r, cy); ctx.lineTo(cx+r, cy);
        ctx.moveTo(cx, cy-r); ctx.lineTo(cx, cy+r);
        ctx.lineWidth = .5;
        ctx.stroke();
        /* Crosshair berputar */
        ctx.rotate && (function(){
            ctx.translate(cx,cy);
            ctx.rotate(time * .003);
            ctx.beginPath();
            ctx.moveTo(-r*.85,0); ctx.lineTo(-r*.5,0);
            ctx.moveTo(r*.5,0);   ctx.lineTo(r*.85,0);
            ctx.moveTo(0,-r*.85); ctx.lineTo(0,-r*.5);
            ctx.moveTo(0,r*.5);   ctx.lineTo(0,r*.85);
            ctx.globalAlpha = .1;
            ctx.strokeStyle = 'rgba(59,130,246,1)';
            ctx.lineWidth = 1;
            ctx.stroke();
        })();
        ctx.restore();
    }

    /* ── INIT ── */
    for (var i=0; i<22; i++) rbcs.push(new RBC());
    for (var i=0; i<6;  i++) wbcs.push(new WBC());
    for (var i=0; i<15; i++) platelets.push(new Platelet());
    for (var i=0; i<55; i++) molecules.push(new Molecule());
    for (var i=0; i<4;  i++) scanLines.push(new ScanLine());

    /* ── LOOP ── */
    function loop() {
        ctx.clearRect(0, 0, W, H);
        time++;

        drawConnections();
        scanLines.forEach(function(s){s.update();s.draw();});
        molecules.forEach(function(m){m.update();m.draw();});
        platelets.forEach(function(p){p.update();p.draw();});
        wbcs.forEach(function(w){w.update();w.draw();});
        rbcs.forEach(function(r){r.update();r.draw();});
        drawMicroscope();

        requestAnimationFrame(loop);
    }
    loop();
})();
</script>
"""


def inject_css():
    import streamlit as st
    st.markdown(ANIMATION_CSS, unsafe_allow_html=True)


def header_html(show_admin_btn=True, is_admin=False):
    admin_btn = ""
    if show_admin_btn and not is_admin:
        admin_btn = '<a href="/admin" target="_self" style="background:rgba(15,30,55,.8);color:#64748B;border:1px solid rgba(59,130,246,.2);padding:8px 16px;border-radius:8px;font-size:12px;text-decoration:none;transition:all .2s;backdrop-filter:blur(8px)">⚙ Admin</a>'
    if is_admin:
        admin_btn = '<span style="background:rgba(239,68,68,.1);color:#FCA5A5;border:1px solid rgba(239,68,68,.2);font-size:11px;padding:4px 12px;border-radius:20px;font-weight:500;letter-spacing:.3px">🔴 Admin Mode</span>'

    return f"""
    <div class="patelki-header">
        <div style="display:flex;align-items:center;gap:16px">
            <div class="patelki-logo">P</div>
            <div class="patelki-title">
                <h1>DPC Patelki Banda Aceh</h1>
                <p>Dewan Pimpinan Cabang &nbsp;·&nbsp; Sistem Data Anggota</p>
            </div>
        </div>
        {admin_btn}
    </div>
    """
