# Rend une page d'un PDF en PNG par le moteur PDF de Windows (Windows.Data.Pdf), sans rien installer.
# Validé sur MM (Maps & Means), 28/10/2026 (épisode 004). Versé au plugin le 30/10/2026. Windows seulement.
# Usage (Windows PowerShell 5.1), depuis la racine de la chaîne : powershell -NoProfile -File ${CLAUDE_PLUGIN_ROOT}/outils/medias/rendre_page_pdf.ps1 PDF PAGE(1..n) DPI DOSSIER NOM
# Attention : le moteur multiplie la taille par l échelle de l écran (1,5 sur le poste de MM) : DPI 200 donne 300 dpi.
# Il ne décode pas le JBIG2 (scans) : pour ceux-là, jbig2_page.py.
param([string]$Pdf, [int]$Page, [double]$Dpi, [string]$Dossier, [string]$Nom)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$methodes = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asTaskOp = ($methodes | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
$asTaskAct = ($methodes | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' })[0]
function Attendre($op, [type]$t) { $k = $asTaskOp.MakeGenericMethod($t).Invoke($null, @($op)); $k.Wait(-1) | Out-Null; $k.Result }
function AttendreAction($a) { $k = $asTaskAct.Invoke($null, @($a)); $k.Wait(-1) | Out-Null }
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFolder, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Pdf.PdfPageRenderOptions, Windows.Data.Pdf, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null

$f = Attendre ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Pdf)) ([Windows.Storage.StorageFile])
$doc = Attendre ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($f)) ([Windows.Data.Pdf.PdfDocument])
$p = $doc.GetPage([uint32]($Page - 1))
# Size est en DIP (1/96 de pouce)
$l = [uint32][math]::Round($p.Size.Width * $Dpi / 96); $h = [uint32][math]::Round($p.Size.Height * $Dpi / 96)
"pages {0} ; page {1} : {2:N1} x {3:N1} DIP -> {4} x {5} px a {6} dpi" -f $doc.PageCount, $Page, $p.Size.Width, $p.Size.Height, $l, $h, $Dpi
$o = New-Object Windows.Data.Pdf.PdfPageRenderOptions
$o.DestinationWidth = $l; $o.DestinationHeight = $h
$d = Attendre ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync($Dossier)) ([Windows.Storage.StorageFolder])
# FailIfExists : jamais d'écrasement
$s = Attendre ($d.CreateFileAsync($Nom, [Windows.Storage.CreationCollisionOption]::FailIfExists)) ([Windows.Storage.StorageFile])
$flux = Attendre ($s.OpenAsync([Windows.Storage.FileAccessMode]::ReadWrite)) ([Windows.Storage.Streams.IRandomAccessStream])
AttendreAction ($p.RenderToStreamAsync($flux, $o))
$flux.Dispose(); $p.Dispose()
"ecrit $Dossier\$Nom"
