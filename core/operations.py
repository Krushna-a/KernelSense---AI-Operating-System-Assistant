"""
System Operations
Handlers for executing system operations like process management and file operations
"""

import os
import psutil
import glob
from typing import Dict, Any, List, Optional
from pathlib import Path

class SystemOperations:
    """Executes system operations"""
    
    @staticmethod
    def kill_process_by_pid(pid: int) -> Dict[str, Any]:
        """
        Kill a process by PID
        
        Args:
            pid: Process ID to kill
            
        Returns:
            Dictionary with 'success', 'message'
        """
        try:
            proc = psutil.Process(pid)
            process_name = proc.name()
            
            # Attempt to terminate gracefully first
            proc.terminate()
            
            # Wait for process to terminate (max 3 seconds)
            try:
                proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                # Force kill if terminate didn't work
                proc.kill()
            
            return {
                'success': True,
                'message': f"✓ Process '{process_name}' (PID {pid}) has been stopped."
            }
        except psutil.NoSuchProcess:
            return {
                'success': False,
                'message': f"❌ Process with PID {pid} not found."
            }
        except psutil.AccessDenied:
            return {
                'success': False,
                'message': f"❌ Access denied. You may need administrator privileges to stop this process."
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Failed to stop process: {str(e)}"
            }
    
    @staticmethod
    def kill_process_by_name(name: str) -> Dict[str, Any]:
        """
        Kill processes by name
        
        Args:
            name: Process name to kill
            
        Returns:
            Dictionary with 'success', 'message', 'killed_pids'
        """
        killed_pids = []
        errors = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == name.lower() or \
                       name.lower() in proc.info['name'].lower():
                        pid = proc.info['pid']
                        
                        # Kill the process
                        proc.terminate()
                        try:
                            proc.wait(timeout=3)
                        except psutil.TimeoutExpired:
                            proc.kill()
                        
                        killed_pids.append(pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    errors.append(f"PID {proc.info['pid']}: {str(e)}")
                    continue
            
            if killed_pids:
                message = f"✓ Stopped {len(killed_pids)} process(es) matching '{name}': PIDs {killed_pids}"
                if errors:
                    message += f"\n⚠️ Some processes could not be stopped: {', '.join(errors)}"
                return {
                    'success': True,
                    'message': message,
                    'killed_pids': killed_pids
                }
            else:
                return {
                    'success': False,
                    'message': f"❌ No processes found matching '{name}'.",
                    'killed_pids': []
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Failed to stop processes: {str(e)}",
                'killed_pids': killed_pids
            }
    
    @staticmethod
    def find_files(pattern: str, search_path: str = None, file_type: str = None, limit: int = 50) -> Dict[str, Any]:
        """
        Find files matching a pattern
        
        Args:
            pattern: File pattern to search for
            search_path: Directory to search in (defaults to current directory)
            file_type: File extension to filter by
            limit: Maximum number of results
            
        Returns:
            Dictionary with 'success', 'message', 'files'
        """
        try:
            if search_path is None:
                search_path = os.getcwd()
            
            search_path = Path(search_path)
            
            if not search_path.exists():
                return {
                    'success': False,
                    'message': f"❌ Search path does not exist: {search_path}",
                    'files': []
                }
            
            # Build search pattern
            if file_type:
                if not file_type.startswith('.'):
                    file_type = f'.{file_type}'
                search_pattern = f"**/*{file_type}"
            elif pattern:
                search_pattern = f"**/*{pattern}*"
            else:
                search_pattern = "**/*"
            
            # Search for files
            found_files = []
            for file_path in search_path.glob(search_pattern):
                if file_path.is_file():
                    found_files.append({
                        'path': str(file_path),
                        'name': file_path.name,
                        'size_bytes': file_path.stat().st_size,
                        'size_mb': round(file_path.stat().st_size / (1024**2), 2)
                    })
                    
                    if len(found_files) >= limit:
                        break
            
            if found_files:
                message = f"Found {len(found_files)} file(s):\n\n"
                for f in found_files[:20]:  # Show first 20
                    message += f"  • {f['name']} ({f['size_mb']} MB)\n    {f['path']}\n"
                
                if len(found_files) > 20:
                    message += f"\n  ... and {len(found_files) - 20} more files"
                
                return {
                    'success': True,
                    'message': message.strip(),
                    'files': found_files
                }
            else:
                return {
                    'success': False,
                    'message': f"❌ No files found matching the criteria.",
                    'files': []
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Error searching for files: {str(e)}",
                'files': []
            }
    
    @staticmethod
    def delete_file(path: str) -> Dict[str, Any]:
        """
        Delete a file
        
        Args:
            path: Path to the file to delete
            
        Returns:
            Dictionary with 'success', 'message'
        """
        try:
            file_path = Path(path)
            
            if not file_path.exists():
                return {
                    'success': False,
                    'message': f"❌ File not found: {path}"
                }
            
            if not file_path.is_file():
                return {
                    'success': False,
                    'message': f"❌ Path is not a file: {path}"
                }
            
            # Get file info before deletion
            size_mb = round(file_path.stat().st_size / (1024**2), 2)
            
            # Delete the file
            file_path.unlink()
            
            return {
                'success': True,
                'message': f"✓ File deleted: {path} ({size_mb} MB)"
            }
        except PermissionError:
            return {
                'success': False,
                'message': f"❌ Permission denied. You may need administrator privileges to delete this file."
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Failed to delete file: {str(e)}"
            }
    
    @staticmethod
    def get_startup_apps() -> Dict[str, Any]:
        """
        Get list of startup applications (Windows)
        
        Returns:
            Dictionary with 'success', 'message', 'apps'
        """
        try:
            import platform
            
            if platform.system() != 'Windows':
                return {
                    'success': False,
                    'message': "❌ This feature is currently only supported on Windows.",
                    'apps': []
                }
            
            startup_apps = []
            
            # Check common startup locations
            startup_paths = [
                os.path.join(os.environ.get('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs\Startup'),
                os.path.join(os.environ.get('PROGRAMDATA', ''), r'Microsoft\Windows\Start Menu\Programs\Startup')
            ]
            
            for startup_path in startup_paths:
                if os.path.exists(startup_path):
                    for item in os.listdir(startup_path):
                        item_path = os.path.join(startup_path, item)
                        if os.path.isfile(item_path):
                            startup_apps.append({
                                'name': item,
                                'path': item_path,
                                'location': 'Startup Folder'
                            })
            
            if startup_apps:
                message = f"Found {len(startup_apps)} startup application(s):\n\n"
                for app in startup_apps:
                    message += f"  • {app['name']}\n    {app['path']}\n"
                
                return {
                    'success': True,
                    'message': message.strip(),
                    'apps': startup_apps
                }
            else:
                return {
                    'success': True,
                    'message': "No startup applications found in common locations.",
                    'apps': []
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Error retrieving startup apps: {str(e)}",
                'apps': []
            }
    
    @staticmethod
    def search_file_content(pattern: str, search_path: str = None, file_type: str = None) -> Dict[str, Any]:
        """
        Search for content within files
        
        Args:
            pattern: Text pattern to search for
            search_path: Directory to search in
            file_type: File extension to filter by
            
        Returns:
            Dictionary with 'success', 'message', 'results'
        """
        try:
            if search_path is None:
                search_path = os.getcwd()
            
            search_path = Path(search_path)
            
            if not search_path.exists():
                return {
                    'success': False,
                    'message': f"❌ Search path does not exist: {search_path}",
                    'results': []
                }
            
            results = []
            files_searched = 0
            max_files = 100  # Limit to prevent excessive searching
            
            # Build file pattern
            if file_type:
                if not file_type.startswith('.'):
                    file_type = f'.{file_type}'
                file_pattern = f"**/*{file_type}"
            else:
                file_pattern = "**/*.txt"  # Default to text files
            
            # Search files
            for file_path in search_path.glob(file_pattern):
                if files_searched >= max_files:
                    break
                
                if file_path.is_file():
                    files_searched += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if pattern.lower() in line.lower():
                                    results.append({
                                        'file': str(file_path),
                                        'line': line_num,
                                        'content': line.strip()
                                    })
                                    
                                    if len(results) >= 50:  # Limit results
                                        break
                    except Exception:
                        # Skip files that can't be read
                        continue
            
            if results:
                message = f"Found {len(results)} match(es) in {files_searched} file(s):\n\n"
                for result in results[:20]:  # Show first 20
                    message += f"  • {result['file']}:{result['line']}\n    {result['content'][:100]}\n"
                
                if len(results) > 20:
                    message += f"\n  ... and {len(results) - 20} more matches"
                
                return {
                    'success': True,
                    'message': message.strip(),
                    'results': results
                }
            else:
                return {
                    'success': False,
                    'message': f"❌ No matches found for '{pattern}' in {files_searched} files.",
                    'results': []
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Error searching file content: {str(e)}",
                'results': []
            }
