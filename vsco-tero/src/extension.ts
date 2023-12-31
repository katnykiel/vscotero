import * as vscode from 'vscode';
import * as child_process from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
	let disposable = vscode.commands.registerCommand('vsco-tero.updateLiteratureNotes', () => {
		const pythonScriptPath = path.join(context.extensionPath, './../core.py');
		const pythonInterpreter = vscode.workspace.getConfiguration('python').get('pythonPath') as string;
		child_process.exec(`${pythonInterpreter} ${pythonScriptPath}`, (error, stdout, stderr) => {
			if (error) {
				vscode.window.showErrorMessage(`Error: ${error.message}`);
				return;
			}
			if (stderr) {
				vscode.window.showErrorMessage(`Python Error: ${stderr}`);
				return;
			}
			vscode.window.showInformationMessage(`Python Output: ${stdout}`);
		});
	});

	context.subscriptions.push(disposable);
}