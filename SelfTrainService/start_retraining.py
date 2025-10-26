"""
Start the auto-retraining background service
Retrains models every 48 hours
"""
import sys
from pathlib import Path
import time
import signal

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from SelfTrainService.retraining_service import start_retraining_service
from SelfTrainService.config import CONFIG

# Global flag for graceful shutdown
running = True


def signal_handler(sig, frame):
    """Handle shutdown signals"""
    global running
    print("\n\nReceived shutdown signal. Stopping retraining service...")
    running = False


def main():
    """Start the retraining service"""
    print("=" * 60)
    print("Auto-Retraining Service")
    print("=" * 60)
    print(f"Retrain interval: {CONFIG.RETRAIN_INTERVAL_HOURS} hours")
    print(f"Model types: {', '.join(CONFIG.MODEL_TYPES)}")
    print(f"Ensemble mode: {'Enabled' if CONFIG.USE_ENSEMBLE else 'Disabled'}")
    print("=" * 60)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("\nStarting background retraining service...")
    print("Press Ctrl+C to stop\n")
    
    # Start the service
    start_retraining_service()
    
    # Keep main thread alive
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    
    print("Service stopped.")


if __name__ == "__main__":
    main()
