# PR Analyzer (MVP)

AI 支持的智能代码评审辅助工具 —— 针对 GitLab Merge Request，提供风险画像、语义摘要与上下文导航。

## 技术栈
- Backend: Python (FastAPI)
- Queue: Kafka
- DB: PostgreSQL + pgvector
- Object Storage: MinIO
- Embedding: all-MiniLM-L12-v2
- LLM: OpenAI GPT-4o 或本地 Llama3
- Observability: OpenTelemetry + Prometheus + Grafana
- Infra: Docker Compose (dev)

## 目录结构
```
backend/        # 后端服务
  app/
    core/       # 配置、数据库
    api/        # 路由
    models/     # ORM模型
    services/   # 业务服务(解析/风险/摘要)
    repositories/ # 数据访问
    utils/      # 工具函数
infra/
  docker/       # docker-compose
  k8s/          # 未来K8s部署模板
scripts/        # 运维/迁移脚本
docs/           # 设计文档
```

## 快速启动 (开发环境)

### 1. 启动依赖与后端
```bash
cd infra/docker
docker compose up -d --build
```
访问: http://localhost:8000/api/healthz

### (无 Docker 本地运行 Backend)
适用于仅需启动 API 做开发调试的场景：
1. 创建本地环境文件 `.env.local`（可选）：
```
LOCAL_MODE=true
DISABLE_KAFKA=true
DISABLE_MINIO=true
DISABLE_EMBEDDING=true
LOG_LEVEL=INFO
```
2. 运行 PowerShell 脚本：
```powershell
pwsh scripts/run_local_backend.ps1
```
3. 访问: http://localhost:8000/api/healthz
默认使用 SQLite `./data/local.db`，无需 Postgres/Kafka/MinIO。

Windows 安装提示：如需连接 Postgres，请确保已安装官方 PostgreSQL 并将 `pg_config` 所在目录加入 PATH；项目已改用 `psycopg` 以减少编译问题。本地仅调试可使用 `requirements-local.txt` 避免多余依赖。

### 2. 创建 MinIO bucket
登录 MinIO console: http://localhost:9001 使用默认凭证 `minioadmin/minioadmin` 创建 `diff-snapshots`。

### 3. pgvector 扩展安装
进入 postgres 容器执行:
```bash
docker exec -it postgres psql -U pr_user -d pr_analyzer -c 'CREATE EXTENSION IF NOT EXISTS vector;'
```

## 后续开发建议
- 添加模型：文件/函数复杂度、结构差异分析
- 集成 GitLab Webhook 接收 MR 事件
- 构建风险评分规则与摘要生成管线

## 健康检查
- `GET /api/healthz` 返回 {"status": "ok"}

## License
TBD
