#!/usr/bin/env bash
# Lance un render.sh quand aucun autre rendu HyperFrames ne tourne (toutes sessions) ; outil commun depuis le 24/10/2026 (skill studio-faceless:episode).
# aucun rendu HyperFrames en cours (toutes sessions). Conditions de processeur et de mémoire retirées (validé sur AA, 24/10/2026) :
# elles sont seulement relevées au journal. Sinon, attend et revérifie toutes les 5 min (12 h au plus). Usage : bash rendre_si_libre.sh <render.sh> <journal>
set -u
RS="$1"; LOG="$2"; ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"   # dossier de la chaîne, pas celui du plugin
mesure() {
  powershell -NoProfile -Command "\$v = 1..6 | ForEach-Object { (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter \"Name='_Total'\").PercentProcessorTime; Start-Sleep -Seconds 3 }; \$c = [math]::Round((\$v | Measure-Object -Average).Average); \$r = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1); \$n = @(Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'node.exe' -and \$_.CommandLine -match 'hyperframes.mjs.* render' }).Count; \"\$c \$r \$n\""
}
for i in $(seq 1 144); do
  read -r CPU RAM NREND < <(mesure | tr -d '\r' | sed 's/,/./g')
  echo "$(date +%H:%M:%S) processeur ${CPU} % · RAM libre ${RAM} Go · rendus en cours ${NREND}" >> "$LOG"
  if [ "${NREND:-1}" = "0" ]; then
    echo "$(date +%H:%M:%S) machine libre : lancement de $RS" >> "$LOG"
    cd "$ROOT" && bash "$RS" >> "$LOG" 2>&1
    code=$?; echo "$(date +%H:%M:%S) fin du rendu, code $code" >> "$LOG"; tail -2 "$LOG"; exit $code
  fi
  sleep 300
done
echo "Attente de 12 h dépassée, rien n'a été lancé" | tee -a "$LOG"; exit 3
