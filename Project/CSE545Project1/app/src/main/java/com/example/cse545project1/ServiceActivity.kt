package com.example.cse545project1

import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.ServiceConnection
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.IBinder
import android.util.Log
import android.view.View
import android.widget.TextView
import com.example.cse545project1.services.TimeService

class ServiceActivity : AppCompatActivity() {
    private lateinit var _tsService: TimeService
    private var _isBound: Boolean = false

    //
    private val _serviceStoppedLabel = "Service Not Running"

    // Logging
    private val _logLabel = "ServiceActivity"

    // ServiceConnection for bindService
    private val _connection = object : ServiceConnection {
        override fun onServiceDisconnected(className: ComponentName?) {
            _isBound = false;
        }

        override fun onServiceConnected(className: ComponentName?, service: IBinder?) {
            val binder = service as TimeService.TSBinder
            _tsService = binder.getTimeService()
            _isBound = true
        }
    }

    // Callbacks
    fun updateCurrentTime(v: View) {
        val textView = findViewById<TextView>(R.id.tv_time)

        if (_isBound) {
            // View the time on the TextView
            val date = _tsService.getCurrentTimeAsString()
            textView.text = date
            Log.v(_logLabel, date)
        }
        else {
            // Let user know that the service is not running
            textView.text = _serviceStoppedLabel
        }
    }

    fun startService(v: View) {
        // Bind to Time service
        if (!_isBound) {
            Log.v(_logLabel, "Binding service")
            Intent(this, TimeService::class.java).also {
                    intent-> bindService(intent, _connection, Context.BIND_AUTO_CREATE)
            }
        }
    }

    fun stopService(v: View) {
        // Unbind service if running
        if (_isBound) {
            unbindService(_connection)
            _isBound = false
        }
    }

    // Overrides
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_service)
    }

    override fun onStop() {
        super.onStop()
        // Housekeeping
        if (_isBound)
            unbindService(_connection)
    }
}