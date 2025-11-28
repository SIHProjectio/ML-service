import React from 'react';
import type { Trainset } from '../types';
import { getPositionAndWidth, timeToMinutes } from '../utils/timeUtils';

interface ScheduleTimelineProps {
  trainsets: Trainset[];
}

const AVERAGE_SPEED_KMPH = 35;

const ScheduleTimeline: React.FC<ScheduleTimelineProps> = ({ trainsets }) => {
  const timelineStart = '05:00';
  const timelineEnd = '23:00';
  
  // Filter only revenue service trains or those with blocks
  const activeTrainsets = trainsets.filter(t => t.service_blocks && t.service_blocks.length > 0);

  const hours = [];
  for (let i = 5; i <= 23; i++) {
    hours.push(i);
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow border border-gray-200 overflow-x-auto">
      <h3 className="text-lg font-semibold mb-4">Schedule Timeline</h3>
      
      <div className="min-w-[800px]">
        {/* Time Header */}
        <div className="flex border-b border-gray-200 pb-2 mb-2">
          <div className="w-24 flex-shrink-0">Train ID</div>
          <div className="flex-grow relative h-6">
            {hours.map(hour => (
              <div 
                key={hour} 
                className="absolute text-xs text-gray-500 transform -translate-x-1/2"
                style={{ left: `${((hour * 60 - timeToMinutes(timelineStart)) / (timeToMinutes(timelineEnd) - timeToMinutes(timelineStart))) * 100}%` }}
              >
                {hour}:00
              </div>
            ))}
          </div>
        </div>

        {/* Rows */}
        <div className="space-y-2">
          {activeTrainsets.map(train => (
            <div key={train.trainset_id} className="flex items-center h-12 hover:bg-gray-50">
              <div className="w-24 flex-shrink-0 font-medium text-sm">{train.trainset_id}</div>
              <div className="flex-grow relative h-8 bg-gray-100 rounded">
                {train.service_blocks?.map((block, index) => {
                  const durationHours = block.estimated_km / AVERAGE_SPEED_KMPH;
                  const durationMinutes = durationHours * 60;
                  const { left, width } = getPositionAndWidth(
                    block.departure_time,
                    durationMinutes,
                    timelineStart,
                    timelineEnd
                  );

                  return (
                    <div
                      key={index}
                      className="absolute h-full bg-blue-500 rounded opacity-80 hover:opacity-100 hover:bg-blue-600 transition-all cursor-pointer group"
                      style={{ left, width }}
                    >
                      {/* Tooltip */}
                      <div className="hidden group-hover:block absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 bg-black text-white text-xs p-2 rounded z-10">
                        <p className="font-bold">{block.block_id}</p>
                        <p>{block.origin} → {block.destination}</p>
                        <p>Dep: {block.departure_time}</p>
                        <p>Est. Dist: {block.estimated_km} km</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ScheduleTimeline;
