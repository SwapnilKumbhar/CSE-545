package com.example.cse545project1

import android.content.Intent
import android.content.IntentFilter
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.TextView
import com.example.cse545project1.helpers.BrdReceiver
import java.text.SimpleDateFormat
import java.util.Date

class BroadcastActivity : AppCompatActivity() {
    private val _intentAction = "com.example.CSE545"
    private val _intentMsg = "Hello from broadcast!"

    private val _receiver = BrdReceiver()
    private val _intentFilter = IntentFilter(_intentAction)

    private val _dateFormatter = SimpleDateFormat("HH:mm")

    // Overrides
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_broadcast)

        // Set the receiver up
        _receiver.setCallback { i:Intent -> brdCallback(i) }
        registerReceiver(_receiver, _intentFilter)
    }

    override fun onDestroy() {
        super.onDestroy()
        // Unregister broadcast receiver
        unregisterReceiver(_receiver)
    }

    // Callback function for the receiver
    private fun brdCallback(i: Intent) {
        // Extract elements from the intent
        val intentAction = i.action
        val intentMsg = i.getStringExtra("Message")
        val intentTime = i.getStringExtra("Time")

        // Update textview
        val tv = findViewById<TextView>(R.id.broadcast_msg)
        // Set textview to the action of the intent
        tv.text = "Action: $intentAction \n" +
                "Message: $intentMsg \n" +
                "Time: $intentTime"
    }

    fun sendBroadcast(v: View) {
        val i = Intent()
        i.action = _intentAction
        i.putExtra("Message", _intentMsg)
        i.putExtra("Time", _dateFormatter.format(Date()))
        sendBroadcast(i)

        // Update on UI
        val tv = findViewById<TextView>(R.id.brd_sent_msg)
        tv.text = "Broadcasted message: $_intentMsg"
    }
}