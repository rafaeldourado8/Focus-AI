/**
 * VS Code Extension for Cerberus AI
 * 
 * Basic example - Full implementation in future phase
 */

const vscode = require('vscode');
const { CerberusAI } = require('@cerberus-ai/sdk');

let cerberus;

function activate(context) {
  // Initialize Cerberus AI
  const apiKey = vscode.workspace.getConfiguration('cerberus').get('apiKey');
  cerberus = new CerberusAI(apiKey);

  // Command: Explain Code
  let explainCommand = vscode.commands.registerCommand('cerberus.explain', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const selection = editor.document.getText(editor.selection);
    const language = editor.document.languageId;

    const response = await cerberus.chatCompletion([
      { role: 'system', content: 'Explain code clearly and concisely.' },
      { role: 'user', content: `Explain this ${language} code:\n${selection}` }
    ]);

    vscode.window.showInformationMessage(response.choices[0].message.content);
  });

  // Command: Debug Code
  let debugCommand = vscode.commands.registerCommand('cerberus.debug', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const code = editor.document.getText(editor.selection);
    const language = editor.document.languageId;
    const error = await vscode.window.showInputBox({ prompt: 'Enter error message' });

    const response = await cerberus.debugCode(error, code, language);
    
    const panel = vscode.window.createWebviewPanel(
      'cerberusDebug',
      'Cerberus Debug',
      vscode.ViewColumn.Two,
      {}
    );
    panel.webview.html = `<pre>${response.debug_info}</pre>`;
  });

  context.subscriptions.push(explainCommand, debugCommand);
}

function deactivate() {}

module.exports = { activate, deactivate };
