import React, { useState } from 'react';
import type { ScheduleData } from '../types';
import FleetStatus from './FleetStatus';
import ScheduleTimeline from './ScheduleTimeline';
import AlertsList from './AlertsList';
import TrainsetTable from './TrainsetTable';
import { Calendar, Clock, Database } from 'lucide-react';

// Import data directly
import schedule1 from '../data/schedule1.json';
import schedule2 from '../data/schedule2.json';

const Dashboard: React.FC = () => {
  const [activeScheduleId, setActiveScheduleId] = useState<string>('schedule1');
  
  // Cast imported JSON to ScheduleData type
  const dataMap: Record<string, ScheduleData> = {
    'schedule1': schedule1 as unknown as ScheduleData,
    'schedule2': schedule2 as unknown as ScheduleData
  };

  const currentData = dataMap[activeScheduleId];

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Metro Schedule Optimizer</h1>
            <p className="text-gray-500 mt-1">Visualizing optimized fleet schedules and assignments</p>
          </div>
          
          <div className="mt-4 md:mt-0 flex items-center space-x-4">
            <div className="bg-white p-2 rounded shadow-sm border border-gray-200 flex items-center">
              <span className="text-sm font-medium mr-2 text-gray-600">Select Schedule:</span>
              <select 
                value={activeScheduleId}
                onChange={(e) => setActiveScheduleId(e.target.value)}
                className="border-gray-300 rounded text-sm focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="schedule1">Schedule 1 (Greedy)</option>
                <option value="schedule2">Schedule 2 (DataService)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Schedule Info Card */}
        <div className="bg-white p-4 rounded-lg shadow border border-gray-200 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center">
              <Database className="text-blue-500 mr-3" />
              <div>
                <p className="text-xs text-gray-500 uppercase">Schedule ID</p>
                <p className="font-mono font-medium">{currentData.schedule_id}</p>
              </div>
            </div>
            <div className="flex items-center">
              <Calendar className="text-green-500 mr-3" />
              <div>
                <p className="text-xs text-gray-500 uppercase">Valid Date</p>
                <p className="font-medium">{new Date(currentData.valid_from).toLocaleDateString()}</p>
              </div>
            </div>
            <div className="flex items-center">
              <Clock className="text-purple-500 mr-3" />
              <div>
                <p className="text-xs text-gray-500 uppercase">Generated At</p>
                <p className="font-medium">{new Date(currentData.generated_at).toLocaleString()}</p>
              </div>
            </div>
          </div>
          
          <div className="mt-4 pt-4 border-t border-gray-100 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Fitness Score:</span>
              <span className="ml-2 font-semibold">{currentData.optimization_metrics.fitness_score.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-500">Total Planned KM:</span>
              <span className="ml-2 font-semibold">{currentData.optimization_metrics.total_planned_km.toLocaleString()} km</span>
            </div>
            <div>
              <span className="text-gray-500">Method:</span>
              <span className="ml-2 font-semibold uppercase">{currentData.optimization_metrics.method}</span>
            </div>
            <div>
              <span className="text-gray-500">Runtime:</span>
              <span className="ml-2 font-semibold">{currentData.optimization_metrics.optimization_runtime_ms} ms</span>
            </div>
          </div>
        </div>

        <FleetStatus summary={currentData.fleet_summary} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-2">
            <ScheduleTimeline trainsets={currentData.trainsets} />
          </div>
          <div>
            <AlertsList alerts={currentData.alerts} />
          </div>
        </div>

        <TrainsetTable trainsets={currentData.trainsets} />
      </div>
    </div>
  );
};

export default Dashboard;
