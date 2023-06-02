export function formatMonitors(monitorData, httpRecordData) {
  // Join http records and monitors together
  monitorData.map((monitor) => {
    monitor.http_records = httpRecordData.filter(
      (record) => record.monitor_id == monitor.id
    );
  });
  // Calculate monitors current state based on its http_records
  return monitorData.map((monitor) => {
    if (monitor.http_records.length > 0) {
      if (
        monitor.http_records[monitor.http_records.length - 1].success == false
      ) {
        // Get last record and check if it failed
        monitor.current_state = "red";
      } else if (
        // Get last 10 records
        monitor.http_records
          .slice(Math.max(monitor.http_records.length - 10, 0))
          .some((record) => record.success == false)
      ) {
        // Check if any of the records are failed
        monitor.current_state = "yellow";
      } else {
        monitor.current_state = "green";
      }
    } else {
      // If there are no records show gray
      monitor.current_state = "gray";
    }
    return monitor;
  });
}
