// =============================================
// GANTI DENGAN ID GOOGLE SHEETS KAMU
// =============================================
var SPREADSHEET_ID = 'GANTI_DENGAN_ID_SPREADSHEET_KAMU';
var SHEET_ANGGOTA  = 'Data Anggota';
var SHEET_IURAN    = 'Data Iuran';

// ── ROUTING ──
function doGet(e) {
  var page = (e && e.parameter && e.parameter.page) ? e.parameter.page : 'dashboard';
  var file = (page === 'admin') ? 'Admin' : 'Index';
  return HtmlService.createHtmlOutputFromFile(file)
    .setTitle('DPC Patelki Banda Aceh')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// ── LOGIN ADMIN ──
function adminLogin(username, password) {
  var props = PropertiesService.getScriptProperties();
  var storedUser = props.getProperty('ADMIN_USER') || 'admin';
  var storedPass = props.getProperty('ADMIN_PASS') || 'patelki2024';
  if (username === storedUser && password === storedPass) {
    var token = Utilities.getUuid();
    props.setProperty('SESSION_' + token, new Date().getTime().toString());
    return { success: true, token: token };
  }
  return { success: false, message: 'Username atau password salah.' };
}

function checkSession(token) {
  if (!token) return false;
  var props = PropertiesService.getScriptProperties();
  var ts = props.getProperty('SESSION_' + token);
  if (!ts) return false;
  // Sesi berlaku 8 jam
  var diff = new Date().getTime() - parseInt(ts);
  return diff < 8 * 60 * 60 * 1000;
}

function adminLogout(token) {
  PropertiesService.getScriptProperties().deleteProperty('SESSION_' + token);
  return { success: true };
}

// ── ANGGOTA: SIMPAN DATA BARU ──
function submitForm(data) {
  try {
    var sheet = getOrCreateAnggota();
    sheet.appendRow([
      new Date(), data.nama, data.jenisKelamin, data.tanggalLahir,
      data.nomorSTR, data.noKTA, data.statusPekerjaan, data.instansi,
      data.gaji, data.phone, data.email, data.status
    ]);
    return { success: true, message: 'Data berhasil disimpan!' };
  } catch (e) {
    return { success: false, message: 'Gagal: ' + e.message };
  }
}

// ── ANGGOTA: AMBIL SEMUA ──
function getAllData() {
  try {
    var sheet = getOrCreateAnggota();
    var last = sheet.getLastRow();
    if (last < 2) return [];
    return sheet.getRange(2, 1, last - 1, 12).getValues();
  } catch(e) { return []; }
}

// ── IURAN: SIMPAN / UPDATE ──
function simpanIuran(token, data) {
  if (!checkSession(token)) return { success: false, message: 'Sesi habis. Login ulang.' };
  try {
    var sheet = getOrCreateIuran();
    var rows = sheet.getDataRange().getValues();
    // Cari baris yang noKTA-nya sama
    for (var i = 1; i < rows.length; i++) {
      if (String(rows[i][0]) === String(data.noKTA)) {
        sheet.getRange(i + 1, 1, 1, 6).setValues([[
          data.noKTA, data.nama, data.tahunDari, data.tahunSampai,
          data.status, new Date()
        ]]);
        return { success: true, message: 'Data iuran diperbarui!' };
      }
    }
    // Baru
    sheet.appendRow([data.noKTA, data.nama, data.tahunDari, data.tahunSampai, data.status, new Date()]);
    return { success: true, message: 'Data iuran disimpan!' };
  } catch(e) {
    return { success: false, message: 'Gagal: ' + e.message };
  }
}

// ── IURAN: AMBIL SEMUA (publik) ──
function getAllIuran() {
  try {
    var sheet = getOrCreateIuran();
    var last = sheet.getLastRow();
    if (last < 2) return [];
    return sheet.getRange(2, 1, last - 1, 6).getValues();
  } catch(e) { return []; }
}

// ── IURAN: HAPUS ──
function hapusIuran(token, noKTA) {
  if (!checkSession(token)) return { success: false, message: 'Sesi habis.' };
  try {
    var sheet = getOrCreateIuran();
    var rows = sheet.getDataRange().getValues();
    for (var i = rows.length - 1; i >= 1; i--) {
      if (String(rows[i][0]) === String(noKTA)) {
        sheet.deleteRow(i + 1);
        return { success: true, message: 'Data iuran dihapus.' };
      }
    }
    return { success: false, message: 'Data tidak ditemukan.' };
  } catch(e) {
    return { success: false, message: 'Gagal: ' + e.message };
  }
}

// ── HAPUS ANGGOTA ──
function hapusAnggota(token, noKTA) {
  if (!checkSession(token)) return { success: false, message: 'Sesi habis.' };
  try {
    var sheet = getOrCreateAnggota();
    var rows = sheet.getDataRange().getValues();
    for (var i = rows.length - 1; i >= 1; i--) {
      if (String(rows[i][5]) === String(noKTA)) {
        sheet.deleteRow(i + 1);
        return { success: true, message: 'Anggota dihapus.' };
      }
    }
    return { success: false, message: 'Anggota tidak ditemukan.' };
  } catch(e) {
    return { success: false, message: 'Gagal: ' + e.message };
  }
}

// ── HELPER: BUAT SHEET ANGGOTA ──
function getOrCreateAnggota() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName(SHEET_ANGGOTA);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_ANGGOTA);
    var h = sheet.getRange(1,1,1,12);
    h.setValues([['Timestamp','Nama','Jenis Kelamin','Tgl Lahir','No STR','No KTA',
                   'Status Kerja','Instansi','Gaji','No HP','Email','Status']]);
    h.setFontWeight('bold').setBackground('#1E3A5F').setFontColor('#fff');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

// ── HELPER: BUAT SHEET IURAN ──
function getOrCreateIuran() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName(SHEET_IURAN);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_IURAN);
    var h = sheet.getRange(1,1,1,6);
    h.setValues([['No KTA','Nama','Tahun Dari','Tahun Sampai','Status Iuran','Diperbarui']]);
    h.setFontWeight('bold').setBackground('#1E3A5F').setFontColor('#fff');
    sheet.setFrozenRows(1);
  }
  return sheet;
}
