const fs = require('fs');
const path = require('path');

[path.join(__dirname, '..', 'web', 'index.html')].forEach(filePath => {
  console.log(`Validating ${filePath}...`);
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Extract all <script> tags
  const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
  let match;
  let scriptIndex = 0;
  
  while ((match = scriptRegex.exec(content)) !== null) {
    scriptIndex++;
    const scriptBody = match[1];
    if (!scriptBody.trim()) continue;
    
    try {
      new Function(scriptBody);
      console.log(`  Script ${scriptIndex}: Syntax OK!`);
    } catch (e) {
      console.error(`  Script ${scriptIndex} Syntax Error: ${e.message}`);
      process.exit(1);
    }
  }
  
  // Check key markers
  const checks = [
    'id="manual-completo"',
    'MANUAL_MARKDOWN_CONTENT',
    'copyManualMarkdown',
    'downloadManualMarkdown',
    'id="tab-schematic"',
    'id="nav-schematic"',
    'id="mobile-nav-schematic"',
    'CODE_MASTER_MEGA_SRC',
    'CODE_SLAVE_NANO_SRC',
    'switchFwView',
    'copyMasterIno',
    'downloadMasterIno',
    'copySlaveIno',
    'downloadSlaveIno',
    'sec-esquematico-master',
    'sec-esquematico-slaves',
    'sec-utp-queda',
    'sec-topologia-predial',
    'sec-layout-quadro',
    'sec-corte-botoes',
    'sec-pinagem',
    'sec-firmwares',
    'sec-montagem',
    'manual-render'
  ];
  
  checks.forEach(chk => {
    if (!content.includes(chk)) {
      console.error(`  Missing required marker: ${chk}`);
      process.exit(1);
    }
  });
  console.log(`  All required markers present in ${filePath}! (Size: ${content.length} bytes)`);
});
console.log('ALL HTML FILES FULLY AUDITED AND VALIDATED!');
