# build.ps1 - 跨平台构建脚本

# 检查并安装 uv
function Install-Uv {
    if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "uv is not installed. Installing uv..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri https://astral.sh/uv/0.6.12/install.sh -OutFile install.sh
        bash install.sh  # 需要 Git Bash 或 WSL
        $env:PATH += ";$HOME/.local/bin"
    }
}

# 安装依赖
function Install {
    Install-Uv
    uv sync --frozen
    npm --prefix frontend install
}

# 开发模式
function Dev {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "uv run adk api_server app --allow_origins=*"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm --prefix frontend run dev"
}

# 后端开发
function DevBackend {
    uv run adk api_server app --allow_origins="*"
}

# 前端开发
function DevFrontend {
    npm --prefix frontend run dev
}

# 运行 playground
function Playground {
    uv run adk web --port 8501
}

# 代码检查
function Lint {
    uv run codespell
    uv run ruff check . --diff
    uv run ruff format . --check --diff
    uv run mypy .
}

# 主入口点
param (
    [Parameter(Position=0)]
    [ValidateSet("install", "dev", "dev-backend", "dev-frontend", "playground", "lint")]
    [string]$Task = "install"
)

switch ($Task) {
    "install" { Install }
    "dev" { Dev }
    "dev-backend" { DevBackend }
    "dev-frontend" { DevFrontend }
    "playground" { Playground }
    "lint" { Lint }
    default { Write-Host "未知任务: $Task" -ForegroundColor Red }
}