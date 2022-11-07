package com.example.cse545project1.services

import android.app.Service
import android.content.Intent
import android.os.Binder
import android.os.IBinder
import java.text.SimpleDateFormat
import java.util.Date

class TimeService : Service() {
    private val _binder: IBinder = TSBinder()
    private val _date = Date()
    private val _dateFormatter = SimpleDateFormat("HH:mm")

    inner class TSBinder : Binder() {
        // Internal class that gives the current time of the day
        fun getTimeService(): TimeService = this@TimeService
    }

    // API starts here
    fun getCurrentTime(): Date {
        return _date
    }

    fun getCurrentTimeAsString(): String {
        return _dateFormatter.format(_date)
    }

    // Overrides
    override fun onBind(intent: Intent): IBinder? {
        // Returns the TSBinder object
        return _binder;
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return super.onStartCommand(intent, flags, startId)
    }
}