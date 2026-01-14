from hwmon.processor_ram.usage import (
    get_cpu_usage_percent,
    get_mem_usage,
)


def main():
    print("CPU Usage:")
    print(f"  {get_cpu_usage_percent()} %")

    print("\nMemory Usage:")
    mem = get_mem_usage()
    print(
        f"  Used: {mem['used_mb']} MB / {mem['total_mb']} MB "
        f"({mem['percent_used']}%)"
    )


if __name__ == "__main__":
    main()
