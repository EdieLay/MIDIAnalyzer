param(
    [string]$Python = "python",
    [switch]$StopOnError
)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptRoot

$mainScript = Join-Path $scriptRoot "main.py"
$inputDir = Join-Path $scriptRoot "input"

if (-not (Test-Path -Path $mainScript -PathType Leaf)) {
    Write-Error "main.py was not found in $scriptRoot"
    exit 1
}

if (-not (Test-Path -Path $inputDir -PathType Container)) {
    Write-Error "Input folder was not found: $inputDir"
    exit 1
}

$midFiles = Get-ChildItem -Path $inputDir -Filter "*.mid" -File | Sort-Object Name

if ($midFiles.Count -eq 0) {
    Write-Warning "No .mid files were found in the input folder"
    exit 0
}

foreach ($midFile in $midFiles) {
    Write-Host "Processing: $($midFile.Name)"
    & $Python $mainScript $midFile.FullName

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Error while processing $($midFile.Name). Exit code: $LASTEXITCODE"
        if ($StopOnError) {
            exit $LASTEXITCODE
        }
    }
}

Write-Host "Done. Processing completed."