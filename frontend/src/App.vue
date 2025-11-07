<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

// 状态管理
const repoName = ref('')
const token = ref('')
const prList = ref([])
const selectedPRs = ref([])
const selectedCategories = ref([])
const analysisResults = ref([])
const loading = ref(false)

// 检测类别
const categories = [
  { id: 'complexity', name: '代码复杂度' },
  { id: 'security', name: '安全扫描' },
  { id: 'duplication', name: '代码重复' },
  { id: 'collaboration', name: '协作分析' }
]

// 获取PR列表
const getPRs = async () => {
  if (!repoName.value || !token.value) {
    alert('请输入仓储名和Token')
    return
  }
  loading.value = true
  try {
    const response = await axios.post('http://localhost:8080/api/gitlab/prs', {
      repo_name: repoName.value,
      token: token.value
    })
    prList.value = response.data.prs
  } catch (error) {
    console.error('获取PR列表失败:', error)
    alert('获取PR列表失败，请检查仓储名和Token是否正确')
  } finally {
    loading.value = false
  }
}

// 选择PR
const togglePR = (prId) => {
  const index = selectedPRs.value.indexOf(prId)
  if (index > -1) {
    selectedPRs.value.splice(index, 1)
  } else {
    selectedPRs.value.push(prId)
  }
}

// 选择检测类别
const toggleCategory = (categoryId) => {
  const index = selectedCategories.value.indexOf(categoryId)
  if (index > -1) {
    selectedCategories.value.splice(index, 1)
  } else {
    selectedCategories.value.push(categoryId)
  }
}

// 执行检测
const runAnalysis = async () => {
  if (selectedPRs.value.length === 0) {
    alert('请选择至少一个PR')
    return
  }
  if (selectedCategories.value.length === 0) {
    alert('请选择至少一个检测类别')
    return
  }
  loading.value = true
  try {
    const response = await axios.post('http://localhost:8080/api/analyze', {
      pr_ids: selectedPRs.value,
      categories: selectedCategories.value
    })
    analysisResults.value = response.data.results
  } catch (error) {
    console.error('执行检测失败:', error)
    alert('执行检测失败，请检查网络连接和参数是否正确')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="app-container">
    <h1>PR检测分析系统</h1>
    
    <!-- 输入区域 -->
    <div class="input-section">
      <div class="input-group">
        <label for="repoName">仓储名:</label>
        <input 
          id="repoName" 
          v-model="repoName" 
          placeholder="例如: username/repo"
        />
      </div>
      <div class="input-group">
        <label for="token">GitLab Token:</label>
        <input 
          id="token" 
          v-model="token" 
          type="password" 
          placeholder="请输入GitLab访问令牌"
        />
      </div>
      <button @click="getPRs" :disabled="loading">
        {{ loading ? '加载中...' : '获取PR列表' }}
      </button>
    </div>
    
    <!-- PR选择区域 -->
    <div class="pr-section">
      <h2>选择PR</h2>
      <div class="pr-list">
        <div 
          v-for="pr in prList" 
          :key="pr.id" 
          class="pr-item"
          :class="{ selected: selectedPRs.includes(pr.id) }"
          @click="togglePR(pr.id)"
        >
          <div class="pr-title">{{ pr.title }}</div>
          <div class="pr-meta">#{{ pr.id }} - {{ pr.author }} - {{ pr.created_at }}</div>
        </div>
      </div>
    </div>
    
    <!-- 检测类别选择区域 -->
    <div class="category-section">
      <h2>选择检测类别</h2>
      <div class="category-list">
        <div 
          v-for="category in categories" 
          :key="category.id" 
          class="category-item"
          :class="{ selected: selectedCategories.includes(category.id) }"
          @click="toggleCategory(category.id)"
        >
          {{ category.name }}
        </div>
      </div>
    </div>
    
    <!-- 执行检测按钮 -->
    <div class="action-section">
      <button @click="runAnalysis" :disabled="loading">
        {{ loading ? '检测中...' : '执行检测' }}
      </button>
    </div>
    
    <!-- 检测结果区域 -->
    <div class="results-section" v-if="analysisResults.length > 0">
      <h2>检测结果</h2>
      <div v-for="result in analysisResults" :key="result.pr_id" class="result-item">
        <h3>PR #{{ result.pr_id }}</h3>
        <div v-for="(categoryResult, category) in result.results" :key="category" class="category-result">
          <h4>{{ categories.find(c => c.id === category)?.name || category }}</h4>
          <pre>{{ JSON.stringify(categoryResult, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.input-section {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
  align-items: flex-end;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

button {
  padding: 8px 16px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background-color: #35495e;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pr-section, .category-section, .results-section {
  margin-bottom: 30px;
}

.pr-list, .category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.pr-item, .category-item {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  background-color: #fff;
}

.pr-item:hover, .category-item:hover {
  border-color: #42b883;
}

.pr-item.selected, .category-item.selected {
  background-color: #42b883;
  color: white;
  border-color: #42b883;
}

.pr-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.pr-meta {
  font-size: 12px;
  opacity: 0.8;
}

.result-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.category-result {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

pre {
  white-space: pre-wrap;
  font-size: 12px;
  margin-top: 5px;
}
</style>
