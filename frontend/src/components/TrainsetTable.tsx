import React from 'react';
import type { Trainset } from '../types';

interface TrainsetTableProps {
  trainsets: Trainset[];
}

const TrainsetTable: React.FC<TrainsetTableProps> = ({ trainsets }) => {
  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold">Fleet Details</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Readiness</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Daily KM</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duty</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {trainsets.map((train) => (
              <tr key={train.trainset_id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{train.trainset_id}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${train.status === 'REVENUE_SERVICE' ? 'bg-green-100 text-green-800' : 
                      train.status === 'MAINTENANCE' ? 'bg-red-100 text-red-800' : 
                      'bg-yellow-100 text-yellow-800'}`}>
                    {train.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div className="flex items-center">
                    <div className="w-16 bg-gray-200 rounded-full h-2.5 mr-2">
                      <div 
                        className={`h-2.5 rounded-full ${train.readiness_score > 0.8 ? 'bg-green-500' : train.readiness_score > 0.5 ? 'bg-yellow-500' : 'bg-red-500'}`} 
                        style={{ width: `${train.readiness_score * 100}%` }}
                      ></div>
                    </div>
                    <span>{(train.readiness_score * 100).toFixed(0)}%</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{train.daily_km_allocation} km</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{train.assigned_duty || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {train.stabling_bay || train.ibl_bay || '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TrainsetTable;
