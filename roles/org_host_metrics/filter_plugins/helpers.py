class FilterModule(object):

  def filters(self):
    return { 
      "analyze" : self.do_analysis,
      "listify": self.do_listify
    }
  
  def do_listify(self, data) -> list:
    if isinstance(data, list):
      return data
    return [data]
  
  def do_analysis(self, hosts: list, org: dict) -> dict:
    report = { 
      "name": org["name"],
      "id": org["id"],
      "organization": self.__setup_metrics(),
      "inventories": {}
    }

    hostnames = set()
    for host in hosts:
      inventory_name = host["summary_fields"]["inventory"]["name"]
      inventory_metrics = report["inventories"].get(inventory_name, self.__setup_metrics())
      report["inventories"][inventory_name] = self.__add_host_metrics(inventory_metrics, host)

      host_name = host["name"]
      if host_name not in hostnames:
        report["organization"] = self.__add_host_metrics(report["organization"], host)
        hostnames.add(host_name)
    
    return report
  
  @staticmethod
  def __setup_metrics() -> dict:
    return {
      "hosts_imported": 0,
      "hosts_automated": 0,
      "hosts_with_failures": 0,
      "hosts_disabled": 0
    }
  
  @staticmethod
  def __add_host_metrics(metrics: dict, host: dict) -> dict:
      automated = host["last_job"] != None
      failures = host["has_active_failures"]
      disabled = not host["enabled"]

      metrics["hosts_imported"] += 1
      if automated:
        metrics["hosts_automated"] += 1
      if failures:
        metrics["hosts_with_failures"] += 1
      if disabled:
        metrics["hosts_disabled"] += 1

      return metrics