# PR Analyzer (MVP)

AI 支持的智能代码评审辅助工具 —— 针对 GitLab Merge Request，提供风险画像、语义摘要与上下文导航。

## 技术栈
- Backend: Python (FastAPI)
- Queue: Kafka
- DB: PostgreSQL + pgvector (或 SQLite 本地模式)
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

### 1. 配置环境变量
创建 `.env.local` 文件并配置 GitLab 信息：
```
ENV=dev
LOCAL_MODE=true
DISABLE_KAFKA=true
DISABLE_MINIO=true
DISABLE_EMBEDDING=true
LOG_LEVEL=INFO
GITLAB_BASE_URL=https://gitlab.mycwt.com.cn
GITLAB_TOKEN=your_gitlab_token_here
```

### 2. 启动后端服务
运行 PowerShell 脚本：
```powershell
pwsh scripts/run_local_backend.ps1
```
访问: http://localhost:8080/api/healthz
默认使用 SQLite `./data/local.db`，无需 Postgres/Kafka/MinIO。

### 3. 测试 API 端点
使用提供的测试脚本验证 API 功能：
```bash
python test_real_pr.py
```
该脚本将从 GitLab 获取真实 PR 数据并测试所有 API 端点。

### (Docker 完整环境)
如需完整环境（包含依赖服务）：
```bash
cd infra/docker
docker compose up -d --build
```
访问: http://localhost:8000/api/healthz

Windows 安装提示：如需连接 Postgres，请确保已安装官方 PostgreSQL 并将 `pg_config` 所在目录加入 PATH；项目已改用 `psycopg` 以减少编译问题。本地仅调试可使用 `requirements-local.txt` 避免多余依赖。

## 已实现功能
- GitLab Webhook 接收 MR 事件
- 风险评分计算（基于规则的加权风险评估）
- 拉取请求数据存储与风险历史记录
- 本地模式支持（无需外部依赖）
- 文件/函数复杂度分析 API
- 测试覆盖率分析：检测PR对测试覆盖率的影响，识别未测试的新代码
- 依赖变更检测：监控PR中的依赖库变更，提示安全风险和兼容性问题
- 安全漏洞扫描：自动检测PR中引入的安全漏洞和代码缺陷
- 代码重复检测：识别PR中的重复代码片段，帮助保持代码简洁性
- 协作效率提升：PR评论智能分类、行动项提取，加速代码评审流程


## 后续开发建议
- 实现结构差异分析
- 构建摘要生成管线
- 集成 LLM 进行智能代码评审
- 测试覆盖率分析：检测PR对测试覆盖率的影响，识别未测试的新代码
- 依赖变更检测：监控PR中的依赖库变更，提示安全风险和兼容性问题
- 安全漏洞扫描：自动检测PR中引入的安全漏洞和代码缺陷
- 代码重复检测：识别PR中的重复代码片段，帮助保持代码简洁性
- 协作效率提升：PR评论智能分类、行动项提取，加速代码评审流程

## API 端点

### 健康检查
- `GET /api/healthz` 返回 {"status": "ok"}

### 环境信息
- `GET /api/env` 返回当前环境配置

### GitLab Webhook
- `POST /api/gitlab/webhook` 接收 GitLab MR 事件并计算风险评分

### 代码复杂度分析
- `POST /api/analyze/complexity` 分析代码片段的复杂度
  - 参数: `code` (代码片段), `language` (编程语言, 默认: python)

### 测试覆盖率分析
- `POST /api/analyze/test-coverage` 分析PR对测试覆盖率的影响
  - 参数: `baseline_coverage` (基线覆盖率数据), `pr_coverage` (PR覆盖率数据)

### 依赖变更检测
- `POST /api/analyze/dependency-changes` 检测PR中的依赖库变更
  - 参数: `baseline_deps` (基线依赖), `pr_deps` (PR依赖)

### 安全漏洞扫描
- `POST /api/analyze/security-scan` 扫描代码中的安全漏洞和缺陷
  - 参数: `code` (代码片段), `language` (编程语言, 默认: python)

### 代码重复检测
- `POST /api/analyze/code-duplication` 检测代码中的重复片段
  - 参数: `code` (代码片段), `language` (编程语言, 默认: python), `min_lines` (最小重复行数, 默认: 3)

### 协作效率分析
- `POST /api/analyze/collaboration` 分析PR评论的协作效率
  - 参数: `comments` (评论列表)
  - 返回: 行数、函数数、类数、圈复杂度、Halstead 体积、复杂度等级等信息

## 风险评分机制

风险评分基于以下特征：
- **复杂度增量**：代码变更的复杂度
- **文件热度**：修改的文件被修改的频率
- **敏感路径**：是否修改了敏感文件
- **作者经验**：作者的代码贡献经验

评分范围：0-1，分为低、中、高三个风险等级

## 配置

主要配置选项：
- `LOCAL_MODE`: 本地模式开关（默认：False）
- `GITLAB_BASE_URL`: GitLab 服务器地址
- `GITLAB_TOKEN`: GitLab API 令牌
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka 服务器地址
- `PG_HOST`: PostgreSQL 服务器地址
- `MINIO_ENDPOINT`: MinIO 服务器地址
- `EMBEDDING_MODEL_NAME`: 嵌入模型名称
- `LLM_PROVIDER`: LLM 提供商（openai 或 local）

完整配置请参考 `backend/app/core/config.py`

## License
TBD
