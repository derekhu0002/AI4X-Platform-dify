# Task And Issues For LLM

| Name | Problem | ProblemNotes | ResolverNotes | ProblemType | Status | Object_ID |
| --- | --- | --- | --- | --- | --- | --- |
| BusinessLayer | 请添加业务层的测试用例集 | 1、这儿测试用例是用于指导测试人员对真实系统的测试工作而不是一个自动化的单元测试或者集成测试；<br>2、测试的目的是从真实用户视角出发，对系统提供的服务进行验收，可以不用针对每种业务角色来设计测试用例，而是从capability视角来设计人工测试验收用例；<br>3、真实系统的访问环境：个人PC，安装DOCKER DESKTOP，并按照DIFY和OPENCTI的DOCKER；<br>4、测试数据准备方式：请基于业务层的用户故事中的价值流场景帮我给出一套虚拟的测试数据；<br>5、测试账号/角色分配：测试时给出，测试用例中用占位符代替；<br>6、人工验收记录模板：请结合我们的项目，使用业界最佳实践给出；<br>7、测试用例最终需要落成独立 Markdown 文档，以及汇总表格；<br>8、需要把人工验收用例与已有自动化测试目录分开管理；<br>9、每条 capability 的通过/不通过判定不需要量化评分、截图留证或审批签字<br>10、如果业务层设计与现网系统当前能力不一致，当前任务是先暴露差距<br>11、测试用例文档放到tests\validation下<br>12、测试人员实际使用的 Dify地址：http://localhost/apps，OpenCTI 访问地址：http://localhost:8080/dashboard<br>13、OpenCTI中的数据通过OPENCTI上的数据导入功能导入；<br>14、业务负责人、安全负责人、管理层、安全运营团队用一个测试账号<br>15、Notification MCP 实际邮件投递是否在测试环境可达，不需要 mock 收件箱<br>16、OpenCTI 导入的测试数据具体采用 STIX Bundle 文件<br>17、需要为每条 capability 单独生成文档 |  | ToDo | Active | 1208 |
