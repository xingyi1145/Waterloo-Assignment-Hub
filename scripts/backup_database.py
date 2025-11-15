"""
Database backup and restore utilities
"""
import sys
import shutil
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

DB_PATH = Path(__file__).parent.parent / "wcah.db"
BACKUP_DIR = Path(__file__).parent.parent / "backups"


def backup_database():
    """Create a timestamped backup of the database"""
    BACKUP_DIR.mkdir(exist_ok=True)
    
    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"wcah_backup_{timestamp}.db"
    
    print(f"💾 Creating backup...")
    shutil.copy2(DB_PATH, backup_path)
    
    # Get file size
    size_mb = backup_path.stat().st_size / (1024 * 1024)
    
    print(f"✅ Backup created: {backup_path.name}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   Location: {backup_path}")


def list_backups():
    """List all available backups"""
    if not BACKUP_DIR.exists():
        print("📂 No backups directory found")
        return []
    
    backups = sorted(BACKUP_DIR.glob("wcah_backup_*.db"), reverse=True)
    
    if not backups:
        print("📂 No backups found")
        return []
    
    print(f"\n💾 Available Backups ({len(backups)})")
    print("-" * 60)
    
    for i, backup in enumerate(backups, 1):
        size_mb = backup.stat().st_size / (1024 * 1024)
        timestamp = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"  [{i}] {backup.name}")
        print(f"      Created: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      Size: {size_mb:.2f} MB")
    
    return backups


def restore_database(backup_path: Path):
    """Restore database from a backup"""
    if not backup_path.exists():
        print(f"❌ Backup not found: {backup_path}")
        return
    
    # Create a backup of current database before restoring
    if DB_PATH.exists():
        print("⚠️  Creating backup of current database before restore...")
        backup_database()
    
    print(f"🔄 Restoring from: {backup_path.name}")
    shutil.copy2(backup_path, DB_PATH)
    print("✅ Database restored successfully")


def main():
    """Main backup/restore function"""
    print("\n💾 Database Backup & Restore Utility")
    print("=" * 60)
    print("1. Create backup")
    print("2. List backups")
    print("3. Restore from backup")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            backup_database()
        
        elif choice == "2":
            list_backups()
        
        elif choice == "3":
            backups = list_backups()
            if not backups:
                continue
            
            try:
                idx = int(input("\nEnter backup number to restore: ")) - 1
                if 0 <= idx < len(backups):
                    confirm = input(f"⚠️  Restore from {backups[idx].name}? (yes/no): ")
                    if confirm.lower() == 'yes':
                        restore_database(backups[idx])
                else:
                    print("❌ Invalid backup number")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == "4":
            print("👋 Goodbye!\n")
            break
        
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
