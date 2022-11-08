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
    fun onClick(v: View) {
        if (_isBound) {
            // View the time on the TextView
            val date = _tsService.getCurrentTimeAsString()
            val textView = findViewById<TextView>(R.id.tv_time)
            textView.text = date
            Log.v(_logLabel, date)
        }
    }

    // Overrides
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_service)
    }

    override fun onStart() {
        super.onStart()

        // Bind to Time service
        Log.v(_logLabel, "Binding service")
        Intent(this, TimeService::class.java).also {
            intent-> bindService(intent, _connection, Context.BIND_AUTO_CREATE)
        }
    }

    override fun onStop() {
        super.onStop()
        unbindService(_connection)
    }
}