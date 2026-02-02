/**
 * Pillar Client for Workflow Blackhole
 * Connects to 8-Pillar Infrastructure via Bridge Service
 * 
 * Port: 8008 (Bridge)
 * Timeout: 2 seconds (fire-and-forget)
 */

const axios = require('axios');

const BRIDGE_URL = process.env.BRIDGE_URL || 'http://localhost:8008';
const TIMEOUT = 2000; // 2 seconds

class PillarClient {
  constructor() {
    this.bridgeUrl = BRIDGE_URL;
    this.enabled = process.env.PILLAR_INTEGRATION_ENABLED !== 'false';
    
    if (this.enabled) {
      console.log(`🌀 Pillar Client initialized: ${this.bridgeUrl}`);
    } else {
      console.log(`⚠️ Pillar integration disabled`);
    }
  }

  /**
   * Log attendance event to Bucket → Karma pipeline
   */
  async logAttendanceEvent(userId, userName, eventType, location = null, hoursWorked = null, metadata = {}) {
    if (!this.enabled) return { success: false, reason: 'disabled' };
    
    try {
      const response = await axios.post(
        `${this.bridgeUrl}/bridge/attendance/event`,
        {
          user_id: userId,
          user_name: userName,
          event_type: eventType,
          timestamp: new Date().toISOString(),
          location: location,
          hours_worked: hoursWorked,
          metadata: metadata
        },
        { timeout: TIMEOUT }
      );
      
      console.log(`✅ Pillar: Attendance event logged (${eventType})`);
      return response.data;
    } catch (error) {
      console.error(`⚠️ Pillar: Attendance logging failed - ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Assign task with AI routing via Core + Insight Flow
   */
  async assignTaskWithAI(taskId, title, assigneeId, assigneeName, priority, status, department, metadata = {}) {
    if (!this.enabled) return { success: false, reason: 'disabled' };
    
    try {
      const response = await axios.post(
        `${this.bridgeUrl}/bridge/task/assign`,
        {
          task_id: taskId,
          title: title,
          assignee_id: assigneeId,
          assignee_name: assigneeName,
          priority: priority,
          status: status,
          department: department,
          metadata: metadata
        },
        { timeout: 5000 } // 5 seconds for AI processing
      );
      
      console.log(`✅ Pillar: Task assigned with AI (${response.data.selected_agent})`);
      return response.data;
    } catch (error) {
      console.error(`⚠️ Pillar: AI task assignment failed - ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Log employee activity to PRANA → Bucket → Karma pipeline
   */
  async logEmployeeActivity(userId, activityType, productivityScore = null, metadata = {}) {
    if (!this.enabled) return { success: false, reason: 'disabled' };
    
    try {
      const response = await axios.post(
        `${this.bridgeUrl}/bridge/activity/log`,
        {
          user_id: userId,
          activity_type: activityType,
          timestamp: new Date().toISOString(),
          productivity_score: productivityScore,
          metadata: metadata
        },
        { timeout: TIMEOUT }
      );
      
      console.log(`✅ Pillar: Activity logged (${activityType})`);
      return response.data;
    } catch (error) {
      console.error(`⚠️ Pillar: Activity logging failed - ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Log salary calculation to Bucket → Karma pipeline
   */
  async logSalaryCalculation(userId, userName, month, baseSalary, hoursWorked, overtimeHours, totalSalary, metadata = {}) {
    if (!this.enabled) return { success: false, reason: 'disabled' };
    
    try {
      const response = await axios.post(
        `${this.bridgeUrl}/bridge/salary/calculate`,
        {
          user_id: userId,
          user_name: userName,
          month: month,
          base_salary: baseSalary,
          hours_worked: hoursWorked,
          overtime_hours: overtimeHours,
          total_salary: totalSalary,
          metadata: metadata
        },
        { timeout: TIMEOUT }
      );
      
      console.log(`✅ Pillar: Salary calculation logged (${month})`);
      return response.data;
    } catch (error) {
      console.error(`⚠️ Pillar: Salary logging failed - ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Check bridge health
   */
  async checkHealth() {
    if (!this.enabled) return { status: 'disabled' };
    
    try {
      const response = await axios.get(`${this.bridgeUrl}/health`, { timeout: TIMEOUT });
      return response.data;
    } catch (error) {
      return { status: 'unhealthy', error: error.message };
    }
  }

  /**
   * Get bridge statistics
   */
  async getStats() {
    if (!this.enabled) return { status: 'disabled' };
    
    try {
      const response = await axios.get(`${this.bridgeUrl}/bridge/stats`, { timeout: TIMEOUT });
      return response.data;
    } catch (error) {
      return { error: error.message };
    }
  }
}

// Export singleton instance
module.exports = new PillarClient();
