import React from 'react';
import type { GlobalAlert } from '../types';
import { AlertCircle, AlertTriangle, Info } from 'lucide-react';

interface AlertsListProps {
  alerts: GlobalAlert[];
}

const AlertsList: React.FC<AlertsListProps> = ({ alerts }) => {
  const getIcon = (severity: string) => {
    switch (severity) {
      case 'HIGH': return <AlertCircle className="text-red-500" />;
      case 'MEDIUM': return <AlertTriangle className="text-yellow-500" />;
      default: return <Info className="text-blue-500" />;
    }
  };

  const getBgColor = (severity: string) => {
    switch (severity) {
      case 'HIGH': return 'bg-red-50 border-red-200';
      case 'MEDIUM': return 'bg-yellow-50 border-yellow-200';
      default: return 'bg-blue-50 border-blue-200';
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
      <h3 className="text-lg font-semibold mb-4">System Alerts</h3>
      <div className="space-y-3 max-h-[400px] overflow-y-auto">
        {alerts.length === 0 ? (
          <p className="text-gray-500 text-center py-4">No active alerts</p>
        ) : (
          alerts.map((alert, index) => (
            <div key={index} className={`p-3 rounded border flex items-start ${getBgColor(alert.severity)}`}>
              <div className="mr-3 mt-0.5">
                {getIcon(alert.severity)}
              </div>
              <div>
                <div className="flex items-center">
                  <span className="font-medium text-sm mr-2">{alert.trainset_id}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-white border border-gray-300">
                    {alert.alert_type}
                  </span>
                </div>
                <p className="text-sm text-gray-700 mt-1">{alert.message}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AlertsList;
