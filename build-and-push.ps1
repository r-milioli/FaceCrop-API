# Script PowerShell para build e push da imagem Docker para Docker Hub
# Uso: .\build-and-push.ps1 [tag]

param(
    [string]$Tag = "latest"
)

$ImageName = "automacaodebaixocusto/facecrop-api"
$FullImageName = "${ImageName}:${Tag}"

Write-Host "🔨 Building Docker image: $FullImageName" -ForegroundColor Cyan

# Build da imagem
docker build -t $FullImageName .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build concluído!" -ForegroundColor Green
    
    $Push = Read-Host "Deseja fazer push para Docker Hub? (y/n)"
    if ($Push -eq "y" -or $Push -eq "Y") {
        Write-Host "📤 Fazendo push para Docker Hub..." -ForegroundColor Cyan
        docker push $FullImageName
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Push concluído!" -ForegroundColor Green
        } else {
            Write-Host "❌ Erro ao fazer push!" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "⏭️  Push cancelado." -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Erro no build!" -ForegroundColor Red
    exit 1
}

