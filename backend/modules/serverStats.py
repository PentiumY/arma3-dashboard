import psutil

def get_server_stats(pid):
    try:
        p = psutil.Process(pid)
        return {
            "cpu_percent": p.cpu_percent(interval=1),
            "memory_mb": p.memory_info().rss / 1024 / 1024,
            "status": p.status()
        }
    except psutil.NoSuchProcess:
        return {"status": "stopped"}
