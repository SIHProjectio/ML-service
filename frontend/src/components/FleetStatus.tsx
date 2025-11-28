import React from 'react';
import type { FleetSummary } from '../types';
import { Train, AlertTriangle, Wrench, CheckCircle } from 'lucide-react';

interface FleetStatusProps {
  summary: FleetSummary;
}

const FleetStatus: React.FC<FleetStatusProps> = ({ summary }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 flex items-center">
        <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
          <Train size={24} />
        </div>
        <div>
          <p className="text-sm text-gray-500">Total Fleet</p>
          <p className="text-2xl font-bold">{summary.total_trainsets}</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 flex items-center">
        <div className="p-3 rounded-full bg-green-100 text-green-600 mr-4">
          <CheckCircle size={24} />
        </div>
        <div>
          <p className="text-sm text-gray-500">Revenue Service</p>
          <p className="text-2xl font-bold">{summary.revenue_service}</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 flex items-center">
        <div className="p-3 rounded-full bg-yellow-100 text-yellow-600 mr-4">
          <AlertTriangle size={24} />
        </div>
        <div>
          <p className="text-sm text-gray-500">Standby</p>
          <p className="text-2xl font-bold">{summary.standby}</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 flex items-center">
        <div className="p-3 rounded-full bg-red-100 text-red-600 mr-4">
          <Wrench size={24} />
        </div>
        <div>
          <p className="text-sm text-gray-500">Maintenance</p>
          <p className="text-2xl font-bold">{summary.maintenance}</p>
        </div>
      </div>
    </div>
  );
};

export default FleetStatus;
