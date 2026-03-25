const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbwOSOuL2LnFRBro229jzfpxrtN5M7S7bLLtUX1YKBSuWCU3pCSsQ5TBuQVc67gCVD2z/exec';

// ===== State =====
let allData = [];
let editingRecord = null;
let deletingRecord = null;

const defaultConfig = {
    dashboard_title: 'LABORATORIUM DASHBOARD',
    subtitle_text: 'Sistem Manajemen Data Staff',
    bg_color: '#060e18',
    accent_color: '#00ff88',
    card_color: '#0f1928',
    text_color: '#e0f0e8',
    muted_color: '#a0c8b4',
    font_family: 'Outfit',
    font_size: 14
};

// ===== Toast =====
function showToast(msg, type = 'success') {
    const c = document.getElementById('toast-container');
    const t = document.createElement('div');
    t.className = `toast toast-${type}`;
    t.textContent = msg;
    c.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transition = 'opacity 0.3s'; setTimeout(() => t.remove(), 300); }, 3000);
}

// ===== Format =====
function fmtCurrency(n) {
    if (!n && n !== 0) return '-';
    const num = typeof n === 'string' ? parseInt(n) : n;
    return 'Rp ' + num.toLocaleString('id-ID');
}
function fmtDate(d) {
    if (!d) return '-';
    try {
        const dt = new Date(d);
        if (isNaN(dt.getTime())) return d;
        return dt.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' });
    } catch { return d; }
}

// ===== Filters =====
function getFiltered() {
    const nama = document.getElementById('filter-nama').value.toLowerCase();
    const status = document.getElementById('filter-status').value;
    const instansi = document.getElementById('filter-instansi').value;
    const gaji = document.getElementById('filter-gaji').value;
    const kelamin = document.getElementById('f-kelamin').value;

    return allData.filter(r => {
        if (nama && !(r.nama || '').toLowerCase().includes(nama)) return false;
        if (status && (r.status_pekerjaan || '') !== status) return false;
        if (instansi && (r.instansi || '') !== instansi) return false;
        if (kelamin && (r.jenis_kelamin || '') !== kelamin) return false;
        if (gaji) {
            const [min, max] = gaji.split('-').map(Number);
            const mappedVal = r.gaji ? parseInt(r.gaji.split('-')[0]) : 0;
            if (mappedVal < min || mappedVal > max || isNaN(mappedVal)) return false;
        }
        return true;
    });
}

function updateFilterOptions() {
    const statusSet = new Set();
    const instansiSet = new Set();
    allData.forEach(r => {
        if (r.status_pekerjaan) statusSet.add(r.status_pekerjaan);
        if (r.instansi) instansiSet.add(r.instansi);
    });

    const selStatus = document.getElementById('filter-status');
    const curStatus = selStatus.value;
    selStatus.innerHTML = '<option value="">Semua Status</option>';
    [...statusSet].sort().forEach(s => {
        selStatus.innerHTML += `<option value="${s}" ${s === curStatus ? 'selected' : ''}>${s}</option>`;
    });

    const selInst = document.getElementById('filter-instansi');
    const curInst = selInst.value;
    selInst.innerHTML = '<option value="">Semua Instansi</option>';
    [...instansiSet].sort().forEach(s => {
        selInst.innerHTML += `<option value="${s}" ${s === curInst ? 'selected' : ''}>${s}</option>`;
    });
}

function updateStats() {
    const total = allData.length;
    const active = allData.filter(r => (r.status_pekerjaan || '').toLowerCase() === 'aktif').length;
    const avgGaji = total > 0 ? allData.reduce((s, r) => {
        const g = r.gaji ? parseInt(r.gaji.split('-')[0]) || 0 : 0;
        return s + g;
    }, 0) / total : 0;
    const instansi = new Set(allData.map(r => r.instansi).filter(Boolean)).size;

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-active').textContent = active;
    document.getElementById('stat-avg').textContent = avgGaji > 0 ? fmtCurrency(Math.round(avgGaji)).replace('Rp ', '') : '0';
    document.getElementById('stat-inst').textContent = instansi;

    updateCharts();
}

function updateCharts() {
    // Instansi Chart
    const instansiCount = {};
    allData.forEach(r => {
        const inst = r.instansi || 'Tidak Diisi';
        instansiCount[inst] = (instansiCount[inst] || 0) + 1;
    });

    const instansiChartEl = document.getElementById('chart-instansi');
    instansiChartEl.innerHTML = '';
    const totalInstansi = Object.values(instansiCount).reduce((a, b) => a + b, 0);

    if (totalInstansi === 0) {
        instansiChartEl.innerHTML = '<p style="color:rgba(160,200,180,0.4);font-size:13px;margin:0;">Belum ada data</p>';
    } else {
        Object.entries(instansiCount).sort((a, b) => b[1] - a[1]).forEach(([inst, count]) => {
            const pct = Math.round((count / totalInstansi) * 100);
            instansiChartEl.innerHTML += `
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="flex:0 0 120px;font-size:12px;color:rgba(160,200,180,0.7);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${inst}</div>
      <div style="flex:1;height:20px;background:rgba(0,255,136,0.1);border-radius:4px;position:relative;overflow:hidden;">
        <div style="height:100%;background:linear-gradient(90deg,#00ff88,#00cc6a);width:${pct}%;border-radius:4px;transition:width 0.3s ease;"></div>
      </div>
      <div style="flex:0 0 50px;text-align:right;font-size:12px;color:#00ff88;font-weight:600;">${count} (${pct}%)</div>
    </div>
  `;
        });
    }

    // Gaji Chart
    const gajiRanges = {
        'Rp 1 - 3.5 Juta': 0,
        'Rp 3.6 - 5 Juta': 0,
        'Rp > 5 Juta': 0
    };

    allData.forEach(r => {
        if (r.gaji === '1000000-3500000') gajiRanges['Rp 1 - 3.5 Juta']++;
        else if (r.gaji === '3600000-5000000') gajiRanges['Rp 3.6 - 5 Juta']++;
        else if (r.gaji === '5000000-999999999') gajiRanges['Rp > 5 Juta']++;
        // Fallback checks
        else {
            let val = parseInt(r.gaji ? r.gaji.split('-')[0] : 0) || 0;
            if (val > 0 && val <= 3500000) gajiRanges['Rp 1 - 3.5 Juta']++;
            else if (val > 3500000 && val <= 5000000) gajiRanges['Rp 3.6 - 5 Juta']++;
            else if (val > 5000000) gajiRanges['Rp > 5 Juta']++;
        }
    });

    const gajiChartEl = document.getElementById('chart-gaji');
    gajiChartEl.innerHTML = '';
    const totalGaji = Object.values(gajiRanges).reduce((a, b) => a + b, 0);

    if (totalGaji === 0) {
        gajiChartEl.innerHTML = '<p style="color:rgba(160,200,180,0.4);font-size:13px;margin:0;">Belum ada data</p>';
    } else {
        const colors = ['#00ff88', '#00cc6a', '#00aa55'];
        let colorIdx = 0;
        Object.entries(gajiRanges).forEach(([range, count]) => {
            if (count > 0) {
                const pct = Math.round((count / totalGaji) * 100);
                gajiChartEl.innerHTML += `
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="flex:0 0 120px;font-size:12px;color:rgba(160,200,180,0.7);">${range}</div>
        <div style="flex:1;height:20px;background:rgba(0,255,136,0.1);border-radius:4px;position:relative;overflow:hidden;">
          <div style="height:100%;background:${colors[colorIdx]};width:${pct}%;border-radius:4px;transition:width 0.3s ease;"></div>
        </div>
        <div style="flex:0 0 50px;text-align:right;font-size:12px;color:${colors[colorIdx]};font-weight:600;">${count} (${pct}%)</div>
      </div>
    `;
                colorIdx++;
            }
        });
    }

    // Jenis Kelamin Chart
    const kelamimCount = {};
    allData.forEach(r => {
        const kel = r.jenis_kelamin || 'Tidak Diisi';
        kelamimCount[kel] = (kelamimCount[kel] || 0) + 1;
    });

    const kelamimChartEl = document.getElementById('chart-kelamin');
    kelamimChartEl.innerHTML = '';
    const totalKelamin = Object.values(kelamimCount).reduce((a, b) => a + b, 0);

    if (totalKelamin === 0) {
        kelamimChartEl.innerHTML = '<p style="color:rgba(160,200,180,0.4);font-size:13px;margin:0;">Belum ada data</p>';
    } else {
        const kelamimColors = { 'Laki-laki': '#00ff88', 'Perempuan': '#ff6b9d', 'Tidak Diisi': 'rgba(160,200,180,0.3)' };
        Object.entries(kelamimCount).sort((a, b) => b[1] - a[1]).forEach(([kel, count]) => {
            const pct = Math.round((count / totalKelamin) * 100);
            const color = kelamimColors[kel] || '#00ff88';
            kelamimChartEl.innerHTML += `
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="flex:0 0 120px;font-size:12px;color:rgba(160,200,180,0.7);">${kel}</div>
      <div style="flex:1;height:20px;background:rgba(0,255,136,0.1);border-radius:4px;position:relative;overflow:hidden;">
        <div style="height:100%;background:${color};width:${pct}%;border-radius:4px;transition:width 0.3s ease;"></div>
      </div>
      <div style="flex:0 0 50px;text-align:right;font-size:12px;color:${color};font-weight:600;">${count} (${pct}%)</div>
    </div>
  `;
        });
    }
}

// ===== Table =====
function renderTable() {
    const filtered = getFiltered();
    const tbody = document.getElementById('table-body');
    const empty = document.getElementById('empty-state');
    const noResults = document.getElementById('no-results');
    const countEl = document.getElementById('table-count');

    if (allData.length === 0) {
        tbody.innerHTML = '';
        empty.style.display = 'block';
        noResults.style.display = 'none';
        countEl.style.display = 'none';
        return;
    }

    empty.style.display = 'none';

    if (filtered.length === 0) {
        tbody.innerHTML = '';
        noResults.style.display = 'block';
        countEl.style.display = 'none';
        return;
    }

    noResults.style.display = 'none';
    countEl.style.display = 'block';
    countEl.textContent = `Menampilkan ${filtered.length} dari ${allData.length} data`;

    // Selective DOM update
    const existingRows = new Map();
    [...tbody.children].forEach(tr => existingRows.set(tr.dataset.id, tr));

    const newIds = new Set(filtered.map(r => r.id));

    // Remove rows no longer in view
    existingRows.forEach((tr, id) => {
        if (!newIds.has(id)) tr.remove();
    });

    filtered.forEach((r, i) => {
        const id = r.id;
        let tr = existingRows.get(id);
        if (tr) {
            updateRow(tr, r);
        } else {
            tr = createRow(r);
            tbody.appendChild(tr);
        }
    });

    lucide.createIcons();
}

function createRow(r) {
    const tr = document.createElement('tr');
    tr.className = 'table-row';
    tr.dataset.id = r.id;
    fillRow(tr, r);
    return tr;
}

function updateRow(tr, r) {
    fillRow(tr, r);
}

const parseGajiLabel = (val) => {
    if (val === '1000000-3500000') return 'Rp 1 - 3.5 Juta';
    if (val === '3600000-5000000') return 'Rp 3.6 - 5 Juta';
    if (val === '5000000-999999999') return '> Rp 5 Juta';
    return val;
};

function fillRow(tr, r) {
    const statusColor = (r.status_pekerjaan || '').toLowerCase() === 'aktif'
        ? 'background:rgba(0,255,136,0.12);color:#00ff88;'
        : 'background:rgba(255,180,60,0.12);color:#ffb43c;';
    tr.innerHTML = `
<td style="padding:12px 16px;font-size:14px;font-weight:500;color:#e0f0e8;">${r.nama || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);font-family:'Space Mono',monospace;">${r.nomor_str || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);font-family:'Space Mono',monospace;">${r.no_kta || '-'}</td>
<td style="padding:12px 16px;"><span style="padding:4px 10px;border-radius:20px;font-size:12px;font-weight:500;${statusColor}">${r.status_pekerjaan || '-'}</span></td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);">${r.instansi || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:#e0f0e8;text-align:right;font-family:'Space Mono',monospace;">${parseGajiLabel(r.gaji) || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);">${r.jenis_kelamin || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);">${r.phone || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);">${r.email || '-'}</td>
<td style="padding:12px 16px;font-size:13px;color:rgba(160,200,180,0.7);">${fmtDate(r.tanggal_lahir)}</td>
<td style="padding:12px 16px;text-align:center;">
  <div style="display:flex;gap:6px;justify-content:center;">
    <button onclick="openEdit('${r.id}')" style="background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.15);border-radius:6px;padding:6px;cursor:pointer;" aria-label="Edit">
      <i data-lucide="edit" style="width:14px;height:14px;color:#00ff88;"></i>
    </button>
    <button onclick="openDelete('${r.id}')" style="background:rgba(255,60,60,0.08);border:1px solid rgba(255,60,60,0.15);border-radius:6px;padding:6px;cursor:pointer;" aria-label="Hapus">
      <i data-lucide="trash-2" style="width:14px;height:14px;color:#ff5c5c;"></i>
    </button>
  </div>
</td>
`;
}

// ===== Modal =====
function openModal(record) {
    editingRecord = record || null;
    document.getElementById('modal-title').textContent = record ? 'Edit Data Staff' : 'Tambah Data Staff';
    document.getElementById('submit-text').textContent = record ? 'Update' : 'Simpan';

    document.getElementById('f-nama').value = record ? record.nama || '' : '';
    document.getElementById('f-str').value = record ? record.nomor_str || '' : '';
    document.getElementById('f-kta').value = record ? record.no_kta || '' : '';
    document.getElementById('f-status').value = record ? record.status_pekerjaan || '' : '';
    document.getElementById('f-instansi').value = record ? record.instansi || '' : '';
    document.getElementById('f-gaji').value = record ? record.gaji || '' : '';
    document.getElementById('f-phone').value = record ? record.phone || '' : '';
    document.getElementById('f-email').value = record ? record.email || '' : '';
    
    let dbDate = record && record.tanggal_lahir ? record.tanggal_lahir : '';
    if (dbDate && dbDate.includes('T')) {
        dbDate = dbDate.split('T')[0];
    }
    document.getElementById('f-lahir').value = dbDate;

    document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    editingRecord = null;
}

function openEdit(id) {
    const record = allData.find(r => r.id == id);
    if (record) openModal(record);
}

function openDelete(id) {
    deletingRecord = allData.find(r => r.id == id);
    if (!deletingRecord) return;
    document.getElementById('delete-name').textContent = `"${deletingRecord.nama}" akan dihapus secara permanen.`;
    document.getElementById('delete-modal').style.display = 'flex';
}

function closeDeleteModal() {
    document.getElementById('delete-modal').style.display = 'none';
    deletingRecord = null;
}

// ===== Form Submit =====
document.getElementById('staff-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!WEB_APP_URL || WEB_APP_URL === 'PASTE_YOUR_GOOGLE_APPS_SCRIPT_URL_HERE') {
        showToast('ERROR: WEB_APP_URL belum di-setting di script.js', 'error');
        return;
    }

    const btn = document.getElementById('modal-submit');
    const spinner = document.getElementById('submit-spinner');
    
    btn.disabled = true;
    spinner.style.display = 'inline-block';

    const reqData = {
        action: editingRecord ? 'edit' : 'add',
        nama: document.getElementById('f-nama').value.trim(),
        nomor_str: document.getElementById('f-str').value.trim(),
        no_kta: document.getElementById('f-kta').value.trim(),
        status_pekerjaan: document.getElementById('f-status').value.trim(),
        instansi: document.getElementById('f-instansi').value.trim(),
        gaji: document.getElementById('f-gaji').value.trim(),
        jenis_kelamin: document.getElementById('f-kelamin').value.trim(),
        phone: document.getElementById('f-phone').value.trim(),
        email: document.getElementById('f-email').value.trim(),
        tanggal_lahir: document.getElementById('f-lahir').value
    };

    if (editingRecord) {
        reqData.id = editingRecord.id;
    }

    try {
        const response = await fetch(WEB_APP_URL, {
            method: 'POST',
            body: JSON.stringify(reqData)
        });
        const result = await response.json();
        
        btn.disabled = false;
        spinner.style.display = 'none';

        if (result.isOk) {
            showToast(editingRecord ? 'Data berhasil diperbarui!' : 'Data berhasil ditambahkan!');
            closeModal();
            loadSheetData(); // refresh data
        } else {
            showToast('Gagal menyimpan data. Coba lagi.', 'error');
            console.error(result);
        }
    } catch(err) {
        btn.disabled = false;
        spinner.style.display = 'none';
        showToast('Terjadi kesalahan koneksi!', 'error');
        console.error(err);
    }
});

// ===== Delete =====
document.getElementById('delete-confirm').addEventListener('click', async () => {
    if (!deletingRecord) return;
    if (!WEB_APP_URL || WEB_APP_URL === 'PASTE_YOUR_GOOGLE_APPS_SCRIPT_URL_HERE') {
        showToast('ERROR: WEB_APP_URL belum di-setting di script.js', 'error');
        return;
    }

    const btn = document.getElementById('delete-confirm');
    const spinner = document.getElementById('delete-spinner');
    btn.disabled = true;
    spinner.style.display = 'inline-block';

    try {
        const response = await fetch(WEB_APP_URL, {
            method: 'POST',
            body: JSON.stringify({ action: 'delete', id: deletingRecord.id })
        });
        const result = await response.json();

        btn.disabled = false;
        spinner.style.display = 'none';

        if (result.isOk) {
            showToast('Data berhasil dihapus.');
            closeDeleteModal();
            loadSheetData(); // refresh
        } else {
            showToast('Gagal menghapus data. Coba lagi.', 'error');
            console.error(result);
        }
    } catch (err) {
        btn.disabled = false;
        spinner.style.display = 'none';
        showToast('Terjadi kesalahan koneksi!', 'error');
        console.error(err);
    }
});

// ===== Fetch Initial Data =====
async function loadSheetData() {
    if (!WEB_APP_URL || WEB_APP_URL === 'PASTE_YOUR_GOOGLE_APPS_SCRIPT_URL_HERE') {
        console.warn('Set WEB_APP_URL to fetch sheet data.');
        allData = [];
        renderTable();
        return;
    }
    try {
        const response = await fetch(WEB_APP_URL);
        const data = await response.json();
        allData = data || [];
        updateFilterOptions();
        updateStats();
        renderTable();
    } catch (err) {
        showToast('Gagal memuat data awal dari Google Sheet.', 'error');
        console.error(err);
    }
}

// ===== Event Listeners & Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('btn-add').addEventListener('click', () => openModal(null));
    document.getElementById('modal-close').addEventListener('click', closeModal);
    document.getElementById('modal-cancel').addEventListener('click', closeModal);
    document.getElementById('delete-cancel').addEventListener('click', closeDeleteModal);
    document.getElementById('modal').addEventListener('click', (e) => { if (e.target.id === 'modal') closeModal(); });
    document.getElementById('delete-modal').addEventListener('click', (e) => { if (e.target.id === 'delete-modal') closeDeleteModal(); });

    ['filter-nama', 'filter-status', 'filter-instansi', 'filter-gaji', 'f-kelamin'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', renderTable);
            el.addEventListener('change', renderTable);
        }
    });

    lucide.createIcons();
    loadSheetData();
});
