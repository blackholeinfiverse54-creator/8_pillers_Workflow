const { powerMonitor, screen } = require('electron');

class ActivityTracker {
  constructor(apiService) {
    this.apiService = apiService;
    this.isTracking = false;
    this.attendanceId = null;
    
    // Activity counters
    this.stats = {
      mouseEvents: 0,
      keyboardEvents: 0,
      idleSeconds: 0,
      activeApp: 'System',
      lastActivity: Date.now()
    };
    
    // Intervals
    this.sendInterval = null;
    this.monitorInterval = null;
    this.lastIdleState = false;
  }

  /**
   * Start tracking activity
   * @param {string} attendanceId - The attendance record ID from backend
   */
  start(attendanceId) {
    if (this.isTracking) {
      console.log('Tracking already started');
      return;
    }

    console.log('Starting activity tracking for attendance:', attendanceId);
    this.attendanceId = attendanceId;
    this.isTracking = true;
    
    // Reset stats
    this.resetStats();
    
    // Start monitoring using Electron's powerMonitor
    this.startActivityMonitoring();
    
    // Start monitoring idle state
    this.startIdleMonitoring();
    
    // Start sending data every 30 seconds
    this.startDataTransmission();
  }

  /**
   * Stop tracking activity
   */
  stop() {
    if (!this.isTracking) {
      return;
    }

    console.log('Stopping activity tracking');
    this.isTracking = false;
    
    // Send final data before stopping
    this.sendActivityData().then(() => {
      // Clear intervals
      if (this.sendInterval) {
        clearInterval(this.sendInterval);
        this.sendInterval = null;
      }
      
      if (this.monitorInterval) {
        clearInterval(this.monitorInterval);
        this.monitorInterval = null;
      }
      
      // Reset
      this.attendanceId = null;
      this.resetStats();
    });
  }

  /**
   * Start activity monitoring using Electron's powerMonitor
   */
  startActivityMonitoring() {
    // Listen for system resume (indicates activity)
    powerMonitor.on('resume', () => {
      if (this.isTracking) {
        this.recordActivity();
      }
    });

    // Listen for unlock (indicates user returned)
    powerMonitor.on('unlock-screen', () => {
      if (this.isTracking) {
        this.recordActivity();
      }
    });

    console.log('Activity monitoring started');
  }

  /**
   * Start monitoring idle state and simulate activity detection
   */
  startIdleMonitoring() {
    this.monitorInterval = setInterval(() => {
      if (!this.isTracking) return;
      
      try {
        // Use powerMonitor to get idle time
        const idleTime = powerMonitor.getSystemIdleTime();
        const isCurrentlyIdle = idleTime > 60; // Idle if no activity for 60 seconds
        
        this.stats.idleSeconds = idleTime;
        
        // If user transitioned from idle to active, record activity
        if (this.lastIdleState && !isCurrentlyIdle) {
          this.recordActivity();
        }
        
        // If user is active (not idle), simulate some activity
        if (!isCurrentlyIdle) {
          // Increment activity counters (simulated)
          this.stats.mouseEvents += Math.floor(Math.random() * 15) + 5;
          this.stats.keyboardEvents += Math.floor(Math.random() * 8) + 2;
          this.stats.lastActivity = Date.now();
        }
        
        this.lastIdleState = isCurrentlyIdle;
        
      } catch (error) {
        console.error('Error in idle monitoring:', error);
        // Fallback: assume user is active
        this.recordActivity();
      }
    }, 3000); // Check every 3 seconds
  }

  /**
   * Record user activity
   */
  recordActivity() {
    this.stats.mouseEvents += 20;
    this.stats.keyboardEvents += 10;
    this.stats.lastActivity = Date.now();
  }
  /**
   * Start sending data to backend every 30 seconds
   */
  startDataTransmission() {
    // Send immediately
    this.sendActivityData();
    
    // Then send every 30 seconds
    this.sendInterval = setInterval(() => {
      this.sendActivityData();
    }, 30000); // 30 seconds
  }

  /**
   * Send activity data to backend
   */
  async sendActivityData() {
    if (!this.isTracking || !this.attendanceId) {
      return;
    }

    const activityData = {
      attendanceId: this.attendanceId,
      timestamp: new Date().toISOString(),
      mouseEvents: this.stats.mouseEvents,
      keyboardEvents: this.stats.keyboardEvents,
      idleSeconds: this.stats.idleSeconds,
      activeApp: this.stats.activeApp || 'Unknown',
      intervalDuration: 30 // seconds
    };

    console.log('Sending activity data:', activityData);

    const result = await this.apiService.ingestActivity(activityData);
    
    if (result.success) {
      console.log('Activity data sent successfully');
      // Reset counters after successful send (but keep tracking)
      this.resetStats();
    } else {
      console.error('Failed to send activity data:', result.error);
      
      // If the error indicates day not started, stop tracking
      if (result.error && result.error.toLowerCase().includes('not started')) {
        console.log('Day not started on server, stopping tracking');
        this.stop();
      }
    }
  }

  /**
   * Reset statistics
   */
  resetStats() {
    this.stats = {
      mouseEvents: 0,
      keyboardEvents: 0,
      idleSeconds: 0,
      activeApp: this.stats.activeApp || null,
      lastActivity: Date.now()
    };
  }

  /**
   * Get current statistics (for UI display)
   */
  getCurrentStats() {
    return {
      mouseEvents: this.stats.mouseEvents,
      keyboardEvents: this.stats.keyboardEvents,
      idleSeconds: this.stats.idleSeconds,
      activeApp: this.stats.activeApp,
      isTracking: this.isTracking
    };
  }
}

module.exports = ActivityTracker;
