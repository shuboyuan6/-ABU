# -*- coding: utf-8 -*-
"""限制 Ollama CPU 使用量为 50%（8核/16核）— 使用 psutil"""
import psutil, os, sys

TARGET_CORES = 8
MASK = (1 << TARGET_CORES) - 1  # 0x00FF

def main():
    print("=" * 50)
    print(f"  Ollama CPU 限制: {TARGET_CORES}/16 核 = ~50%")
    print("=" * 50)

    # 1. 找 llama* 进程
    llama_procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if 'llama' in p.info['name'].lower():
                mb = p.info['memory_info'].rss // 1024 // 1024
                llama_procs.append((p, mb))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if not llama_procs:
        print("未找到 Ollama 进程，请确认 Ollama 正在运行")
        sys.exit(1)

    print(f"\n发现 {len(llama_procs)} 个 Ollama 进程:")
    for p, mb in sorted(llama_procs, key=lambda x: -x[1]):
        print(f"  PID {p.pid}: {mb} MB")

    # 2. 对最大的推理进程设置亲和性
    target_proc, target_mb = max(llama_procs, key=lambda x: x[1])
    pid = target_proc.pid
    print(f"\n目标进程 PID {pid} ({target_mb} MB)")

    try:
        old_affinity = target_proc.cpu_affinity()
        print(f"当前 CPU 亲和性: {len(old_affinity)} 核 {sorted(old_affinity)}")
    except psutil.AccessDenied as e:
        print(f"无法读取亲和性（需要管理员权限）: {e}")
        sys.exit(1)

    # 3. 设置新的亲和性：只用前 TARGET_CORES 个核心
    new_affinity = list(range(TARGET_CORES))  # [0, 1, 2, ..., 7]
    try:
        target_proc.cpu_affinity(new_affinity)
        print(f"已设置亲和性: {new_affinity}")
    except psutil.AccessDenied as e:
        print(f"\n❌ 设置亲和性失败: {e}")
        print("提示：以管理员身份运行此脚本")
        sys.exit(1)

    # 4. 验证
    verify_affinity = target_proc.cpu_affinity()
    print(f"验证: 现在可用 {len(verify_affinity)} 核 {sorted(verify_affinity)}")

    if len(verify_affinity) == TARGET_CORES:
        print(f"\n✅ 完成！Ollama 推理进程(PID {pid}) CPU 已限制为 50%（{TARGET_CORES}/16 核）")
        print(f"   推理速度会变慢，但 CPU 占用约为原来一半")
        print(f"   ⚠️ 此设置在 Ollama 重启后失效，需重新执行")
    else:
        print(f"\n⚠️ 亲和性设置结果异常（{len(verify_affinity)} 核）")

if __name__ == "__main__":
    main()
