"""
System Information Collector
Gathers CPU, RAM, disk, process, and network information
"""

import psutil
import platform
from datetime import datetime
from typing import Dict, List, Any

class SystemInfoCollector:
    """Collects comprehensive system information"""
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get CPU usage and information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        per_cpu = psutil.cpu_percent(interval=1, percpu=True)
        
        return {
            'overall_usage': cpu_percent,
            'cpu_count': cpu_count,
            'physical_cores': psutil.cpu_count(logical=False),
            'frequency_mhz': cpu_freq.current if cpu_freq else None,
            'per_cpu_usage': per_cpu,
            'status': 'HIGH' if cpu_percent > 80 else 'NORMAL' if cpu_percent > 50 else 'LOW'
        }
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get RAM usage information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': round(mem.total / (1024**3), 2),
            'available_gb': round(mem.available / (1024**3), 2),
            'used_gb': round(mem.used / (1024**3), 2),
            'percent_used': mem.percent,
            'swap_total_gb': round(swap.total / (1024**3), 2),
            'swap_used_gb': round(swap.used / (1024**3), 2),
            'swap_percent': swap.percent,
            'status': 'CRITICAL' if mem.percent > 90 else 'HIGH' if mem.percent > 75 else 'NORMAL'
        }
    
    @staticmethod
    def get_disk_info() -> Dict[str, Any]:
        """Get disk usage information"""
        partitions = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'percent_used': usage.percent,
                    'status': 'CRITICAL' if usage.percent > 90 else 'HIGH' if usage.percent > 80 else 'NORMAL'
                })
            except PermissionError:
                # Skip partitions we can't access
                continue
        
        return {
            'partitions': partitions,
            'io_counters': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
        }
    
    @staticmethod
    def get_process_list(sort_by='memory', limit=10) -> List[Dict[str, Any]]:
        """Get list of running processes sorted by resource usage"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'memory_info', 'status']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'username': pinfo['username'],
                    'cpu_percent': pinfo['cpu_percent'],
                    'memory_percent': round(pinfo['memory_percent'], 2),
                    'memory_mb': round(pinfo['memory_info'].rss / (1024**2), 2) if pinfo['memory_info'] else 0,
                    'status': pinfo['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort by specified criterion
        if sort_by == 'memory':
            processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        elif sort_by == 'cpu':
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        return processes[:limit]
    
    @staticmethod
    def get_specific_process(pid: int) -> Dict[str, Any]:
        """Get detailed information about a specific process"""
        try:
            proc = psutil.Process(pid)
            
            return {
                'pid': proc.pid,
                'name': proc.name(),
                'exe': proc.exe(),
                'cwd': proc.cwd(),
                'status': proc.status(),
                'username': proc.username(),
                'create_time': datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
                'cpu_percent': proc.cpu_percent(interval=0.1),
                'memory_percent': round(proc.memory_percent(), 2),
                'memory_mb': round(proc.memory_info().rss / (1024**2), 2),
                'num_threads': proc.num_threads(),
                'cmdline': ' '.join(proc.cmdline()) if proc.cmdline() else None
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        """Get network usage information"""
        net_io = psutil.net_io_counters()
        connections = len(psutil.net_connections())
        
        return {
            'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
            'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2),
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout,
            'active_connections': connections
        }
    
    @staticmethod
    def get_system_overview() -> Dict[str, Any]:
        """Get overall system overview"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'hostname': platform.node(),
            'processor': platform.processor(),
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
            'uptime_hours': round(uptime.total_seconds() / 3600, 2)
        }
    
    @staticmethod
    def diagnose_slowness() -> Dict[str, Any]:
        """Diagnose potential causes of system slowness"""
        issues = []
        
        # Check CPU
        cpu_info = SystemInfoCollector.get_cpu_info()
        if cpu_info['overall_usage'] > 80:
            issues.append({
                'category': 'CPU',
                'severity': 'HIGH',
                'message': f"CPU usage is very high ({cpu_info['overall_usage']}%)"
            })
        
        # Check Memory
        mem_info = SystemInfoCollector.get_memory_info()
        if mem_info['percent_used'] > 85:
            issues.append({
                'category': 'MEMORY',
                'severity': 'CRITICAL' if mem_info['percent_used'] > 95 else 'HIGH',
                'message': f"RAM usage is very high ({mem_info['percent_used']}%). Using {mem_info['used_gb']} GB of {mem_info['total_gb']} GB"
            })
        
        # Check top memory consumers
        top_procs = SystemInfoCollector.get_process_list(sort_by='memory', limit=3)
        if top_procs:
            top_consumer = top_procs[0]
            if top_consumer['memory_mb'] > 1000:  # More than 1GB
                issues.append({
                    'category': 'PROCESS',
                    'severity': 'MEDIUM',
                    'message': f"Process '{top_consumer['name']}' (PID {top_consumer['pid']}) is using {top_consumer['memory_mb']} MB of memory"
                })
        
        # Check Disk
        disk_info = SystemInfoCollector.get_disk_info()
        for partition in disk_info['partitions']:
            if partition['percent_used'] > 90:
                issues.append({
                    'category': 'DISK',
                    'severity': 'HIGH',
                    'message': f"Disk {partition['mountpoint']} is {partition['percent_used']}% full ({partition['free_gb']} GB free)"
                })
        
        return {
            'issues': issues,
            'overall_status': 'CRITICAL' if any(i['severity'] == 'CRITICAL' for i in issues) else 'WARNING' if issues else 'HEALTHY'
        }
