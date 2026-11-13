"""CLI for agent-memory-leak-valgrind-profiler."""
import sys
import argparse
from .profiler import MemoryLeakProfiler

def main():
    parser = argparse.ArgumentParser(description="Agent Memory Leak Valgrind Profiler CLI")
    parser.add_argument("--demo", action="store_true", help="Run memory leak profiling demo")
    args = parser.parse_args()

    if args.demo:
        profiler = MemoryLeakProfiler(leak_threshold_bytes=1000)
        profiler.start()
        leaky_cache = []
        for i in range(500):
            leaky_cache.append(f"leak_payload_{i}" * 10)
        rep = profiler.stop_and_evaluate()
        print(f"[+] Profiler completed: is_leaking={rep.is_leaking}, growth={rep.growth_bytes}B")
        print(f"[+] Top offender: {rep.top_offender}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
