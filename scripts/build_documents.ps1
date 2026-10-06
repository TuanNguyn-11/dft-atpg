param([string]$TexBin = '')

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$xelatex = if ($TexBin) { Join-Path $TexBin 'xelatex.exe' } else { 'xelatex' }
$biber = if ($TexBin) { Join-Path $TexBin 'biber.exe' } else { 'biber' }

function Invoke-Checked([string]$Program, [string[]]$Arguments) {
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Program failed with exit code $LASTEXITCODE"
    }
}

# Biên dịch đủ lượt; dừng nếu công cụ hoặc tham chiếu có lỗi.
foreach ($document in @('report', 'slides')) {
    Push-Location (Join-Path $repoRoot $document)
    try {
        $texArgs = @('-interaction=nonstopmode', '-halt-on-error', 'main.tex')
        Invoke-Checked $xelatex $texArgs
        if ($document -eq 'report') { Invoke-Checked $biber @('main') }
        Invoke-Checked $xelatex $texArgs
        Invoke-Checked $xelatex $texArgs
        $issues = Select-String -Path 'main.log' -Pattern 'undefined|Please \(re\)run Biber|Missing character:|Overfull \\[hv]box'
        if ($issues) { throw ($issues -join [Environment]::NewLine) }
        $artifact = if ($document -eq 'report') { 'bao_cao_DFT_ATPG.pdf' } else { 'slides_DFT_ATPG.pdf' }
        Copy-Item -LiteralPath 'main.pdf' -Destination $artifact -Force
        Write-Output "PASS: $document/$artifact"
    }
    finally { Pop-Location }
}
