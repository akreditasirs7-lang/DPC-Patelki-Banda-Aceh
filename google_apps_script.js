const SCRIPT_PROP = PropertiesService.getScriptProperties();

function setup() {
  const doc = SpreadsheetApp.getActiveSpreadsheet();
  SCRIPT_PROP.setProperty("key", doc.getId());
}

function doGet(e) {
  try {
    const doc = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = doc.getSheets()[0]; 
    const data = sheet.getDataRange().getValues();
    
    if (data.length <= 1) {
      return ContentService
        .createTextOutput(JSON.stringify([]))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const headers = data[0];
    const rows = data.slice(1);
    
    const result = rows.map(row => {
      const obj = {};
      headers.forEach((header, index) => {
        // Map backend ID to a specific column, let's say we use Row index + 1 as __backendId
        obj[header] = row[index];
      });
      // Add row index as ID if not exist
      obj.__backendId = row[0]; // Assuming Id is first column
      return obj;
    });
    
    return ContentService
      .createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch(e) {
    return ContentService
      .createTextOutput(JSON.stringify({ 'error': e.stack }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  try {
    const doc = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = doc.getSheets()[0]; 
    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    
    const action = e.parameter.action; // 'add', 'edit', 'delete'
    const postDataStr = e.postData ? e.postData.contents : '';
    let req;
    
    if (postDataStr) {
      req = JSON.parse(postDataStr);
    } else {
      req = e.parameter;
    }
    
    // Ensure ID column exists, if headers are empty, initialize them
    if (headers.length === 0 || headers[0] === '') {
      const newHeaders = ['id', 'nama', 'nomor_str', 'no_kta', 'status_pekerjaan', 'instansi', 'gaji', 'jenis_kelamin', 'phone', 'email', 'tanggal_lahir'];
      sheet.getRange(1, 1, 1, newHeaders.length).setValues([newHeaders]);
      SpreadsheetApp.flush();
    }
    
    const actualHeaders = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

    if (req.action === 'delete') {
      const idToDelete = req.id;
      const data = sheet.getDataRange().getValues();
      for (let i = 1; i < data.length; i++) {
        if (data[i][0] == idToDelete) { // Assuming col 1 is ID
          sheet.deleteRow(i + 1);
          return ContentService.createTextOutput(JSON.stringify({ "status": "success", "message": "Deleted", "isOk": true })).setMimeType(ContentService.MimeType.JSON);
        }
      }
      return ContentService.createTextOutput(JSON.stringify({ "status": "error", "message": "Not found", "isOk": false })).setMimeType(ContentService.MimeType.JSON);
    }
    
    if (req.action === 'edit') {
      const idToEdit = req.id;
      const data = sheet.getDataRange().getValues();
      for (let i = 1; i < data.length; i++) {
        if (data[i][0] == idToEdit) {
          const rowData = [];
          actualHeaders.forEach(header => {
            if (header === 'id') {
              rowData.push(idToEdit);
            } else {
              rowData.push(req[header] !== undefined ? req[header] : data[i][actualHeaders.indexOf(header)]);
            }
          });
          sheet.getRange(i + 1, 1, 1, rowData.length).setValues([rowData]);
          return ContentService.createTextOutput(JSON.stringify({ "status": "success", "message": "Updated", "isOk": true })).setMimeType(ContentService.MimeType.JSON);
        }
      }
      return ContentService.createTextOutput(JSON.stringify({ "status": "error", "message": "Not found", "isOk": false })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Default action: add
    const newId = Utilities.getUuid();
    const rowData = [];
    actualHeaders.forEach(header => {
      if (header === 'id') {
        rowData.push(newId);
      } else {
        rowData.push(req[header] || '');
      }
    });
    
    sheet.appendRow(rowData);
    
    return ContentService
      .createTextOutput(JSON.stringify({ "status": "success", "id": newId, "isOk": true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch(e) {
    return ContentService
      .createTextOutput(JSON.stringify({ "status": "error", "message": e.stack, "isOk": false }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
