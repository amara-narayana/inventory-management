import { useState, useEffect } from 'react'

interface DashboardStats {
  todaySales: number
  totalProducts: number
  lowStockItems: number
  inventoryValue: number
}

export default function Dashboard() {
  const [_stats, setStats] = useState<DashboardStats>({
    todaySales: 0,
    totalProducts: 0,
    lowStockItems: 0,
    inventoryValue: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // In production, fetch from API
    // For now, show placeholder
    setLoading(false)
  }, [])

  const statCards = [
    { title: "Today's Sales", value: `₹${_stats.todaySales.toLocaleString('en-IN')}`, icon: '💰', color: 'bg-green-500' },
    { title: 'Total Products', value: _stats.totalProducts.toString(), icon: '👗', color: 'bg-blue-500' },
    { title: 'Low Stock Items', value: _stats.lowStockItems.toString(), icon: '⚠️', color: 'bg-yellow-500' },
    { title: 'Inventory Value', value: `₹${_stats.inventoryValue.toLocaleString('en-IN')}`, icon: '📦', color: 'bg-purple-500' },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-800">Dashboard</h2>
        <p className="text-gray-600">Welcome to Saree Shop Management System</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card) => (
          <div key={card.title} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">{card.title}</p>
                <p className="text-2xl font-bold text-gray-800">{card.value}</p>
              </div>
              <div className={`${card.color} text-white p-3 rounded-lg text-2xl`}>
                {card.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Sales</h3>
          <div className="text-center text-gray-500 py-8">
            <p>No recent sales data available</p>
            <p className="text-sm mt-2">Start using POS to record sales</p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Low Stock Alerts</h3>
          <div className="text-center text-gray-500 py-8">
            <p>No low stock items</p>
            <p className="text-sm mt-2">Inventory levels are healthy</p>
          </div>
        </div>
      </div>
    </div>
  )
}
