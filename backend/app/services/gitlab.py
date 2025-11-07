import gitlab
from app.core.config import settings

class GitLabService:
    def __init__(self):
        self.gitlab_url = settings.GITLAB_URL
    
    async def get_merge_requests(self, repo_name: str, token: str):
        # 创建GitLab客户端
        gl = gitlab.Gitlab(self.gitlab_url, private_token=token)
        
        try:
            # 获取项目
            project = gl.projects.get(repo_name)
            
            # 获取所有打开的合并请求
            merge_requests = project.mergerequests.list(state='opened', all=True)
            
            # 格式化PR信息
            prs = []
            for mr in merge_requests:
                prs.append({
                    'id': mr.id,
                    'title': mr.title,
                    'author': mr.author['name'] if mr.author else 'Unknown',
                    'created_at': mr.created_at,
                    'updated_at': mr.updated_at,
                    'state': mr.state,
                    'source_branch': mr.source_branch,
                    'target_branch': mr.target_branch
                })
            
            return prs
        except Exception as e:
            raise Exception(f"Failed to get merge requests: {str(e)}")
    
    async def handle_webhook(self, request):
        # 处理GitLab Webhook事件
        # 这里可以添加Webhook事件处理逻辑
        pass