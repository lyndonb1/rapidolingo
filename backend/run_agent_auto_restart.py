"""
Auto-restart wrapper for LiveKit agent worker
Restarts the worker automatically if it crashes
"""
import subprocess
import time
import sys

def main():
    print("=" * 60)
    print("🔄 RápidoLingo Agent Worker with Auto-Restart")
    print("=" * 60)
    print("Worker will automatically restart if it crashes")
    print("Press Ctrl+C to stop\n")
    
    restart_count = 0
    
    while True:
        try:
            print(f"\n🚀 Starting worker (restart #{restart_count})...")
            
            # Run the worker
            process = subprocess.run(
                [sys.executable, "working_agent.py"],
                cwd=".",
            )
            
            # If we get here, the worker exited
            restart_count += 1
            print(f"\n⚠️ Worker exited with code {process.returncode}")
            print("Restarting in 2 seconds...")
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n\n👋 Stopping agent worker...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()
