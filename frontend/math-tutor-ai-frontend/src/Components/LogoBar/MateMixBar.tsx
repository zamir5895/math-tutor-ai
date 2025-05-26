import React from 'react'

type MateMixBarProps = {
  icon: React.ReactNode
  label: string
  percent: number
  color: string
}

const MateMixBar = ({ icon, label, percent, color }: MateMixBarProps) => {
  return (
    <div className="flex items-center gap-2">
      <div className="w-5 h-5 flex items-center justify-center">{icon}</div>
      <span className="w-20 font-medium">{label}</span>
      <span className="text-xs w-10">{percent}%</span>
      <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <div className={`h-full ${color}`} style={{ width: `${percent}%` }}></div>
      </div>
    </div>
  )
}

export default MateMixBar
