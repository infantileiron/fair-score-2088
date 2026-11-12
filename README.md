# 衡尺招聘 · 筛选公平性复核

为衡尺招聘评估组12人构建的回顾性筛选审计工作台。用模拟匿名候选数据复核统一分数线下的组间差异，保留样本分母、Wilson区间、人工意见与归档报告。

## 场景与工作流

团队此前用多张Excel手工比较入选率：分组分母不明、阈值更改缺少留痕、稀少样本的差异容易被过度解读。上游为统一技能测评和去标识筛选记录；本项目替代样本核对、差异计算和报告复核；下游由评估研究组讨论后续核查，不自动做录用决策。

一天的剧本：09:00分析员登录；09:03查看 hengchi_candidates_202611.json 的800条样本与两组分母；09:08新建统一阈值65、差距提示线0.10的方案；09:10提交后台计算；09:12检查入选率/TPR/FPR及Wilson区间；09:15比较21档阈值的非支配前沿；09:20记录标签偏差与样本局限；09:25管理员确认最新复核为接受后归档；09:30只读复核员下载真实CSV。

## 功能与角色

- 候选样本：匿名JSON导入、重复ID/样本量/组数/分数边界校验；全量计算、前40条预览。
- 分数线方案：统一阈值、数据集及人工差距提示线持久化。
- 后台复核：Redis队列和独立Python worker；运行状态、计算结果和校验码写入PostgreSQL；worker重启恢复持久化的排队/运行任务。
- 证据页：组间混淆计数、分母、Wilson95%区间、真实阈值前沿图。
- 人工复核/归档：最新复核为接受才能由管理员归档，一次运行只归档一次；CSV下载与操作审计。

|角色|权限|典型动作|
|---|---|---|
|admin|全部读写及批准归档|确认复核后创建报告|
|analyst|导入样本、建方案、运行、提交人工意见|运行统一阈值复核|
|viewer|只读与下载归档CSV|核对结果；写入返回403|

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

访问 http://localhost:18212 ，后端 http://localhost:19212/docs ，数据库映射17712。五服务frontend/backend/worker/db/redis均有healthcheck；数据库、Redis、worker产物各用命名卷。结束演示：`docker compose down -v --remove-orphans`，这会清除本项目演示数据。

账号：admin@hengchi.demo、analyst@hengchi.demo、viewer@hengchi.demo；统一演示密码`Review2026!`。只用于本地模拟环境。JWT_SECRET在实际使用前自行替换。

SEED_DEMO=true自动建表及填充种子。自然键和固定种子ID保证重复运行不新增、不覆盖用户修改；800条候选由固定随机种子2203生成，不含真实个人信息。seed输出六类实体计数供幂等核对。

## 算法与口径

组间复核：对分数≥统一阈值计为入选，统一技能测评的qualified作为参考标签。计算TP/FP/FN/TN、入选率、TPR、FPR；分母为0则返回null（UI显示无分母），至少两组可估计才能计算组间最大差距。逐组Wilson区间使用z=1.959963984540054，公式为(p+z²/2n)/(1+z²/n) ± z√(p(1-p)/n+z²/4n²)/(1+z²/n)。n=0无可估计区间。

阈值Pareto：扫描0至100、步长5的21个全组统一阈值；准确率为(TP+TN)/N，差距为最大与最小入选率差。若另一个阈值准确率不低、差距不高，且至少一项严格更好，当前阈值被支配。前沿仅供回顾性讨论，不自动推荐招聘决策。

两算法均由Python真实计算；前端仅绘制持久化结果。输入至少20条、2至8组、最多5000条，分数必须有限且在[0,100]，候选ID唯一。阈值网格固定，无随机计算，样本JSON附SHA256用于复现。

局限：模拟组别是复核批次；差异不直接代表因果或合规判断。标签可能存在偏差。Wilson为逐组区间，未做多重比较校正；小样本低于30条醒目标记。没有真实招聘服务连接、自动录用和个人画像。

## 技术、目录与开发

|部分|技术|
|---|---|
|前端|React18、TypeScript、Vite、Nginx|
|后端|Python3.11、FastAPI、SQLAlchemy、PyJWT|
|持久化|PostgreSQL16|
|队列|Redis7、独立Python worker|

frontend/src含api、stores、types、components/common、hooks、pages、router、utils、constants；backend/src含routes、controllers、services、models、schemas、middlewares、utils、constants、config；backend/scripts为seed；backend/migrations说明初始模型与生产变更约束。

本地开发：后端安装backend/requirements.txt，配置DATABASE_URL/REDIS_URL/JWT_SECRET后在backend目录`uvicorn src.main:app --reload`；另开`python -m src.worker`。前端`npm install && npm run dev`，开发请求需同源反向代理/api到后端；默认Docker已由Nginx配置此代理。

环境变量：COMPOSE_PROJECT_NAME=fair-score；FRONTEND_PORT=18212；BACKEND_PORT=19212；DB_PORT=17712；JWT_SECRET签名密钥；SEED_DEMO自动种子开关。DATABASE_URL和REDIS_URL由Compose传入服务。双字体通过Google Fonts加载，网络不可用时使用浏览器衬线/无衬线回退，不影响业务。

共享枚举：角色admin/analyst/viewer与运行状态queued/running/completed/failed定义于backend/src/constants/enums.py及frontend/src/constants/enums.ts；角色校验在backend/src/controllers/auth.py；运行状态变更在services/runs.py和worker.py，前端Status组件与Results页消费。复核decision为accepted/needs_attention，在schemas/review.py与前端constants/enums.ts及Reviews页保持一致。

测试脚本、真实截图、日志、TESTING.md均在批次test-artifacts/gb-2203目录，源码包不混入这些产物。数据库模式由SQLAlchemy初次初始化，未提供生产迁移回滚；当前异步任务适合单worker演示，未实现分布式租约和多worker去重。

MIT License。
