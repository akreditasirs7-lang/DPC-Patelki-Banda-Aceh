ANIMATION_CSS = """
<style>
/* ── IMPORT FONT ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* ── HIDE STREAMLIT DEFAULT ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── CANVAS ANIMASI ── */
#bio-canvas {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
}

/* ── SEMUA KONTEN DI ATAS CANVAS ── */
.stApp > div { position: relative; z-index: 1; }

/* ── HEADER ── */
.patelki-header {
    background: linear-gradient(135deg, #0D2137 0%, #0F2744 50%, #0A1F3D 100%);
    padding: 1.1rem 2rem;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid rgba(59,130,246,.2);
    position: relative; z-index: 10;
    box-shadow: 0 4px 24px rgba(0,0,0,.4);
}
.patelki-logo {
    width: 52px; height: 52px; border-radius: 50%;
    background: linear-gradient(135deg, #3B82F6, #1D4ED8);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 700; color: #fff;
    border: 2px solid rgba(255,255,255,.25);
    box-shadow: 0 0 20px rgba(59,130,246,.5);
    flex-shrink: 0;
}
.patelki-title h1 { font-size: 17px; font-weight: 700; color: #fff; margin: 0; }
.patelki-title p  { font-size: 11px; color: #93C5FD; margin: 2px 0 0; }

/* ── STAT CARDS ── */
.stat-card {
    background: linear-gradient(135deg, rgba(30,41,59,.95), rgba(15,23,42,.95));
    border: 1px solid rgba(59,130,246,.2);
    border-radius: 14px; padding: 1.1rem 1.3rem;
    backdrop-filter: blur(12px);
    transition: transform .2s, box-shadow .2s;
    position: relative; overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #3B82F6, transparent);
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(59,130,246,.25); }
.stat-lbl { font-size: 10px; color: #64748B; text-transform: uppercase; letter-spacing: .7px; margin-bottom: 6px; }
.stat-val { font-size: 28px; font-weight: 700; color: #F1F5F9; line-height: 1; }
.stat-sub { font-size: 11px; color: #475569; margin-top: 4px; }

/* ── PANEL / TABLE ── */
.glass-panel {
    background: rgba(30,41,59,.9);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px; overflow: hidden;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0,0,0,.3);
}
.panel-header {
    padding: .9rem 1.4rem;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,.07);
    background: linear-gradient(90deg, rgba(59,130,246,.1), transparent);
}
.panel-header h3 { font-size: 13px; font-weight: 600; color: #F1F5F9; margin: 0; }

/* ── BADGE ── */
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.badge-aktif  { background: rgba(16,185,129,.15); color: #6EE7B7; border: 1px solid rgba(16,185,129,.3); }
.badge-non    { background: rgba(239,68,68,.12);  color: #FCA5A5; border: 1px solid rgba(239,68,68,.25); }
.badge-lunas  { background: rgba(59,130,246,.15); color: #93C5FD; border: 1px solid rgba(59,130,246,.3); }
.badge-belum  { background: rgba(245,158,11,.12); color: #FCD34D; border: 1px solid rgba(245,158,11,.25); }

/* ── STREAMLIT FORM ── */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stDateInput"] input,
div[data-testid="stNumberInput"] input {
    background: rgba(15,23,42,.8) !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 8px !important; color: #F1F5F9 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
}
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    border: none !important; color: #fff !important;
    font-weight: 600 !important; border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(37,99,235,.35) !important;
    transition: transform .15s !important;
}
div[data-testid="stFormSubmitButton"] button:hover { transform: translateY(-1px) !important; }

/* ── TABS ── */
div[data-testid="stTabs"] button {
    font-size: 13px !important; font-weight: 500 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #3B82F6 !important;
    border-bottom-color: #3B82F6 !important;
}

/* ── DATAFRAME TABLE ── */
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── TOAST / NOTIF ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #3B82F6; }
</style>

<!-- CANVAS ANIMASI SEL DARAH & LABORATORIUM -->
<canvas id="bio-canvas"></canvas>
<script>
(function() {
    var canvas = document.getElementById('bio-canvas');
    var ctx = canvas.getContext('2d');
    var W, H, particles = [], molecules = [], bubbles = [];
    var RAF;

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    /* ── SEL DARAH MERAH ── */
    function RBC(x, y) {
        this.x = x || Math.random() * W;
        this.y = y || Math.random() * H;
        this.r = 10 + Math.random() * 8;
        this.vx = (Math.random() - .5) * .6;
        this.vy = (Math.random() - .5) * .6;
        this.angle = Math.random() * Math.PI * 2;
        this.aSpeed = (Math.random() - .5) * .015;
        this.alpha = .12 + Math.random() * .18;
        this.pulse = Math.random() * Math.PI * 2;
        this.pSpeed = .02 + Math.random() * .02;
    }
    RBC.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.angle += this.aSpeed;
        this.pulse += this.pSpeed;
        if (this.x < -50) this.x = W + 50;
        if (this.x > W + 50) this.x = -50;
        if (this.y < -50) this.y = H + 50;
        if (this.y > H + 50) this.y = -50;
    };
    RBC.prototype.draw = function() {
        var pr = this.r * (1 + .06 * Math.sin(this.pulse));
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.globalAlpha = this.alpha;
        /* Bentuk bikonkaf sel darah merah */
        ctx.beginPath();
        ctx.ellipse(0, 0, pr, pr * .6, 0, 0, Math.PI * 2);
        var grad = ctx.createRadialGradient(0, 0, pr * .15, 0, 0, pr);
        grad.addColorStop(0, 'rgba(220,50,50,.05)');
        grad.addColorStop(.5, 'rgba(180,40,40,.35)');
        grad.addColorStop(1, 'rgba(140,20,20,.55)');
        ctx.fillStyle = grad;
        ctx.fill();
        /* Tepi sel */
        ctx.strokeStyle = 'rgba(220,80,80,' + (this.alpha * 2.5) + ')';
        ctx.lineWidth = 1.2;
        ctx.stroke();
        /* Lekukan tengah (bikonkaf) */
        ctx.beginPath();
        ctx.ellipse(0, 0, pr * .38, pr * .22, 0, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(100,15,15,' + (this.alpha * .9) + ')';
        ctx.fill();
        ctx.restore();
    };

    /* ── SEL DARAH PUTIH ── */
    function WBC(x, y) {
        this.x = x || Math.random() * W;
        this.y = y || Math.random() * H;
        this.r = 14 + Math.random() * 6;
        this.vx = (Math.random() - .5) * .3;
        this.vy = (Math.random() - .5) * .3;
        this.alpha = .07 + Math.random() * .1;
        this.pulse = Math.random() * Math.PI * 2;
        this.pSpeed = .015 + Math.random() * .015;
        this.lobes = 3 + Math.floor(Math.random() * 3);
    }
    WBC.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.pulse += this.pSpeed;
        if (this.x < -60) this.x = W + 60;
        if (this.x > W + 60) this.x = -60;
        if (this.y < -60) this.y = H + 60;
        if (this.y > H + 60) this.y = -60;
    };
    WBC.prototype.draw = function() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.globalAlpha = this.alpha;
        var r = this.r * (1 + .08 * Math.sin(this.pulse));
        /* Inti berlobus */
        for (var i = 0; i < this.lobes; i++) {
            var ang = (i / this.lobes) * Math.PI * 2;
            var lx = Math.cos(ang) * r * .35;
            var ly = Math.sin(ang) * r * .35;
            ctx.beginPath();
            ctx.arc(lx, ly, r * .55, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(100,160,255,.22)';
            ctx.fill();
            ctx.strokeStyle = 'rgba(120,180,255,.4)';
            ctx.lineWidth = 1;
            ctx.stroke();
        }
        /* Membran luar */
        ctx.beginPath();
        ctx.arc(0, 0, r, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(140,190,255,' + (this.alpha * 3) + ')';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([3, 4]);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.restore();
    };

    /* ── MOLEKUL DNA (spiral titik) ── */
    function Molecule() {
        this.x = Math.random() * W;
        this.y = Math.random() * H;
        this.vx = (Math.random() - .5) * .4;
        this.vy = (Math.random() - .5) * .4;
        this.size = 1.5 + Math.random() * 2;
        this.alpha = .08 + Math.random() * .15;
        this.color = Math.random() > .5 ? '59,130,246' : '99,102,241';
        this.pulse = Math.random() * Math.PI * 2;
    }
    Molecule.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.pulse += .03;
        if (this.x < 0 || this.x > W) this.vx *= -1;
        if (this.y < 0 || this.y > H) this.vy *= -1;
    };
    Molecule.prototype.draw = function() {
        var s = this.size * (1 + .3 * Math.sin(this.pulse));
        ctx.beginPath();
        ctx.arc(this.x, this.y, s, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + this.color + ',' + this.alpha + ')';
        ctx.fill();
    };

    /* ── BUBBLE TABUNG LAB ── */
    function Bubble() {
        this.reset();
    }
    Bubble.prototype.reset = function() {
        this.x = Math.random() * W;
        this.y = H + 20;
        this.r = 3 + Math.random() * 7;
        this.vy = -.3 - Math.random() * .5;
        this.vx = (Math.random() - .5) * .4;
        this.alpha = .04 + Math.random() * .1;
        this.color = Math.random() > .6 ? '59,130,246' : (Math.random() > .5 ? '16,185,129' : '99,102,241');
    };
    Bubble.prototype.update = function() {
        this.x += this.vx; this.y += this.vy;
        this.alpha *= .999;
        if (this.y < -20) this.reset();
    };
    Bubble.prototype.draw = function() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(' + this.color + ',' + (this.alpha * 2.5) + ')';
        ctx.lineWidth = 1;
        ctx.stroke();
        /* Pantulan cahaya */
        ctx.beginPath();
        ctx.arc(this.x - this.r * .3, this.y - this.r * .3, this.r * .25, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,255,255,' + (this.alpha * 1.5) + ')';
        ctx.fill();
    };

    /* ── GARIS KONEKSI ── */
    function drawConnections() {
        for (var i = 0; i < molecules.length; i++) {
            for (var j = i + 1; j < molecules.length; j++) {
                var dx = molecules[i].x - molecules[j].x;
                var dy = molecules[i].y - molecules[j].y;
                var dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(molecules[i].x, molecules[i].y);
                    ctx.lineTo(molecules[j].x, molecules[j].y);
                    ctx.strokeStyle = 'rgba(59,130,246,' + (.06 * (1 - dist / 120)) + ')';
                    ctx.lineWidth = .8;
                    ctx.stroke();
                }
            }
        }
    }

    /* ── GRID LATAR ── */
    function drawGrid() {
        ctx.strokeStyle = 'rgba(30,58,138,.06)';
        ctx.lineWidth = .5;
        var step = 60;
        for (var x = 0; x < W; x += step) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
        }
        for (var y = 0; y < H; y += step) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
        }
    }

    /* ── INIT ── */
    for (var i = 0; i < 28; i++) particles.push(new RBC());
    for (var i = 0; i < 8;  i++) particles.push(new WBC());
    for (var i = 0; i < 60; i++) molecules.push(new Molecule());
    for (var i = 0; i < 25; i++) bubbles.push(new Bubble());

    /* ── LOOP ── */
    function loop() {
        ctx.clearRect(0, 0, W, H);
        drawGrid();
        drawConnections();
        molecules.forEach(function(m) { m.update(); m.draw(); });
        bubbles.forEach(function(b) { b.update(); b.draw(); });
        particles.forEach(function(p) { p.update(); p.draw(); });
        RAF = requestAnimationFrame(loop);
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
        admin_btn = '<a href="?page=admin" target="_self" style="background:transparent;color:#64748B;border:1px solid rgba(255,255,255,.1);padding:8px 14px;border-radius:8px;font-size:12px;text-decoration:none;transition:all .15s">⚙ Admin</a>'
    if is_admin:
        admin_btn = '<span style="background:rgba(239,68,68,.15);color:#FCA5A5;border:1px solid rgba(239,68,68,.25);font-size:11px;padding:4px 12px;border-radius:20px;font-weight:500">🔴 Admin Mode</span>'

    return f"""
    <div class="patelki-header">
        <div style="display:flex;align-items:center;gap:14px">
            <div class="patelki-logo">P</div>
            <div class="patelki-title">
                <h1>DPC Patelki Banda Aceh</h1>
                <p>Dewan Pimpinan Cabang · Sistem Data Anggota</p>
            </div>
        </div>
        {admin_btn}
    </div>
    """
