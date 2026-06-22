# set_affinity.ps1 - 设置 Ollama CPU 亲和性为 50%（8/16核）
$ErrorActionPreference = "Continue"

Write-Output "=================================================="
Write-Output "  Ollama CPU 亲和性限制脚本"
Write-Output "=================================================="

# 找最大的 llama 进程
$proc = Get-Process -Name llama* -ErrorAction SilentlyContinue |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 1

if (-not $proc) {
    Write-Output "未找到 Ollama 进程"
    exit 1
}

$pid = $proc.Id
$ws = [math]::Round($proc.WorkingSet64 / 1MB, 0)
Write-Output "目标进程: PID=$pid WS=${ws}MB"

# 读取当前亲和性
try {
    $old_aff = $proc.ProcessorAffinity
    $cores_old = (${env:Number_of_Processors})  # 16
    Write-Output "当前亲和性: $old_aff"
} catch {
    Write-Output "无法读取亲和性: $_"
    exit 1
}

# 设置亲和性：MASK=255 表示只用核心 0-7
# 255 = 0b0000000011111111
$AffinityMask = 255

try {
    $proc.ProcessorAffinity = $AffinityMask
    $new_aff = $proc.ProcessorAffinity
    $cores_new = (${new_aff}.ToString()).Split(',').Count
    Write-Output "已设置: $new_aff"
    Write-Output ""
    Write-Output "✅ 成功！Ollama CPU 已限制为 50%（8/16核）"
    Write-Output "⚠️ 此设置在 Ollama 重启后失效"
} catch {
    Write-Output "❌ 设置失败: $_"
    Write-Output ""
    Write-Output "可能原因：需要管理员权限"
    Write-Output "解决方案：右键 PowerShell → 以管理员身份运行 → 重新执行此脚本"
    exit 1
}
