package com.example.cse545project1

import android.content.Intent
import android.content.IntentFilter
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.TextView
import com.example.cse545project1.helpers.BrdReceiver

class BroadcastActivity : AppCompatActivity() {
    private val _intentAction = "com.example.CSE545"

    private val _receiver = BrdReceiver()
    private val _intentFilter = IntentFilter(_intentAction)

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
        // Update textview
        val tv = findViewById<TextView>(R.id.broadcast_msg)
        // Set textview to the action of the intent
        tv.text = i.action
    }

    fun sendBroadcast(v: View) {
        val i = Intent()
        i.action = _intentAction
        sendBroadcast(i)
    }
}