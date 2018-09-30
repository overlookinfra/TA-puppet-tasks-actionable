
[puppet_task_exec]
param.environment = <string> Environment. It's a required parameter. It's default value is production.
param.description = <string> Description. It's a required parameter.
param.command = <string> Command. It's a required parameter.
param.node = <string> Node.
param.severity = <list> Severity. It's a required parameter. It's default value is INFO.

[puppet_enterprise_tasks]
param.noop = <bool> Noop.
param.parameters = <string> Parameters.
param.description = <string> Description. It's a required parameter.
param.severity = <list> Severity. It's a required parameter. It's default value is INFO.
param.environment = <string> Environment. It's a required parameter. It's default value is production.
param.module = <string> Task. It's a required parameter.
param.host = <string> Node. It's a required parameter.

