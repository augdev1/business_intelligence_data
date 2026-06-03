# Script de automação para iniciar o Sistema de Análise Olist E-Commerce
# Este script executa todos os passos manuais necessários

Write-Host '=== Sistema de Análise Olist E-Commerce ===' -ForegroundColor Cyan
Write-Host ''

# 1. Verificar se .env existe, se não, criar a partir de .env.example
Write-Host '[1/5] Configurando variáveis de ambiente...' -ForegroundColor Yellow
if (-not (Test-Path '.env')) {
    Write-Host 'Criando .env a partir de .env.example...' -ForegroundColor Green
    Copy-Item '.env.example' '.env'
    Write-Host '⚠️  ATENÇÃO: Edite o arquivo .env com suas configurações reais!' -ForegroundColor Red
    Write-Host '   - DATABASE_URL (PostgreSQL)' -ForegroundColor Red
    Write-Host '   - GROQ_API_KEY ou OPENAI_API_KEY' -ForegroundColor Red
    Write-Host ''
    Write-Host 'Pressione qualquer tecla para continuar após editar o .env...' -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
} else {
    Write-Host '✓ Arquivo .env já existe' -ForegroundColor Green
}
Write-Host ''

# 2. Verificar se PostgreSQL está rodando
Write-Host '[2/5] Verificando PostgreSQL...' -ForegroundColor Yellow
$dockerRunning = docker ps 2>$null | Select-String 'vendas_db'
if ($dockerRunning) {
    Write-Host '✓ PostgreSQL Docker container está rodando' -ForegroundColor Green
} else {
    Write-Host 'Iniciando PostgreSQL via Docker...' -ForegroundColor Green
    docker-compose -f docker/docker-compose.yml up -d db
    Write-Host 'Aguardando PostgreSQL iniciar...' -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}
Write-Host ''

# 3. Carregar dataset Olist
Write-Host '[3/5] Carregando dataset Olist...' -ForegroundColor Yellow
Write-Host 'Este processo pode levar alguns minutos...' -ForegroundColor Yellow
python scripts/carregar_olist.py
if ($LASTEXITCODE -eq 0) {
    Write-Host '✓ Dataset carregado com sucesso' -ForegroundColor Green
} else {
    Write-Host '⚠️  Erro ao carregar dataset. Verifique a configuração do banco.' -ForegroundColor Red
    Write-Host 'Pressione qualquer tecla para continuar mesmo assim...' -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}
Write-Host ''

# 4. Iniciar Backend
Write-Host '[4/5] Iniciando Backend API...' -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
} -ArgumentList (Get-Location)

Write-Host '✓ Backend iniciado em background' -ForegroundColor Green
Write-Host '   API: http://localhost:8000' -ForegroundColor Cyan
Write-Host '   Docs: http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host ''

# 5. Iniciar Frontend
Write-Host '[5/5] Iniciando Frontend Dashboard...' -ForegroundColor Yellow
Write-Host '✓ Frontend iniciado' -ForegroundColor Green
Write-Host '   Dashboard: http://localhost:8501' -ForegroundColor Cyan
Write-Host ''

Write-Host '=== Sistema Iniciado com Sucesso ===' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Para parar o sistema:' -ForegroundColor Yellow
Write-Host '1. Pressione Ctrl+C neste terminal para parar o frontend' -ForegroundColor White
Write-Host '2. Execute: Stop-Job -Id $backendJob.Id para parar o backend' -ForegroundColor White
Write-Host '3. Execute: docker-compose -f docker/docker-compose.yml down para parar o PostgreSQL' -ForegroundColor White
Write-Host ''

# Iniciar frontend em foreground
streamlit run frontend/app.py

# Limpar backend job quando frontend for fechado
Stop-Job -Id $backendJob.Id
Remove-Job -Id $backendJob.Id
