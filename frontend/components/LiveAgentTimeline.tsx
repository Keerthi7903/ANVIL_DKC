'use client'

import AgentCard from './AgentCard'

interface Props {
  agentResults: any[]
}

export default function LiveAgentTimeline({
  agentResults,
}: Props) {

  return (
    <div className="space-y-6">

      {agentResults.map(
        (agent, index) => (

          <AgentCard
            key={`${agent.agent_name}-${index}`}
            agent={{
              name: agent.agent_name,
              description:
                agent.recommended_action ||
                'Autonomous agent execution',
              confidence:
                agent.confidence,
              duration:
                `${agent.duration_ms}ms`,
            }}
            status={
              agent.status === 'success'
                ? 'completed'
                : agent.status === 'failed'
                ? 'pending'
                : 'running'
            }
          />

        )
      )}

    </div>
  )
}