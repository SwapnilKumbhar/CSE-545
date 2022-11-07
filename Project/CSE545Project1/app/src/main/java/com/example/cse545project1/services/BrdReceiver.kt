package com.example.cse545project1.services

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

class BrdReceiver : BroadcastReceiver() {

    private val _logTag = "BroadcastReceiver"

    private var _callback: ((i: Intent) -> Unit)? = null

    //
    fun setCallback(cb: ((i: Intent) -> Unit)) {
        Log.v(_logTag, "Registering Callback")
        _callback = cb;
    }

    // Overrides
    override fun onReceive(context: Context, intent: Intent) {
        // Invokes the passed callback function
        Log.v(_logTag, "Received broadcast!")
        _callback?.invoke(intent)
    }
}