### Git提交规范
```
feat 适用场景：全是新增功能，在旧功能基础上做改动（包含新增，删除）
fix 适用场景：修复bug，包含测试环境和生产环境
refactor 适用场景：重构任何功能，重构前和重构后输入和输出需要完全不变，如果有变化，在改动的部分请使用`feat`
test 适用场景：增加单元测试时
style 适用场景：修改代码格式，代码逻辑完全不变
docs 适用场景：编写注释或者使用文档
```
## 一、整个框架设计思路
1. `OkHttps`+`AllureUtils` 模块进行http的请求及allure报告日志信息注入
2. `pytest`实现单元测试 、`@pytest.mark.parametrize`实现数据驱动（实际业务使用过程中并不灵活，太局限）
3. `HarToData EncrypUtils（加解密）`实现模块自动导出标`RESTful`风格的测试用例 （有依赖性的接口 感觉效率并不高）
4. `Processor` 来实现 前置、后置脚本处理的功能
5. `RandUtils （随机获取字符）FileUtils（文件处理）DataUtils（日期处理）....`来产生测试数据
6. `MySQLUtils`、`RedisUtils`实现过多依赖上级接口调换数据中间挂了的问题
7. `DataKit`、`Loader`、`JsonUtils`、`YamlUtils`、`Template`数据加载及处理部分格式问题
8. `Wrapper` 扩展语法糖
9. `WxRobotTools`、`EmaliUtils`、`JenkinsUtils` 实现企微推送机器人及邮件抄送
## 二、实际目录结构
```
InterfaceTest
├─ config （allure、header、消息推送是的一些配置信息）
│  ├─ allure_feature.yaml
│  ├─ norm_headers.yaml
│  └─ push_message.yaml
├─ environment.properties （allure报告所需的环境变量）
├─ application-prod.yaml  （生成环境配置）
├─ application-sit.yaml   （sit环境配置）
├─ application-uat.yaml   （uat环境配置）
├─ application.properties.yaml （环境声明）
├─ BaseSetting.py          （项目所需引用到的路径配置）
├─ conftest.py             （pytest fixture应用）
├─ iutils  （工具类、若业务用不上的也可以去掉一部分）
│  ├─ AllureUtils.py
│  ├─ AreaCode.py
│  ├─ Assertion.py
│  ├─ ConfigParser.py
│  ├─ DataKit.py
│  ├─ DateUtils.py
│  ├─ DingTalkRobot.py
│  ├─ EmaliUtils.py
│  ├─ EncryptUtils.py
│  ├─ Exceptions.py
│  ├─ FolderUtils.py
│  ├─ HarToData.py
│  ├─ Helper.py
│  ├─ IDCards.py
│  ├─ JenkinsUtils.py
│  ├─ JsonUtils.py
│  ├─ Loader.py
│  ├─ LogUtils.py
│  ├─ MySQLUtils.py
│  ├─ OkHttps.py
│  ├─ PandasUtils.py
│  ├─ Processor.py
│  ├─ RandUtils.py
│  ├─ RedisUtils.py
│  ├─ Shell.py
│  ├─ Swagger.py
│  ├─ Template.py
│  ├─ Wrapper.py
│  ├─ WxRobotTools.py
│  ├─ YamlUtils.py
│  └─ __init__.py
├─ libs  （依赖包）
├─ output（日志产生存等相关输出的路径）
├─ pytest.ini （pytest一些基础配置、注意要ansi编码）
├─ requirements.txt （依赖架包）
├─ RunAll.py  （调试的时候用的主函数）
├─ SendMsg.py  （发送邮件及消息推送）
├─ summary.yaml 存储产生报告结果的
├─ testings  （测试类、主要分config、control、dao、service层具体实现根据不同业务）
│  ├─ config
│  │  ├─ localhost （离线本地数据）
│  │  │  └─ xxxx.yaml
│  │  ├─ properties (域名及url的基础配置)
│  │  │  ├─ dns_prod.yaml
│  │  │  ├─ dns_sit.yaml
│  │  │  └─ dns_uat.yaml
│  │  └─ variables  （自定义参数：如token、全局变量...）
│  │     ├─ token.yaml
│  │     └─ global.yaml
│  ├─ control （一些相关配置：依赖数据、路径、sql连接、url...）
│  │  ├─ data.py
│  │  ├─ init.py
│  │  ├─ path.py
│  │  ├─ sql.py
│  │  ├─ url.py
│  │  ├─ variables.py
│  │  └─ __init__.py
│  ├─ dao  （准备好的测试数据）
│  │  ├─ test_csv
│  │  │  └─ xxxx.csv
│  │  ├─ test_img
│  │  │  └─ xxxx.png
│  │  ├─ test_json
│  │  │  └─ xxxxx.json
│  │  └─ test_yaml
│  │     └─ xxxxx.yaml
│  ├─ entity  （公共实体类）
│  │  ├─ Backend.py
│  │  ├─ Blockette.py
│  │  ├─ Login.py
│  │  └─ Seckill.py
│  └─ service  （case编写）
│     ├─ product
│     │  ├─ test_xxxx_001.py
│     │  └─ test_xxxx_002.py
│     └─ seckilll
│        ├─ test_xxxx_001.py
│        ├─ test_xxxx_002.py
│        ├─ test_xxxx_003.py
├─ _version.py
├─ __init__.py
```

## 三、jenkins 持续集成
1. jenkins 中配置源码 git 路径
2. jenkins 中配置 allure
3. 构建，查看报告

## 四、Case编写规范
#### 全自动模式
1. 调用iutils模块下的HarToData或者手动创建一个测试yaml数据格式如下：

```
config:
- headers:
- allures:
- request:
test_setup:
  test_name:
    allures:
    headers:
    request:
    validations:
      expected_code: status_code
      expected_content: content
      expected_variables: (单字段效验)
        json_path: [eq_method,var]
      expected_time: timeout
    extracts:
        var_name: json_path
```

2. 创建一个文件目录（即模块说明）
3. 在对接模块下创建一个测试类 （需注意的是开头需要与pytest.ini配置文件中的python_files保持一致）
4. 编写case：

```
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("test_helper.yaml")['config']
test_setup = Envision.getYaml("test_helper.yaml")['test_setup']

class TestClass():
    def test_func_xxx(self):
        Httpx.sendApi(auto=True, esdata=[config,test_setup["test_name"]])        
```

#### 半自动模式
1. 暂时不用考虑

### 手动
1. 所有的数据来源在case中声明于调用request模块保持一致

### 混合模式
1. yaml+case均给了参数 默认以最后声明者为主

```
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("test_helper.yaml")['config']
test_setup = Envision.getYaml("test_helper.yaml")['test_setup']

class TestClass():
    def test_func_xxx(self):
        url= url
        method = method
        data, json, params = randData()
        hook_header= extend_headers
        esdata=[config, test_setup["test_name"]]
        Httpx.sendApi(method=method, url=url, aided=True,hook_header=hook_header,data=data,esdata=esdata)
```

### case上下联动
1. 在全自动模式下需要给extracts参数
2. 手动模式下可以req进行赋值调用Httpx中的获取对应值的函数来实现数据依赖

### 调试测试类

```
import pytest
pytest.main(["-v","test_project.py"])
pytest.main(["-v","test_project.py::TestClass"])
pytest.main(["-v","test_project.py::TestClass::test_func"])
```

## 五、不同方式的数据请求说明
1. params:字典或者字节序列作为参数增加到URL中多半用于get

```
data ={'wd':'params作用域',}
response = requests.get('https://www.baidu.com/s',params=data)
print(response.url)
输出：
https://www.baidu.com/s?wd=params作用域
等同于：
response = requests.get('https://www.baidu.com/s?wd=params作用域')
print(response.url)
```

2. data|json都是用于post提交的、但是区别在于：不同在于data需要强转json.dumps格式、json参数会自动将字典类型的对象转换为json格式

```
response = Httpx.sendApi(method="post", url=url, json=target_data)
等同于：
response = Httpx.sendApi(method="post", url=url, json=json.dumps(target_data,ensure_ascii=False))
```

## 六、断言
1. 原生assert

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
 
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    assert x == y  #如果这个断言失败，则后续都不会执行
    assert True
    assert False
```

2. pytest-assume

```
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_pytest_assume(x, y):
    pytest.assume(x == y) #即使这个断言失败，后续仍旧执行
    pytest.assume(True)
    pytest.assume(False)
```


|断言类型| 1，1 | 1，0 | 0，1 | 结论 |
| :----:| :----: | :----: |:----:| :----: |
| assert | 断言3失败 | 断言1失败 |断言2和断言3不执行|断言1失败，断言2和断言3不执行|assert遇到断言失败则停下|
| pytest.assume | 断言3失败 | 断言1失败 |断言2和断言3继续执行|断言1失败，断言2和断言3继续执行|pytest.assume无论断言结果，全部执行|
通过上下文管理器with使用pytest-assume

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
from pytest import assume
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    #使用上下文管理器的好处是不用显示去try和finally捕获异常，建议使用这种写法，简洁有效。
    with assume: assert x == y
    with assume: assert True
    with assume: assert False
```

主要注意的是，如果上下文管理器里面包含多个断言，则只有第一个会被执行，如

```
#!/usr/bin/env python3
#!coding:utf-8
import pytest
from pytest import assume
    
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    #使用上下文管理器的好处是不用显示去try和finally捕获异常，建议使用这种写法，简洁有效。
    with assume: 
        #只有第一个断言会被执行！
        assert x == y
        assert True
        assert False  
```