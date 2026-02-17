/**
 * Utility functions for date formatting in Pakistan timezone
 */

export const formatToPakistanTime = (dateString: string): string => {
  try {
    // Create a new Date object from the date string
    const date = new Date(dateString);

    // Verify the date is valid
    if (isNaN(date.getTime())) {
      console.error('Invalid date string:', dateString);
      return dateString;
    }

    // Format the date using Pakistan timezone
    // Using Intl.DateTimeFormat with timeZone option should correctly convert the time
    return new Intl.DateTimeFormat('en-US', {
      timeZone: 'Asia/Karachi',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true // Use 12-hour format with AM/PM
    }).format(date);
  } catch (error) {
    console.error('Error formatting date to Pakistan time:', error);
    // Fallback to original date string if formatting fails
    return dateString;
  }
};

// Simplified function that only shows date without time
export const formatDateOnly = (dateString: string): string => {
  try {
    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
      console.error('Invalid date string:', dateString);
      return dateString;
    }

    return new Intl.DateTimeFormat('en-US', {
      timeZone: 'Asia/Karachi',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString;
  }
};

export const formatDateToPakistanDate = (dateString: string): string => {
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      timeZone: 'Asia/Karachi',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    console.error('Error formatting date to Pakistan date:', error);
    // Fallback to original date string if formatting fails
    return dateString;
  }
};

export const formatDateTimeRangePakistan = (startDate: string, endDate: string): string => {
  const startFormatted = formatToPakistanTime(startDate);
  const endFormatted = formatToPakistanTime(endDate);
  return `${startFormatted} - ${endFormatted}`;
};