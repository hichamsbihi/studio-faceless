<#
Sauvegarde de la chaîne : mode d'emploi

Ce que fait le script :
- copie les dossiers et fichiers de la chaîne (par défaut : episodes, marque, direction, templates, .claude, CLAUDE.md,
  package.json, package-lock.json, requirements.txt ; jamais node_modules) dans un nouveau dossier daté
  « <nom du dossier de la chaîne>_AAAA-MM-JJ_HHMM » sous la destination choisie ;
- vérifie chaque copie par empreinte SHA-256 et écrit MANIFEST.sha256.txt dans ce dossier ;
- ne supprime ni ne remplace rien, à la source comme à la destination ; refuse une destination située dans la chaîne.

Utilisation, depuis la racine de la chaîne (PowerShell 5.1 ou 7) :
  powershell -File ${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1 -Destination E:\Sauvegardes -Simulation   # liste et volume, aucune copie
  powershell -File ${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1 -Destination E:\Sauvegardes               # copie complète (~3,9 Go sur AA)
  powershell -File ${CLAUDE_PLUGIN_ROOT}/outils/sauvegarde-chaine.ps1 -Destination E:\Sauvegardes -Elements marque,direction

Restauration : copier à la main les fichiers voulus depuis le dossier daté ; le manifeste donne leur empreinte.
Quand : après chaque livraison validée, et avant toute mise à jour d'outil (Node, HyperFrames, FFmpeg).
Une destination synchronisée (OneDrive…) envoie les fichiers en ligne : à décider par le propriétaire.
#>
param(
    [Parameter(Mandatory = $true)][string]$Destination,
    [string]$Chaine = (Get-Location).Path,   # dossier de la chaîne (par défaut : le dossier courant)
    [switch]$Simulation,
    [string[]]$Elements = @('episodes', 'marque', 'direction', 'templates', '.claude', 'CLAUDE.md', 'package.json', 'package-lock.json', 'requirements.txt')
)
$ErrorActionPreference = 'Stop'
# -Elements a,b passé par -File arrive en une seule chaîne : on la découpe.
$Elements = @($Elements | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim().Trim("'").Trim('"') } | Where-Object { $_ })
$source = (Resolve-Path -LiteralPath $Chaine).Path
$destFull = [IO.Path]::GetFullPath($Destination)
if ($destFull.TrimEnd('\') -eq $source.TrimEnd('\') -or $destFull.StartsWith($source.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "La destination ne peut pas être dans la chaîne : $destFull"
}

$files = New-Object System.Collections.Generic.List[object]
foreach ($e in $Elements) {
    $p = Join-Path $source $e
    if (-not (Test-Path -LiteralPath $p)) { Write-Warning "Absent, ignoré : $e"; continue }
    if (Test-Path -LiteralPath $p -PathType Leaf) { $files.Add((Get-Item -LiteralPath $p -Force)) }
    else { Get-ChildItem -LiteralPath $p -Recurse -File -Force | Where-Object { $_.FullName -notmatch '\\node_modules\\|\\__pycache__\\' } | ForEach-Object { $files.Add($_) } }
}
$total = ($files | Measure-Object Length -Sum).Sum
if ($files.Count -eq 0) { throw 'Aucun fichier à sauvegarder : vérifier -Elements.' }
'{0} fichiers, {1:N2} Go, depuis {2}' -f $files.Count, ($total / 1GB), $source

if ($Simulation) {
    $files | Group-Object { $_.FullName.Substring($source.Length + 1).Split('\')[0] } |
        ForEach-Object { '  {0,-20} {1,6} fichiers {2,9:N1} Mo' -f $_.Name, $_.Count, (($_.Group | Measure-Object Length -Sum).Sum / 1MB) }
    "Simulation : rien n'a été copié. Destination prévue : $(Join-Path $destFull ((Split-Path $source -Leaf) + '_' + (Get-Date -Format 'yyyy-MM-dd_HHmm')))"
    return
}

$drive = [IO.Path]::GetPathRoot($destFull)
$free = (New-Object System.IO.DriveInfo $drive).AvailableFreeSpace
if ($free -lt $total * 1.05) { throw ('Place insuffisante sur {0} : {1:N2} Go libres pour {2:N2} Go' -f $drive, ($free / 1GB), ($total / 1GB)) }

$target = Join-Path $destFull ((Split-Path $source -Leaf) + '_' + (Get-Date -Format 'yyyy-MM-dd_HHmm'))
if (Test-Path -LiteralPath $target) { throw "Existe déjà : $target" }
New-Item -ItemType Directory -Path $target | Out-Null

$rows = New-Object System.Collections.Generic.List[string]
$i = 0
foreach ($f in $files) {
    $i++
    $rel = $f.FullName.Substring($source.Length + 1)
    $to = Join-Path $target $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $to) | Out-Null
    Copy-Item -LiteralPath $f.FullName -Destination $to
    $h1 = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLower()
    $h2 = (Get-FileHash -LiteralPath $to -Algorithm SHA256).Hash.ToLower()
    if ($h1 -ne $h2) { throw "Copie différente : $rel" }
    $rows.Add("$h1  $($rel.Replace('\', '/'))")
    if ($i % 200 -eq 0) { "  $i / $($files.Count)" }
}
@("# Sauvegarde de la chaîne du $(Get-Date -Format 'yyyy-MM-dd HH:mm') : $($rows.Count) fichiers, SHA-256  chemin") + $rows |
    Set-Content -LiteralPath (Join-Path $target 'MANIFEST.sha256.txt') -Encoding UTF8
"Sauvegarde terminée et vérifiée : $($rows.Count) fichiers dans $target"
