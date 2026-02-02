param(
	[string]$ruta_env = ".env"
)

$ErrorActionPreference = "Stop"

function Importar-VariablesDesdeEnv([string]$ruta) {
	if (-not (Test-Path $ruta)) {
		throw "No se encontró el archivo: $ruta. Crea .env a partir de .env.example."
	}

	Get-Content $ruta -Encoding UTF8 |
		Where-Object { $_ -and (-not $_.Trim().StartsWith('#')) } |
		ForEach-Object {
			$linea = $_
			$partes = $linea -split '=', 2
			if ($partes.Count -ne 2) { return }
			$nombre = $partes[0].Trim()
			$valor = $partes[1].Trim()
			# Quitar comillas envolventes si existen: KEY="valor" o KEY='valor'
			if (($valor.StartsWith('"') -and $valor.EndsWith('"')) -or ($valor.StartsWith("'") -and $valor.EndsWith("'"))) {
				$valor = $valor.Substring(1, $valor.Length - 2)
			}
			[Environment]::SetEnvironmentVariable($nombre, $valor, 'Process')
		}
}

# Ubicarse en la raíz del proyecto (carpeta del script -> ..)
$ruta_raiz = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $ruta_raiz

# Activar entorno virtual si existe
if (Test-Path ".venv\Scripts\Activate.ps1") {
	. .\.venv\Scripts\Activate.ps1
}

Importar-VariablesDesdeEnv $ruta_env

Write-Host "Variables cargadas en el proceso actual. Ejecutando app.py..." -ForegroundColor Green
python app.py
