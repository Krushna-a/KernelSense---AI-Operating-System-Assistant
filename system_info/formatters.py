"""
Formatters for system information
Converts raw data into human-readable strings
"""

from typing import Dict, Any, List

class SystemInfoFormatter:
    """Formats system information for display"""
    
    @staticmethod
    def format_cpu_info(cpu_info: Dict[str, Any]) -> str:
        """Format CPU information"""
        output = []
        output.append(f"CPU Usage: {cpu_info['overall_usage']}% [{cpu_info['status']}]")
        output.append(f"CPU Cores: {cpu_info['cpu_count']} ({cpu_info['physical_cores']} physical)")
        if cpu_info['frequency_mhz']:
            output.append(f"Frequency: {cpu_info['frequency_mhz']:.2f} MHz")
        
        return "\n".join(output)
    
    @staticmethod
    def format_memory_info(mem_info: Dict[str, Any]) -> str:
        """Format memory information"""
        output = []
        output.append(f"RAM: {mem_info['used_gb']} GB / {mem_info['total_gb']} GB ({mem_info['percent_used']}%) [{mem_info['status']}]")
        output.append(f"Available: {mem_info['available_gb']} GB")
        
        if mem_info['swap_total_gb'] > 0:
            output.append(f"Swap: {mem_info['swap_used_gb']} GB / {mem_info['swap_total_gb']} GB ({mem_info['swap_percent']}%)")
        
        return "\n".join(output)
    
    @staticmethod
    def format_disk_info(disk_info: Dict[str, Any]) -> str:
        """Format disk information"""
        output = []
        
        for partition in disk_info['partitions']:
            status_indicator = "⚠️" if partition['status'] != 'NORMAL' else "✓"
            output.append(
                f"{status_indicator} {partition['mountpoint']} ({partition['fstype']}): "
                f"{partition['used_gb']} GB / {partition['total_gb']} GB "
                f"({partition['percent_used']}% used, {partition['free_gb']} GB free)"
            )
        
        return "\n".join(output)
    
    @staticmethod
    def format_process_list(processes: List[Dict[str, Any]]) -> str:
        """Format process list"""
        if not processes:
            return "No processes found."
        
        output = []
        output.append(f"{'PID':<8} {'Name':<30} {'CPU %':<8} {'Memory MB':<12} {'Memory %':<10} {'Status':<10}")
        output.append("-" * 90)
        
        for proc in processes:
            output.append(
                f"{proc['pid']:<8} "
                f"{proc['name'][:29]:<30} "
                f"{proc['cpu_percent'] or 0:<8.1f} "
                f"{proc['memory_mb']:<12.2f} "
                f"{proc['memory_percent']:<10.2f} "
                f"{proc['status']:<10}"
            )
        
        return "\n".join(output)
    
    @staticmethod
    def format_network_info(net_info: Dict[str, Any]) -> str:
        """Format network information"""
        output = []
        output.append(f"Sent: {net_info['bytes_sent_mb']} MB ({net_info['packets_sent']} packets)")
        output.append(f"Received: {net_info['bytes_recv_mb']} MB ({net_info['packets_recv']} packets)")
        output.append(f"Active Connections: {net_info['active_connections']}")
        
        if net_info['errors_in'] > 0 or net_info['errors_out'] > 0:
            output.append(f"⚠️ Errors: {net_info['errors_in']} in, {net_info['errors_out']} out")
        
        return "\n".join(output)
    
    @staticmethod
    def format_system_overview(overview: Dict[str, Any]) -> str:
        """Format system overview"""
        output = []
        output.append(f"Platform: {overview['platform']} {overview['platform_release']}")
        output.append(f"Architecture: {overview['architecture']}")
        output.append(f"Hostname: {overview['hostname']}")
        output.append(f"Processor: {overview['processor']}")
        output.append(f"Boot Time: {overview['boot_time']}")
        output.append(f"Uptime: {overview['uptime_hours']} hours")
        
        return "\n".join(output)
    
    @staticmethod
    def format_diagnosis(diagnosis: Dict[str, Any]) -> str:
        """Format system diagnosis"""
        output = []
        
        if diagnosis['overall_status'] == 'HEALTHY':
            output.append("✓ System appears to be running normally.")
            return "\n".join(output)
        
        output.append(f"System Status: {diagnosis['overall_status']}")
        output.append("\nIssues Found:")
        
        for issue in diagnosis['issues']:
            severity_icon = "🔴" if issue['severity'] == 'CRITICAL' else "🟠" if issue['severity'] == 'HIGH' else "🟡"
            output.append(f"{severity_icon} [{issue['category']}] {issue['message']}")
        
        return "\n".join(output)
