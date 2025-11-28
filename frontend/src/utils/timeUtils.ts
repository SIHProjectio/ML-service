export const timeToMinutes = (time: string): number => {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
};

export const getPositionAndWidth = (
  startTime: string,
  durationMinutes: number, // or calculate from end time if available
  timelineStart: string = '05:00',
  timelineEnd: string = '23:00'
) => {
  const startMinutes = timeToMinutes(timelineStart);
  const endMinutes = timeToMinutes(timelineEnd);
  const totalMinutes = endMinutes - startMinutes;

  const currentStartMinutes = timeToMinutes(startTime);
  
  // Calculate position percentage
  const left = ((currentStartMinutes - startMinutes) / totalMinutes) * 100;
  
  // Calculate width percentage
  // Note: The data doesn't explicitly have duration or end time for blocks, 
  // but it has estimated_km. We might need to estimate duration or just show a fixed width 
  // or assume a speed. 
  // Wait, the blocks have departure_time. Do they have arrival time?
  // The JSON shows: "departure_time": "07:00", "estimated_km": 153.0.
  // It doesn't have arrival time.
  // I'll assume an average speed to calculate duration for visualization.
  // e.g., 60 km/h? 153 km -> ~2.5 hours.
  
  const estimatedDurationMinutes = (durationMinutes); 
  const width = (estimatedDurationMinutes / totalMinutes) * 100;

  return { left: `${left}%`, width: `${width}%` };
};
