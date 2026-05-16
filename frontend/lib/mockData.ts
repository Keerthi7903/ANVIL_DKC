export const workflows = [
  {
    id: 'wf-001',
    title: 'feat/payment-retry-system',
    repo: 'my-org/backend',
    status: 'running',
    decision: 'Analyzing CI failures',
    time: '2 mins ago',
  },
  {
    id: 'wf-002',
    title: 'fix/auth-token-refresh',
    repo: 'my-org/api',
    status: 'completed',
    decision: 'Auto-assigned reviewer',
    time: '8 mins ago',
  },
  {
    id: 'wf-003',
    title: 'refactor/user-service',
    repo: 'my-org/core',
    status: 'failed',
    decision: 'GitHub API timeout',
    time: '15 mins ago',
  },
]

export const agents = [
  {
    name: 'Planner',
    description: 'Orchestrating pipeline',
    confidence: 0.98,
    duration: '1220ms',
  },
  {
    name: 'Priority',
    description: 'Scoring urgency with Gemini',
    confidence: 0.87,
    duration: '840ms',
  },
  {
    name: 'Research',
    description: 'Searching Tavily for similar issues',
    confidence: 0.72,
    duration: '1430ms',
  },
  {
    name: 'Reflection',
    description: 'Self-checking confidence',
    confidence: 0.91,
    duration: '620ms',
  },
]
